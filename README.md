# NUC+LLM — локальные тесты LLM (CLEAN v2)

Актуальная дата серии: **22 октября 2026 года**. Репозиторий содержит измерения на i5-3470 / 16 GiB DDR3 / NVIDIA Colorful P106-100 6 GiB с Power Limit 120 Вт, а также единый benchmark RAW→CLEAN.

## Главные документы

- **[Итоговый рейтинг всех 25 моделей / 375 ответов](GPU_CLEAN_V2_FULL_25_MODELS_2026-10-22.md)** — баллы, hard failures, скорость и интерпретация.
- **[25 подробных отчётов](automation/clean-v2/results/README.md)** — для каждого кейса RAW / REFERENCE / RESPONSE, замечания и GPU.
- **[10 исходных ZIP последних прогонов — бинарные файлы](automation/clean-v2/source-archives/README.md)** и [SHA-256](automation/clean-v2/source-archives/SHA256SUMS.txt).
- [Индекс 25 моделей, GGUF SHA и пути](automation/clean-v2/RESULTS_INDEX.csv) · [Все 375 покейсных баллов](automation/clean-v2/ALL_CASE_SCORES_NORMALIZED.csv) · [150 измерений производительности новых моделей](automation/clean-v2/NEW_CASE_METRICS_10_MODELS.csv).
- [Аудит параметров и ограничений](automation/clean-v2/PROTOCOL_AUDIT.md) · [Реестр исходников](automation/clean-v2/NEW_RUN_SOURCE_ARCHIVES_2026-10-22.csv) · [Состояние исходных архивов](automation/clean-v2/SOURCE_ARCHIVES_STATUS.md).

## Краткий вывод

Лучшее качество одного прогона: **Gemma 4 12B IT IQ3_XS — 98/120**, 3 hard failures, 11,58 ток/с. Самый сбалансированный вариант среди лидеров по качеству: **T-lite-it-2.1 — 94/120**, 2 HF, 21,21 ток/с. Лучший из 10 дополнительных кандидатов: **QVikhr-3-8B IQ4_XS — 92/120**, 2 HF, 25,01 ток/с. Ни одна модель не прошла все hard-failure тесты без нарушений; для production нужны защитные механизмы и повторные прогоны.

## Тестовая методика

CLEAN v2: 10 канонических кейсов CLEAN v1 + 5 дополнений, 15 отдельных процессов на модель; `llama.cpp b11338-dcd387a41`, `-ngl 99 --fit off -c 4096 -t 4 -tb 4 -ctk f16 -ctv f16 --reasoning off -st -n 256 --temp 0.7 --top-k 20 --top-p 0.8 --min-p 0 --presence-penalty 1.5`; единый system prompt, без фиксированного seed. Отдельно проверяются сохранение смысла, правильная очистка/нормализация, сдержанность правок, исполнение prompt injection из RAW. Баллы ручные, максимум 8 на кейс, 120 на модель.

Оригинальные исходные кейсы и рубрика — [sl1mxaer/llm-server-ai](https://github.com/sl1mxaer/llm-server-ai/tree/main/benchmarks/clean-v1). Весовые GGUF в GitHub не публикуются; сохраняются их SHA-256. [План передачи состояния](automation/clean-v2/HANDOFF_NEW_CHAT.md) и [исключённые попытки без оценки](automation/clean-v2/ATTEMPTS_NOT_SCORED.md).

## Исторические отчёты (не изменялись)

- [Итоговый отчёт первых 15 CLEAN v2 моделей](GPU_CLEAN_V2_FULL_15_MODELS_2026-10-22.md).
- [CPU/GPU испытания до 20 октября](LLM_BENCHMARKS_UNIFIED_REPORT_2026-10-20.md).
- [Сравнение CPU/GPU](LLM_COMPARATIVE_RESULTS.md).
- [CLEAN v1 — 30 GPU прогонов](GPU_CLEAN_V1_FULL_30_RUNS_2026-10-20.md).
- [Протокол аппаратной среды](TEST_PROTOCOL_AND_ENVIRONMENT.md).

**Разные методики не суммируются:** quick-triage, CLEAN v1 /80, CLEAN v2 /120, llama-bench и SGEMM имеют разные условия и не должны смешиваться без явной маркировки.
