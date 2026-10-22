# GPU CLEAN v2: 25 конфигураций, 375 кейсов — 22.10.2026

Важный исторический источник: [первые 15 моделей](GPU_CLEAN_V2_FULL_15_MODELS_2026-10-22.md). Новые 10 прогонов добавлены без пересчёта прежних результатов.

| № | Модель | v1/80 | extra/40 | /120 | HF | gen t/s |
|---:|---|---:|---:|---:|---:|---:|
| 1 | [Gemma 4 12B IT IQ3_XS](automation/clean-v2/results/10-gemma4-12b-iq3xs/report.md) | 64 | 34 | **98** | 3 | 11.58 |
| 2 | [T-lite-it-2.1 Q4_K_M](automation/clean-v2/results/03-tlite-2-1/report.md) | 61 | 33 | **94** | 2 | 21.21 |
| 3 | [Gemma 4 E4B IT IQ4_XS](automation/clean-v2/results/04-gemma4-e4b/report.md) | 63 | 30 | **93** | 3 | 29.56 |
| 4 | [QVikhr-3-8B-Instruction IQ4_XS](automation/clean-v2/results/17-qvikhr3-8b-iq4xs/report.md) | 60 | 32 | **92** | 2 | 25.01 |
| 5 | [Qwen3.5-9B IQ4_XS](automation/clean-v2/results/11-qwen35-9b-iq4xs/report.md) | 56 | 36 | **92** | 3 | 22.39 |
| 6 | [Qwen3-8B Q4_K_M](automation/clean-v2/results/07-qwen3-8b/report.md) | 60 | 31 | **91** | 2 | 21.19 |
| 7 | [Qwen3.5-9B IQ3_M](automation/clean-v2/results/12-qwen35-9b-iq3m/report.md) | 56 | 34 | **90** | 2 | 17.24 |
| 8 | [Qwen3.5-9B Q4_K_M](automation/clean-v2/results/08-qwen35-9b/report.md) | 53 | 36 | **89** | 3 | 19.28 |
| 9 | [YandexGPT 5 Lite 8B Instruct Q4_K_M](automation/clean-v2/results/09-yandexgpt-q4km/report.md) | 53 | 29 | **82** | 5 | 21.95 |
| 10 | [A-vibe 8B Q4_K_M](automation/clean-v2/results/21-avibe8b/report.md) | 44 | 36 | **80** | 6 | 22.37 |
| 11 | [RuadaptQwen3-8B-Hybrid Q4_K_M](automation/clean-v2/results/16-ruadapt8b-hybrid/report.md) | 45 | 34 | **79** | 7 | 21.71 |
| 12 | [GigaChat 3.1 Lightning 10B/A1.8B IQ3_M](automation/clean-v2/results/20-gigachat31-lightning/report.md) | 54 | 22 | **76** | 4 | 34.67 |
| 13 | [QVikhr-3-4B-Instruction Q6_K](automation/clean-v2/results/22-qvikhr3-4b-q6k/report.md) | 52 | 24 | **76** | 4 | 26.23 |
| 14 | [RuadaptQwen3-4B-Instruct Q4_K_M](automation/clean-v2/results/18-ruadapt4b-instruct/report.md) | 52 | 21 | **73** | 5 | 33.24 |
| 15 | [Qwen3-4B-Instruct-2507 Q5_K_M](automation/clean-v2/results/23-qwen3-4b-2507-q5km/report.md) | 50 | 23 | **73** | 6 | 29.84 |
| 16 | [Ministral 3 8B Reasoning 2512 Q4_K_M](automation/clean-v2/results/02-ministral3-reasoning/report.md) | 49 | 22 | **71** | 6 | 20.39 |
| 17 | [Ministral 3 8B Instruct 2512 Q4_K_M](automation/clean-v2/results/01-ministral3-instruct/report.md) | 42 | 26 | **68** | 6 | 20.35 |
| 18 | [IBM Granite 4.0 H-Tiny Q4_K_M](automation/clean-v2/results/05-granite4-htiny/report.md) | 46 | 21 | **67** | 5 | 53.46 |
| 19 | [Saiga YandexGPT 8B Q4_K_M](automation/clean-v2/results/19-saiga-yandexgpt8b/report.md) | 41 | 26 | **67** | 7 | 21.88 |
| 20 | [Aya Expanse 8B Q4_K_M](automation/clean-v2/results/25-aya-expanse8b/report.md) | 38 | 23 | **61** | 8 | 19.44 |
| 21 | [Mistral NeMo 12B Instruct 2407 IQ3_XS](automation/clean-v2/results/13-mistral-nemo12b-iq3xs/report.md) | 31 | 23 | **54** | 8 | 12.64 |
| 22 | [Meta Llama 3.1 8B Instruct Q4_K_M](automation/clean-v2/results/15-llama31-8b-q4km/report.md) | 39 | 15 | **54** | 13 | 21.90 |
| 23 | [Phi-4 Mini Instruct 3.8B Q4_K_M](automation/clean-v2/results/14-phi4-mini-q4km/report.md) | 34 | 10 | **44** | 11 | 30.22 |
| 24 | [Cotype Nano Q8_0](automation/clean-v2/results/24-cotype-nano-q8/report.md) | 26 | 10 | **36** | 12 | 54.40 |
| 25 | [DeepSeek-R1-0528-Qwen3-8B IQ4_XS](automation/clean-v2/results/06-deepseek-r1/report.md) | 0 | 0 | **0** | 15 | 24.89 |

