# CLEAN v2 · результаты 9 конфигураций

В каждой папке модели есть:
- **report.md** — полный Markdown-отчёт: RAW, эталон CLEAN, фактический ответ, ручные оценки по четырём критериям, ошибки и GPU-метрики.
- **scores.csv** — 15 оценок и комментарии.
- **gpu.csv** — ежесекундная телеметрия видеокарты.

[RESULTS_INDEX.csv](../RESULTS_INDEX.csv) — все 9 моделей и SHA-256 весов; [ALL_CASE_SCORES_NORMALIZED.csv](../ALL_CASE_SCORES_NORMALIZED.csv) — 135 унифицированных строк оценки. Оригинальные 9 ZIP с каждым run.log, manifest.json и результатами, а также байтовые оригиналы CSV сохранены в локальном архиве передачи.

| Папка | Конфигурация | Баллы /120 | Hard failures |
|---|---|---:|---:|
| 01-ministral3-instruct | Ministral 3 8B Instruct 2512 Q4_K_M | 68 | 6 |
| 02-ministral3-reasoning | Ministral 3 8B Reasoning 2512 Q4_K_M | 71 | 6 |
| 03-tlite-2-1 | T-lite-it-2.1 Q4_K_M | **94** | 2 |
| 04-gemma4-e4b | Gemma 4 E4B IT IQ4_XS | **93** | 3 |
| 05-granite4-htiny | IBM Granite 4.0 H-Tiny Q4_K_M | 67 | 5 |
| 06-deepseek-r1 | DeepSeek-R1-0528-Qwen3-8B IQ4_XS | 0 | 15 |
| 07-qwen3-8b | Qwen3-8B Q4_K_M | **91** | 2 |
| 08-qwen35-9b | Qwen3.5-9B Q4_K_M | 89 | 3 |
| 09-yandexgpt-q4km | YandexGPT 5 Lite 8B Q4_K_M | 82 | 5 |

Следующие: YandexGPT 5 Lite 8B IQ3_M, Gemma 4 12B IQ3_XS. Полный алгоритм — [HANDOFF_NEW_CHAT.md](../HANDOFF_NEW_CHAT.md).
