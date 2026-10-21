# GPU CLEAN v2 — сводный отчёт по 15 конфигурациям (22.10.2026)

**Серия завершена.** Проведено **15 × 15 = 225** технически успешных отдельных запусков и выставлено **225 ручных оценок** по канонической шкале (4 критерия × 0–2 балла, максимум 8 за кейс и 120 на конфигурацию). Изначально в репозитории было 9 конфигураций; **6 новых** обработаны 21.10.2026.

- Полный [реестр качества и SHA-256](automation/clean-v2/RESULTS_INDEX.csv).
- [Папки 15 моделей](automation/clean-v2/results/README.md): `report.md` с RAW/эталоном/ответом, `scores.csv` с замечаниями, `gpu.csv` с ежесекундной телеметрией.
- [225 покейсных оценок](automation/clean-v2/ALL_CASE_SCORES_NORMALIZED.csv), [аудит условий](automation/clean-v2/PROTOCOL_AUDIT.md), [передача состояния](automation/clean-v2/HANDOFF_NEW_CHAT.md).
- [Неоценённые попытки и их ошибки](automation/clean-v2/ATTEMPTS_NOT_SCORED.md).

## 1. Итоговый рейтинг по баллам CLEAN v2

| Место по качеству | Модель / квантовка | v1 /80 | Дополнение /40 | Итого /120 | Hard failures | Генерация, ток/с |
|---:|---|---:|---:|---:|---:|---:|
| 1 | [Gemma 4 12B IT IQ3_XS](automation/clean-v2/results/10-gemma4-12b-iq3xs/report.md) | 64 | 34 | **98** | 3 | 11.58 |
| 2 | [T-lite-it-2.1 Q4_K_M](automation/clean-v2/results/03-tlite-2-1/report.md) | 61 | 33 | **94** | 2 | 21.21 |
| 3 | [Gemma 4 E4B IT IQ4_XS](automation/clean-v2/results/04-gemma4-e4b/report.md) | 63 | 30 | **93** | 3 | 29.56 |
| 4 | [Qwen3.5-9B IQ4_XS](automation/clean-v2/results/11-qwen35-9b-iq4xs/report.md) | 56 | 36 | **92** | 3 | 22.39 |
| 5 | [Qwen3-8B Q4_K_M](automation/clean-v2/results/07-qwen3-8b/report.md) | 60 | 31 | **91** | 2 | 21.19 |
| 6 | [Qwen3.5-9B IQ3_M](automation/clean-v2/results/12-qwen35-9b-iq3m/report.md) | 56 | 34 | **90** | 2 | 17.24 |
| 7 | [Qwen3.5-9B Q4_K_M](automation/clean-v2/results/08-qwen35-9b/report.md) | 53 | 36 | **89** | 3 | 19.28 |
| 8 | [YandexGPT 5 Lite 8B Instruct Q4_K_M](automation/clean-v2/results/09-yandexgpt-q4km/report.md) | 53 | 29 | **82** | 5 | 21.95 |
| 9 | [Ministral 3 8B Reasoning 2512 Q4_K_M](automation/clean-v2/results/02-ministral3-reasoning/report.md) | 49 | 22 | **71** | 6 | 20.39 |
| 10 | [Ministral 3 8B Instruct 2512 Q4_K_M](automation/clean-v2/results/01-ministral3-instruct/report.md) | 42 | 26 | **68** | 6 | 20.35 |
| 11 | [IBM Granite 4.0 H-Tiny Q4_K_M](automation/clean-v2/results/05-granite4-htiny/report.md) | 46 | 21 | **67** | 5 | 53.46 |
| 12 | [Mistral NeMo 12B Instruct 2407 IQ3_XS](automation/clean-v2/results/13-mistral-nemo12b-iq3xs/report.md) | 31 | 23 | **54** | 8 | 12.64 |
| 13 | [Meta Llama 3.1 8B Instruct Q4_K_M](automation/clean-v2/results/15-llama31-8b-q4km/report.md) | 39 | 15 | **54** | 13 | 21.90 |
| 14 | [Phi-4 Mini Instruct 3.8B Q4_K_M](automation/clean-v2/results/14-phi4-mini-q4km/report.md) | 34 | 10 | **44** | 11 | 30.22 |
| 15 | [DeepSeek-R1-0528-Qwen3-8B IQ4_XS](automation/clean-v2/results/06-deepseek-r1/report.md) | 0 | 0 | **0** | 15 | 24.89 |

**Важно:** порядок — по общей сумме баллов. Hard failures указаны **отдельно**, и высокий балл не означает пригодности модели без защитных мер. Пример: Gemma 4 12B IT IQ3_XS получила 98/120, но имела 3 критические ошибки; Llama 3.1 8B Instruct Q4_K_M — 54/120 и 13 критических ошибок, включая выполнение вложенных команд и выдуманную дату/время.

## 2. Характеристики единой серии

