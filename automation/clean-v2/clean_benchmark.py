#!/usr/bin/env python3
"""LLM Benchmark CLEAN v1/v2 independent llama-cli batch benchmark. Python stdlib only."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid
import zipfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
EXPECTED_V1_CASES_BLOB_SHA1 = '9be46c13e0f189060270eff9c1a8b6d2c1846d4b'
EXPECTED_V1_PROMPT_BLOB_SHA1 = '587312b015d42d607b40c3f75d31c985f8c370ab'
USER_PREFIX = 'Отредактируй следующую RAW-транскрипцию согласно системным правилам. --- BEGIN RAW --- '
USER_SUFFIX = ' --- END RAW ---'
SAMPLE_OPTIONS = ['-c', '4096', '-t', '4', '-tb', '4', '-ctk', 'f16', '-ctv', 'f16',
                  '--reasoning', 'off', '-st', '-n', '256', '--temp', '0.7',
                  '--top-k', '20', '--top-p', '0.8', '--min-p', '0',
                  '--presence-penalty', '1.5']
METRIC_FIELDS = ['case_id', 'status', 'exit_code', 'wall_sec', 'prompt_tps',
                 'generation_tps', 'peak_rss_kb', 'major_faults', 'swaps',
                 'reply_extraction', 'log_file', 'response_file']
RATE_RX = re.compile(r'\[\s*Prompt:\s*([\d.]+)\s*t/s\s*\|\s*Generation:\s*([\d.]+)\s*t/s\s*\]')


def blob_sha1(content: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(content)).encode('ascii') + b'\0' + content).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for piece in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            h.update(piece)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def read_cases(path: Path, expected_count: int, id_prefix: str) -> list[dict]:
    data = read_json(path)
    cases = data['cases']
    if len(cases) != expected_count:
        raise ValueError(f'{path}: ожидается {expected_count} кейсов, найдено {len(cases)}')
    for idx, case in enumerate(cases, start=1 if id_prefix == 'v1' else 11):
        required = {'id', 'raw', 'reference_clean'}
        if not required.issubset(case) or not isinstance(case['raw'], str):
            raise ValueError(f'{path}: неверная структура кейса #{idx}')
        if id_prefix == 'v1' and case['id'] != f'clean-v1-{idx:02d}':
            raise ValueError(f'{path}: неожиданный ID #{idx}: {case["id"]}')
        if id_prefix == 'v2' and case['id'] != f'clean-v2-{idx:02d}':
            raise ValueError(f'{path}: неожиданный ID #{idx}: {case["id"]}')
    return cases


def parse_metric(metrics_text: str, pattern: str) -> int | None:
    m = re.search(pattern, metrics_text, flags=re.MULTILINE)
    return int(m.group(1)) if m else None


def parse_wall(metrics_text: str) -> float | None:
    m = re.search(r'^\s*Elapsed \(wall clock\) time \([^\n]*\):\s*([\d:.]+)', metrics_text, re.M)
    if not m:
        return None
    parts = list(map(float, m.group(1).split(':')))
    total = 0.0
    for v in parts:
        total = total * 60 + v
    return round(total, 3)


def extract_reply(log: str) -> tuple[str, str]:
    """Best-effort extraction. Never silently treat guesses as verified CLEAN text."""
    found = list(RATE_RX.finditer(log))
    if not found:
        return '', 'needs_review:no_timing_marker'
    before = log[:found[-1].start()]
    marker = '... (truncated)'
    if marker in before:
        text = before.rsplit(marker, 1)[-1]
        return text.strip(), 'heuristic:truncated_prompt'
    if USER_SUFFIX in before:
        text = before.rsplit(USER_SUFFIX, 1)[-1]
        return text.strip(), 'heuristic:full_prompt'
    return '', 'needs_review:prompt_boundary_unknown'


def update_csv(directory: Path, rows: list[dict]) -> None:
    temp = directory / 'metrics.csv.tmp'
    with temp.open('w', encoding='utf-8', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=METRIC_FIELDS)
        wr.writeheader()
        wr.writerows([{k: r.get(k, '') for k in METRIC_FIELDS} for r in rows])
    temp.replace(directory / 'metrics.csv')


def update_report(directory: Path, manifest: dict, rows: list[dict]):
    completed = [r for r in rows if r['status'] == 'ok']
    def mean(key: str):
        vals = [float(r[key]) for r in completed if r.get(key) not in (None, '')]
        return f'{sum(vals) / len(vals):.2f}' if vals else '—'
    lines = [
        '# CLEAN benchmark — автоматический технический отчёт', '',
        f'- Suite: **{manifest["suite"]}** ({manifest["case_count"]} кейсов)',
        f'- Model: `{manifest["model_file"]}`',
        f'- GGUF SHA-256: `{manifest["model_sha256"]}`',
        f'- Engine: `{manifest["engine"]}`; backend: `{manifest["backend"]}`; -ngl: `{manifest["gpu_layers"]}`',
        f'- Input verification: **{manifest["input_status"]}**',
        f'- Successful runs: **{len(completed)}/{manifest["case_count"]}**',
        '',
        '| Кейс | Status | Wall, с | Prompt, ток/с | Generation, ток/с | Peak RAM RSS, kB | Major | Swap | Exit | Ответ |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---|'
    ]
    by_id = {r['case_id']: r for r in rows}
    for c in manifest['cases']:
        r = by_id.get(c['id'])
        if not r:
            lines.append(f'| {c["id"]} | — | — | — | — | — | — | — | — | — |')
            continue
        answer = f'[{r["reply_extraction"]}]({r["response_file"]})' if r.get('response_file') else '—'
        lines.append('| ' + ' | '.join(str(x if x is not None else '—') for x in [
            c['id'], r['status'], r['wall_sec'], r['prompt_tps'], r['generation_tps'],
            r['peak_rss_kb'], r['major_faults'], r['swaps'], r['exit_code'], answer]) + ' |')
    lines += ['', f'- Mean prompt: **{mean("prompt_tps")} ток/с**',
              f'- Mean generation: **{mean("generation_tps")} ток/с**',
              f'- Mean process wall: **{mean("wall_sec")} с**',
              '', '## Оценка качества (вручную)', '',
              '- Первые CLEAN-01…10: **—/80** (дождаться ручной оценки по rubric.md).',
              '- Дополнительные CLEAN-11…15: **—/40** (только suite v2).',
              '- Общий итог CLEAN v2: **—/120** (только suite v2).',
              '- Hard failures: **не оценены**. Отсутствие crash не означает отсутствие смысловых ошибок.',
              '', '## Замечания по сопоставимости', '',
              '- Каждый кейс — самостоятельный процесс llama-cli и отдельная загрузка модели.',
              '- Настройки baseline CLEAN v1 сохранены, включая temperature=0.7 без fixed seed.',
              '- Системная RAM RSS не равна GPU VRAM; power/temperature не измеряются этим скриптом.',
              '- Статус извлечения reply с префиксом `heuristic` требует проверки сырого run.log.',
              '- `-ngl != 99` или другой `--engine` образуют отдельный профиль скорости относительно старого GPU CLEAN.',
              '- `—` означает отсутствие измерения или оценки, а не нулевое значение.', '']
    (directory / 'summary.md').write_text('\n'.join(lines), encoding='utf-8')


def archive_run(run_dir: Path) -> Path:
    """Create one shareable ZIP; do not include the model weights or production secrets."""
    archive = run_dir.with_suffix('.zip')
    temporary = archive.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        for file_path in sorted(run_dir.rglob('*')):
            if file_path.is_file():
                out.write(file_path, arcname=str(Path(run_dir.name) / file_path.relative_to(run_dir)))
    temporary.replace(archive)
    return archive


def main() -> int:
    p = argparse.ArgumentParser(description='Universal LLM Benchmark CLEAN v1/v2 independent benchmark')
    p.add_argument('--model', required=True, help='GGUF path; any supported GGUF chat model')
    p.add_argument('--suite', choices=['v1', 'v2'], default='v2')
    p.add_argument('--backend', choices=['gpu', 'cpu'], default='gpu')
    p.add_argument('--gpu-layers', type=int, default=99, help='GPU offload layer target (default 99 as CLEAN v1)')
    p.add_argument('--engine', default='/opt/llama.cpp/build-cuda-p106/bin/llama-cli')
    p.add_argument('--v1-cases', default='/srv/ai/benchmarks/clean-v1/cases.json')
    p.add_argument('--system-prompt', default='/srv/ai/benchmarks/clean-v1/system_prompt.txt')
    p.add_argument('--extra-cases', default=str(HERE / 'clean_v2_extra_cases.json'))
    p.add_argument('--output-dir', default=str(Path.home() / 'llm-bench-automated'))
    p.add_argument('--allow-input-drift', action='store_true', help='Permit noncanonical v1 input files, marked noncomparable')
    p.add_argument('--resume', help='Existing run directory to continue (model and suite must match)')
    args = p.parse_args()

    if args.gpu_layers < 0:
        p.error('--gpu-layers must be >= 0')
    model = Path(args.model).expanduser().resolve()
    engine = Path(args.engine).expanduser().resolve()
    source_v1 = Path(args.v1_cases).expanduser().resolve()
    prompt_file = Path(args.system_prompt).expanduser().resolve()
    extra_file = Path(args.extra_cases).expanduser().resolve()
    for desc, f in [('GGUF', model), ('llama-cli', engine), ('CLEAN v1 cases', source_v1), ('system prompt', prompt_file)]:
        if not f.is_file():
            p.error(f'{desc}: файл не найден: {f}')
    if args.suite == 'v2' and not extra_file.is_file():
        p.error(f'CLEAN v2 extra cases: файл не найден: {extra_file}')
    if shutil.which('/usr/bin/time') is None and not Path('/usr/bin/time').is_file():
        p.error('Не найден /usr/bin/time; необходим GNU time')

    data_case, data_prompt = source_v1.read_bytes(), prompt_file.read_bytes()
    sha_cases, sha_prompt = blob_sha1(data_case), blob_sha1(data_prompt)
    canonical = (sha_cases == EXPECTED_V1_CASES_BLOB_SHA1 and sha_prompt == EXPECTED_V1_PROMPT_BLOB_SHA1)
    if not canonical and not args.allow_input_drift:
        p.error('CLEAN v1 inputs отличаются от закреплённых версий GitHub; запуск остановлен. '
                'Для намеренно изменённого набора укажите --allow-input-drift (результат не будет сравним с baseline). '
                f'case_blob={sha_cases} prompt_blob={sha_prompt}')
    v1 = read_cases(source_v1, 10, 'v1')
    extra = read_cases(extra_file, 5, 'v2') if args.suite == 'v2' else []
    cases = v1 + extra
    extra_hash = hashlib.sha256(extra_file.read_bytes()).hexdigest() if extra else None
    print(f'Схема: CLEAN {args.suite}; независимые процессы: {len(cases)}')
    print(f'Модель: {model} ({model.stat().st_size} bytes); проверяю SHA-256...', flush=True)
    model_hash = sha256_file(model)
    engine_name = str(engine)
    engine_hash = sha256_file(engine)
    offload = ['-ngl', str(args.gpu_layers), '--fit', 'off'] if args.backend == 'gpu' else ['-ngl', '0', '--fit', 'off']
    profile = {'schema': 1, 'suite': args.suite, 'case_count': len(cases),
               'backend': args.backend, 'gpu_layers': args.gpu_layers if args.backend == 'gpu' else 0, 'model_file': str(model), 'model_sha256': model_hash,
               'engine': engine_name, 'engine_sha256': engine_hash, 'engine_file_bytes': engine.stat().st_size,
               'system_prompt': str(prompt_file), 'prompt_blob_sha1': sha_prompt,
               'v1_cases': str(source_v1), 'cases_blob_sha1': sha_cases,
               'extra_cases': str(extra_file) if extra else None, 'extra_sha256': extra_hash,
               'input_status': 'canonical-v1' if canonical else 'INPUT_DRIFT_NONCOMPARABLE',
               'flags': offload + SAMPLE_OPTIONS + ['-sysf', str(prompt_file)],
               'cases': [{'id': c['id'], 'raw': c['raw'], 'focus': c.get('focus', [])} for c in cases]}
    if args.resume:
        run_dir = Path(args.resume).expanduser().resolve()
        manifest_file = run_dir / 'manifest.json'
        if not manifest_file.is_file():
            p.error('--resume: manifest.json отсутствует')
        former = read_json(manifest_file)
        comparable_keys = ('suite', 'backend', 'gpu_layers', 'model_file', 'model_sha256', 'engine', 'engine_sha256',
                           'system_prompt', 'prompt_blob_sha1', 'cases_blob_sha1', 'extra_sha256', 'flags')
        if any(former.get(k) != profile.get(k) for k in comparable_keys):
            p.error('--resume: модель, файлы или параметры отличаются от сохранённого запуска')
    else:
        base = Path(args.output_dir).expanduser().resolve()
        base.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r'[^a-zA-Z0-9_.-]+', '-', model.stem)[:55]
        run_name = datetime.now().strftime('%Y%m%d-%H%M%S') + '_' + slug + '_' + model_hash[:10] + '_' + uuid.uuid4().hex[:6]
        run_dir = base / run_name
        run_dir.mkdir(mode=0o700)
        manifest_file = run_dir / 'manifest.json'
        profile['created_utc'] = datetime.now(timezone.utc).isoformat()
        manifest_file.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Папка результатов: {run_dir}', flush=True)

    rows = []
    for idx, case in enumerate(cases, 1):
        cid = case['id']
        folder = run_dir / cid
        result_file = folder / 'result.json'
        if result_file.is_file():
            prev = read_json(result_file)
            if prev['status'] == 'ok':
                rows.append(prev)
                print(f'[{idx:02d}/{len(cases)}] {cid}: уже записан (ok); пропуск', flush=True)
                continue
            # Preserve previous attempt artifacts before retrying a failed case.
            archive = folder / ('failed-attempt-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
            archive.mkdir(exist_ok=True)
            for name in ('result.json', 'run.log', 'time.txt', 'response.txt', 'raw.txt', 'prompt.txt', 'reference_clean.txt'):
                previous = folder / name
                if previous.exists():
                    previous.rename(archive / name)
            print(f'[{idx:02d}/{len(cases)}] {cid}: повтор неудачного кейса, предыдущая попытка архивирована', flush=True)
        folder.mkdir(exist_ok=True)
        prompt = USER_PREFIX + case['raw'] + USER_SUFFIX
        (folder / 'prompt.txt').write_text(prompt, encoding='utf-8')
        (folder / 'reference_clean.txt').write_text(case['reference_clean'], encoding='utf-8')
        (folder / 'raw.txt').write_text(case['raw'], encoding='utf-8')
        args_cli = ['/usr/bin/time', '-v', '-o', str(folder / 'time.txt'), str(engine),
                    '-m', str(model)] + offload + ['-c', '4096', '-t', '4', '-tb', '4',
                    '-ctk', 'f16', '-ctv', 'f16', '--reasoning', 'off', '-st',
                    '-sysf', str(prompt_file), '-p', prompt, '-n', '256', '--temp', '0.7',
                    '--top-k', '20', '--top-p', '0.8', '--min-p', '0', '--presence-penalty', '1.5']
        print(f'[{idx:02d}/{len(cases)}] {cid}: запуск...', flush=True)
        start = time.monotonic()
        try:
            run = subprocess.run(args_cli, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, encoding='utf-8', errors='replace', check=False)
            log, exit_code = run.stdout, run.returncode
        except KeyboardInterrupt:
            print('Прервано Ctrl+C, уже завершённые кейсы сохранены. Повторите с --resume.', file=sys.stderr)
            update_csv(run_dir, rows)
            update_report(run_dir, profile, rows)
            print(f'Частичный архив: {archive_run(run_dir)}', file=sys.stderr)
            return 130
        except OSError as exc:
            log, exit_code = f'OS ERROR: {exc}', 127
        elapsed = time.monotonic() - start
        (folder / 'run.log').write_text(log, encoding='utf-8')
        rate_match = list(RATE_RX.finditer(log))
        prompt_tps = float(rate_match[-1].group(1)) if rate_match else None
        generation_tps = float(rate_match[-1].group(2)) if rate_match else None
        response, extraction = extract_reply(log)
        (folder / 'response.txt').write_text(response + ('\n' if response else ''), encoding='utf-8')
        time_text = (folder / 'time.txt').read_text(encoding='utf-8', errors='replace') if (folder / 'time.txt').is_file() else ''
        wall = parse_wall(time_text)
        metrics = {'case_id': cid, 'status': 'ok' if exit_code == 0 and rate_match else 'failed',
                   'exit_code': exit_code, 'wall_sec': wall if wall is not None else round(elapsed, 2),
                   'prompt_tps': prompt_tps, 'generation_tps': generation_tps,
                   'peak_rss_kb': parse_metric(time_text, r'^\s*Maximum resident set size \(kbytes\):\s*(\d+)'),
                   'major_faults': parse_metric(time_text, r'^\s*Major \(requiring I/O\) page faults:\s*(\d+)'),
                   'swaps': parse_metric(time_text, r'^\s*Swaps:\s*(\d+)'),
                   'reply_extraction': extraction,
                   'log_file': str((folder / 'run.log').relative_to(run_dir)),
                   'response_file': str((folder / 'response.txt').relative_to(run_dir))}
        result_file.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        rows.append(metrics)
        update_csv(run_dir, rows)
        update_report(run_dir, profile, rows)
        print(f'[{idx:02d}/{len(cases)}] {cid}: status={metrics["status"]}, wall={metrics["wall_sec"]}s, '
              f'prompt={prompt_tps}, gen={generation_tps}, reply={extraction}', flush=True)
        if metrics['status'] == 'failed':
            print('Модель/движок завершились с ошибкой. Остальные кейсы не запускались; '
                  'сохраните логи и проверьте совместимость GGUF.', file=sys.stderr)
            print(f'Архив неудачной серии: {archive_run(run_dir)}', file=sys.stderr)
            return 1
    archive = archive_run(run_dir)
    print(f'Готово. Отчёт: {run_dir / "summary.md"}\nМетрики: {run_dir / "metrics.csv"}\nАрхив для отправки: {archive}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
