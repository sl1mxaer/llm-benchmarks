# NUC+LLM — локальные LLM benchmarks

Актуальное состояние: **22 октября 2026 года**. Репозиторий хранит проверяемые измерения локальных LLM на Intel i5-3470 и NVIDIA Colorful P106-100 6 GiB, а также правила оценки RAW→CLEAN.

## Главное: завершённый GPU CLEAN v2

**25 моделей/квантовок, 375 отдельных кейсов, единый frozen протокол, 15× ручной рейтинг /120.**

- **[Актуальный рейтинг и отчёт 25 моделей](GPU_CLEAN_V2_FULL_25_MODELS_2026-10-22.md)**
- [Историческая таблица первых 15 моделей](GPU_CLEAN_V2_FULL_15_MODELS_2026-10-22.md)
- [Обзор всех 25 моделей и ссылки на 25 подробных отчётов](automation/clean-v2/results/README.md)
- [Сводный индекс CSV — 25 моделей, SHA-256 и производительность](automation/clean-v2/RESULTS_INDEX.csv)
- [Покейсные оценки CSV — все 375 записей](automation/clean-v2/ALL_CASE_SCORES_NORMALIZED.csv)
- [Аудит неизменности CLI, промптов, кейсов и раннера](automation/clean-v2/PROTOCOL_AUDIT.md)
- [План воспроизведения / передача состояния](automation/clean-v2/HANDOFF_NEW_CHAT.md)
- [Проверенные неудачные попытки без баллов: YandexGPT IQ3_M и Gemma IQ3_M](automation/clean-v2/ATTEMPTS_NOT_SCORED.md)

**Краткая статистика:** лучший суммарный балл Gemma 4 12B IT IQ3_XS — **98/120** (3 hard failures, 11.58 ток/с); T-lite-it-2.1 — **94/120** (2 hard failures, 21.21 ток/с); Qwen3.5-9B IQ4_XS — **92/120** (3 hard failures, 22.39 ток/с). Ни у одной оценённой конфигурации нет нулевого числа hard failures, поэтому результаты нельзя трактовать как гарантию безопасной production очистки.

## Исторические отчёты (сохранили исходные цифры и даты)

- [Итоговый архив CPU/GPU испытаний до 20 октября](LLM_BENCHMARKS_UNIFIED_REPORT_2026-10-20.md).
- [CPU/GPU сравнительные результаты](LLM_COMPARATIVE_RESULTS.md).
- [Полный GPU CLEAN v1 — 30 прогонов (10 кейсов × 3 модели)](GPU_CLEAN_V1_FULL_30_RUNS_2026-10-20.md).
- [Сборка сервера и протокол среды](TEST_PROTOCOL_AND_ENVIRONMENT.md).

**Разделение методик принципиально:** quick-triage, CLEAN v1 /80, CLEAN v2 /120, llama-bench, CUDA SGEMM и постоянный llama-server измеряют разные режимы, не суммируются и не сопоставляются без условий. Веса GGUF и исходные архивы ZIP с логами хранятся вне GitHub; исходные модельные ответы и баллы опубликованы в `automation/clean-v2/results/`.

Источник оригинальных CLEAN v1 кейсов/рубрики — [sl1mxaer/llm-server-ai](https://github.com/sl1mxaer/llm-server-ai/tree/main/benchmarks/clean-v1). Канонические RAW, system prompt, тестовая рубрика и замороженный PTY-раннер не изменялись для подгонки результатов.

## Дополнительные серии №16–25

- [Сводный рейтинг 25 моделей](GPU_CLEAN_V2_FULL_25_MODELS_2026-10-22.md)
- [Полные RAW/REFERENCE/RESPONSE и комментарии к 150 новым ответам](automation/clean-v2/results/README.md)
- [Покейсная скорость и wall-time 150 новых тестов](automation/clean-v2/NEW_CASE_METRICS_10_MODELS.csv)
- [Архивные SHA-256 оригиналов 10 ZIP](automation/clean-v2/NEW_RUN_SOURCE_ARCHIVES_2026-10-22.csv)
