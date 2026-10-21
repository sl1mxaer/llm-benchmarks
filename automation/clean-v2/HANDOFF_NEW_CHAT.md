# NUC+LLM — итоговая передача GPU CLEAN v2 (22.10.2026)

## Статус: серия завершена

- **15 конфигураций** проведены и вручную оценены по 15 RAW-кейсам — **225** кейсов; полный список и SHA-256 в [RESULTS_INDEX.csv](RESULTS_INDEX.csv).
- [Рейтинг, быстрые выводы и индивидуальные отчёты](results/README.md). В каждой папке `report.md` (RAW/reference/reply/комментарии), `scores.csv` (15 баллов) и `gpu.csv` (1 Гц).
- [ALL_CASE_SCORES_NORMALIZED.csv](ALL_CASE_SCORES_NORMALIZED.csv) — 225 однородных записей оценок.
- [ATTEMPTS_NOT_SCORED.md](ATTEMPTS_NOT_SCORED.md) — YandexGPT 5 Lite 8B IQ3_M (SMOKE_FAILED/INVALID_OUTPUT), Gemma 4 12B IQ3_M (VRAM_LIMIT/NOT_TESTED); баллы не присваивались.
- Qwen3-4B и Qwen3.5-4B пропущены в новой серии v2 **по решению пользователя**. Более ранний CLEAN v1 quick-triage отдельный.
- ZIP исходных результатов, логи и оригиналы CSV оставлены локально на `llm-server`, у пользователя и в прикреплённых файлах бесед; GGUF веса в GitHub не выкладывались.

## Строго неизменяемый эталон (для повторных прогонов)

- Хост `llm-server`, пользователь `artem`; Intel i5-3470 / 16 GiB DDR3 / NVIDIA Colorful P106-100 6 GiB, **Power Limit 120 Вт**.
- Исполняемый файл `/opt/llama.cpp/build-cuda-p106/bin/llama-cli`, версия `b11338-dcd387a41`, SHA-256 `ea8b9eea55752f1c3a7b66bf4221af0a46f252d279a52b4ccd2ba4fb0e1c4e1b`.
- `~/llm-bench-tools/clean_benchmark_pty.py` (`pty-2.0.1`), SHA-256 `b84e83e5bea8f0d560fe3965a32a388ae37f48af13359cfb41a1aeef54a6c1ef`. **Не путать** с более ранним `clean_benchmark.py`.
- Модели: `/srv/ai/models/text/*.gguf`, SHA-256 каждая в [RESULTS_INDEX.csv](RESULTS_INDEX.csv).
- Оригинальные CLEAN v1 cases blob SHA-1 `9be46c13e0f189060270eff9c1a8b6d2c1846d4b`; system prompt blob SHA-1 `587312b015d42d607b40c3f75d31c985f8c370ab`; v2 extra-cases SHA-256 `0379e6ce2de6236c3a7890f0b793aa71a13a174b01db27964d70fe49f89767f8`.
- Флаги: `-ngl 99 --fit off -c 4096 -t 4 -tb 4 -ctk f16 -ctv f16 --reasoning off -st -n 256 --temp 0.7 --top-k 20 --top-p 0.8 --min-p 0 --presence-penalty 1.5`, системный промпт через `-sysf /srv/ai/benchmarks/clean-v1/system_prompt.txt`. 15 независимых процессов; `--suite v2`. Отсутствует фиксированный seed.
- Для мониторинга `nvidia-smi --query-gpu=timestamp,temperature.gpu,power.draw,power.limit,memory.used,utilization.gpu --format=csv -l 1`.
- SHA-256 PTY-раннера и CLI обязательно проверять перед сравнением. Баг `Path.with_suffix('.zip')` может сокращать название ZIP для моделей с точкой; пользоваться путём из строки `Архив для отправки:`.

## Рейтинг и решение

| Модель | Баллы /120 | Hard | Gen, ток/с |
|---|---:|---:|---:|
| Gemma 4 12B IT IQ3_XS | **98** | 3 | 11.58 |
| T-lite-it-2.1 Q4_K_M | 94 | **2** | 21.21 |
| Gemma 4 E4B IT IQ4_XS | 93 | 3 | 29.56 |
| Qwen3.5-9B IQ4_XS | 92 | 3 | 22.39 |
| Qwen3-8B Q4_K_M | 91 | **2** | 21.19 |
| Qwen3.5-9B IQ3_M | 90 | **2** | 17.24 |
| Qwen3.5-9B Q4_K_M | 89 | 3 | 19.28 |

Остальные восемь и все исходные оценки см. [таблицу](results/README.md). **Ни одна модель не прошла всё без hard failures**, значит выбранный рабочий CLEAN всё ещё нуждается в проверках, например валидации результата и дополнительной защите от prompt injection. Показатели скорости — измерения именно этой frozen серии, а не общего llama-bench.

Не меняйте исходные CLEAN v1 RAW/system prompt/quick-triage и версию PTY-раннера задним числом. Исторические CPU/GPU отчёты от 19–20 октября описывают иной протокол и не должны перезаписываться новыми данными.

Следующий этап пользователь ещё не назначил: текущий план из 15 моделей завершён. Для новых моделей следует сохранять условия и отдельно отмечать ограничения VRAM, новые квантовки и различия версий движка.

[Подробный аудит и ограничения интерпретации](PROTOCOL_AUDIT.md).