- Хост: Intel i5-3470 / 16 GiB DDR3 / NVIDIA Colorful P106-100 6 GiB (6144 MiB), **Power Limit 120 W**.
- `llama.cpp` версия `b11338-dcd387a41` (исполняемый SHA-256 `ea8b9eea55752f1c3a7b66bf4221af0a46f252d279a52b4ccd2ba4fb0e1c4e1b`).
- PTY runner `pty-2.0.1` SHA-256 `b84e83e5bea8f0d560fe3965a32a388ae37f48af13359cfb41a1aeef54a6c1ef`; все 15 процессов каждой модели создавались независимо.
- Флаги: `-ngl 99 --fit off -c 4096 -t 4 -tb 4 -ctk f16 -ctv f16 --reasoning off -st -n 256 --temp 0.7 --top-k 20 --top-p 0.8 --min-p 0 --presence-penalty 1.5`; базовый `system_prompt.txt` и исходные 10 CLEAN v1 кейсов оставлены без изменений, добавлены 5 стабильных CLEAN v2 кейсов.
- Source hashes: CLEAN v1 cases `9be46c13e0f189060270eff9c1a8b6d2c1846d4b` (Git SHA-1), system prompt `587312b015d42d607b40c3f75d31c985f8c370ab` (Git SHA-1), extension `0379e6ce2de6236c3a7890f0b793aa71a13a174b01db27964d70fe49f89767f8` (SHA-256).
- Единичные прогоны с температурой 0.7 и без seed означают, что небольшие различия баллов (например 2–3) могут зависеть от стохастики.

## 3. Шесть новых конфигураций и замеры VRAM

| Модель | Генерация, ток/с | Максимум VRAM, МиБ | Температура GPU, макс. |
|---|---:|---:|---:|
| Gemma 4 12B IT IQ3_XS | 11.58 | 6035 | 62 °C |
| Qwen3.5-9B IQ4_XS | 22.39 | 4739 | 59 °C |
| Qwen3.5-9B IQ3_M | 17.24 | 4457 | 60 °C |
| Mistral NeMo 12B IQ3_XS | 12.64 | 5629 | 63 °C |
| Phi-4 Mini Instruct 3.8B Q4_K_M | 30.22 | 3035 | 52 °C |
| Meta Llama 3.1 8B Instruct Q4_K_M | 21.90 | 5121 | 60 °C |

Показания `power.draw` у отдельных точек могут быть выше 120 W, но поле `power.limit` сохраняет 120 W. Максимальная RSS из GNU time — системная RAM, **не** VRAM.

## 4. Отдельные попытки, не вошедшие в рейтинг

- **YandexGPT 5 Lite 8B IQ3_M**, GGUF SHA-256 `e8833a0254ee77747683ef9cf34c7a002bfa03b76c3d70ea91179432a11578a6`: три smoke-теста с некорректными ответами, **SMOKE_FAILED / INVALID_OUTPUT**. Полный 15-кейсовый бенчмарк не запускался.
- **Gemma 4 12B IT IQ3_M**, GGUF SHA-256 `def80efba2f976bb0c9709f06845b237ba3092bf4d68d5b47fd84b4ef23f4439`: при запуске CUDA не смогла выделить 480 MiB KV-кеша, **VRAM_LIMIT / NOT_TESTED**. Отдельная успешная Gemma IQ3_XS — иная квантовка.
- Qwen3-4B Q4_K_M и Qwen3.5-4B Q4_K_M сознательно **пропущены** в этой новой полной серии CLEAN v2; они фигурируют в прошлых самостоятельных CPU/GPU протоколах.

**Не назначать этим попыткам 0/120.** Для сравнения, DeepSeek-R1 IQ4_XS действительно выполнила 15 процессов и получила **0/120** за негодный для CLEAN результат; это совершенно иной случай.

## 5. Границы сопоставимости и исторические документы

Исторические [CPU и GPU quick-triage](LLM_COMPARATIVE_RESULTS.md), [30 GPU CLEAN v1 кейсов от 20.10](GPU_CLEAN_V1_FULL_30_RUNS_2026-10-20.md), [единый отчёт от 20.10](LLM_BENCHMARKS_UNIFIED_REPORT_2026-10-20.md) и [полный протокол оборудования](TEST_PROTOCOL_AND_ENVIRONMENT.md) сохраняют прежнюю временную область. **Оценки /80 не пересчитывались задним числом в оценки /120.** Весовые GGUF (несколько ГБ каждый) и сырые ZIP логи в GitHub не публикуются; полные RAW/эталоны/ответы доступны в отчётах моделей, ZIP сохранены в разговорах и локальных файлах пользователя.

### Вывод

Если выбирать только по **максимальному баллу одного прогона**, лидер Gemma 4 12B IQ3_XS — **98/120**, но почти полностью заполняет VRAM 6 GiB и генерирует 11.58 ток/с. Среди более быстрых относительно качественных альтернатив — T-lite-it-2.1 (94/120, 21.21 ток/с, 2 HF), Gemma 4 E4B (93/120, 29.56 ток/с, 3 HF) и Qwen3.5-9B IQ4_XS (92/120, 22.39 ток/с, 3 HF). **Ни одна конфигурация не продемонстрировала 0 hard failures** — до production требуется оценка защиты от выполнения команд внутри RAW и более широкий повторяемый набор.