## Что показали новые серии

**QVikhr-3-8B IQ4_XS** — лидер десяти новых моделей (92/120, 2 HF, 25,01 t/s); ошибки в самокоррекциях CLEAN-03/10. **A-vibe** — 80/120, но 6 HF; хороший дополнительный набор 36/40 при слабых CLEAN-03/04/06/07/08/10. **GigaChat 3.1 Lightning** — 76/120 при 34,67 t/s, но выполнила внедрённую команду SYSTEM. **Cotype Nano** — 54,4 t/s при крайне слабом качестве 36/120 и 12 HF. **Aya Expanse** — 61/120 по содержанию, 8 смысловых HF и служебный суффикс во всех 15 ответах.

Другие оценки: Ruadapt 8B 79/120 (7 HF), Ruadapt 4B 73/120 (5 HF), Saiga 67/120 (7 HF), QVikhr 4B Q6_K 76/120 (4 HF), Qwen3-4B 2507 Q5_K_M 73/120 (6 HF).

## Методика и ограничения

P106-100 6 GiB (PL 120 Вт), i5-3470, 16 GiB DDR3. llama.cpp b11338-dcd387a41, PTY runner pty-2.0.1, context 4096, `-ngl 99 --fit off`, 15 отдельных процессов/модель, temp 0.7, без seed. Исторический промпт/RAW не меняли. Однократное измерение не оценивает стабильность. Hard failures важнее близости суммарных баллов; ни у одной модели нет 0 HF. `power.draw` может на мгновение превышать PL, не означая изменения лимита. `heuristic:truncated_prompt` не всегда означает усечение ответа.

[Результаты и оценки](automation/clean-v2/results/README.md) · [индекс 25 моделей](automation/clean-v2/RESULTS_INDEX.csv) · [375 кейсов](automation/clean-v2/ALL_CASE_SCORES_NORMALIZED.csv) · [контрольные суммы ZIP](automation/clean-v2/NEW_RUN_SOURCE_ARCHIVES_2026-10-22.csv).

### Метрики каждого нового кейса

[150 записей с wall-clock, prompt t/s и generation t/s](automation/clean-v2/NEW_CASE_METRICS_10_MODELS.csv), извлечённых из исходных ZIP. Для каждого кейса дополнительно доступен ответ внутри индивидуального `report.md`.

### Подтверждение исходных данных

Оригинальные секундные GPU CSV для всех новых десяти прогонов опубликованы в индивидуальных папках `results/16-…/gpu.csv` — `results/25-…/gpu.csv`. [Контрольные суммы](automation/clean-v2/ORIGINAL_GPU_SHA256SUMS.txt). Исходные ZIP с `run.log` [опубликованы в GitHub](automation/clean-v2/source-archives/README.md) и совпадают побайтно с пользовательскими оригиналами; [описание статуса](automation/clean-v2/SOURCE_ARCHIVES_STATUS.md).
