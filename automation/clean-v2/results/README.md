# CLEAN v2 · результаты 25 конфигураций (22.10.2026)

**25 оценённых серий × 15 независимых процессов = 375 ответов CLEAN**. Все сравнимые серии запускались на NVIDIA Colorful P106-100 6 GiB с Power Limit 120 Вт и `llama.cpp b11338-dcd387a41`. Системный промпт, 15 RAW-кейсов и флаги `-ngl 99 --fit off -c 4096 -ctk f16 -ctv f16` оставались неизменными. У каждой серии — один прогон с `--temp 0.7` без фиксированного seed.

В каждой папке конфигурации: **report.md** (15 полных RAW, эталонов, ответов, оценок и замечаний), **scores.csv** (15 ручных оценок, 4 критерия и hard failures), **gpu.csv** (телеметрия 1 раз/с). Проверенные архивы прогонов с `run.log`/`manifest.json` хранятся локально и были приложены в чат; большие ZIP и веса GGUF в GitHub не помещались.

[Сводный индекс, SHA-256 и скорости](../RESULTS_INDEX.csv) · [225 нормализованных покейсных строк](../ALL_CASE_SCORES_NORMALIZED.csv) · [Аудит замороженного протокола](../PROTOCOL_AUDIT.md) · [Неоценённые попытки](../ATTEMPTS_NOT_SCORED.md)

| Папка | Конфигурация | v1 /80 | v2 доп. /40 | Итого /120 | Hard failures | Gen, ток/с |
|---|---|---:|---:|---:|---:|---:|
| [01-ministral3-instruct](01-ministral3-instruct/report.md) | Ministral 3 8B Instruct 2512 Q4_K_M | 42 | 26 | **68** | 6 | 20.35 |
| [02-ministral3-reasoning](02-ministral3-reasoning/report.md) | Ministral 3 8B Reasoning 2512 Q4_K_M | 49 | 22 | **71** | 6 | 20.39 |
| [03-tlite-2-1](03-tlite-2-1/report.md) | T-lite-it-2.1 Q4_K_M | 61 | 33 | **94** | 2 | 21.21 |
| [04-gemma4-e4b](04-gemma4-e4b/report.md) | Gemma 4 E4B IT IQ4_XS | 63 | 30 | **93** | 3 | 29.56 |
| [05-granite4-htiny](05-granite4-htiny/report.md) | IBM Granite 4.0 H-Tiny Q4_K_M | 46 | 21 | **67** | 5 | 53.46 |
| [06-deepseek-r1](06-deepseek-r1/report.md) | DeepSeek-R1-0528-Qwen3-8B IQ4_XS | 0 | 0 | **0** | 15 | 24.89 |
| [07-qwen3-8b](07-qwen3-8b/report.md) | Qwen3-8B Q4_K_M | 60 | 31 | **91** | 2 | 21.19 |
| [08-qwen35-9b](08-qwen35-9b/report.md) | Qwen3.5-9B Q4_K_M | 53 | 36 | **89** | 3 | 19.28 |
| [09-yandexgpt-q4km](09-yandexgpt-q4km/report.md) | YandexGPT 5 Lite 8B Instruct Q4_K_M | 53 | 29 | **82** | 5 | 21.95 |
| [10-gemma4-12b-iq3xs](10-gemma4-12b-iq3xs/report.md) | Gemma 4 12B IT IQ3_XS | 64 | 34 | **98** | 3 | 11.58 |
| [11-qwen35-9b-iq4xs](11-qwen35-9b-iq4xs/report.md) | Qwen3.5-9B IQ4_XS | 56 | 36 | **92** | 3 | 22.39 |
| [12-qwen35-9b-iq3m](12-qwen35-9b-iq3m/report.md) | Qwen3.5-9B IQ3_M | 56 | 34 | **90** | 2 | 17.24 |
| [13-mistral-nemo12b-iq3xs](13-mistral-nemo12b-iq3xs/report.md) | Mistral NeMo 12B Instruct 2407 IQ3_XS | 31 | 23 | **54** | 8 | 12.64 |
| [14-phi4-mini-q4km](14-phi4-mini-q4km/report.md) | Phi-4 Mini Instruct 3.8B Q4_K_M | 34 | 10 | **44** | 11 | 30.22 |
| [15-llama31-8b-q4km](15-llama31-8b-q4km/report.md) | Meta Llama 3.1 8B Instruct Q4_K_M | 39 | 15 | **54** | 13 | 21.90 |

### Итоги

- **Лидер по чистому качеству:** Gemma 4 12B IT IQ3_XS — **98/120**, 3 hard failures, **11,58 ток/с**. Использование GPU VRAM доходило до **6035 / 6144 МиБ**.
- **Сбалансированный скоростной вариант среди 9B:** Qwen3.5-9B IQ4_XS — **92/120**, 3 hard failures, **22,39 ток/с**. Разница с IQ3_M (**90/120**, 2 hard failures, 17,24 ток/с) получена на единичных стохастических прогонах.
- **Phi-4 Mini** — **44/120** при **30,22 ток/с**; **Mistral NeMo** — **54/120** при **12,64 ток/с**; **Llama 3.1 8B** — **54/120**, **13 hard failures** при **21,90 ток/с**. Скорость не компенсирует опасность исполнения инструкций внутри RAW и потери фактов.
- Дополнительные **YandexGPT IQ3_M** (SMOKE_FAILED / INVALID_OUTPUT) и **Gemma 4 12B IQ3_M** (VRAM_LIMIT / NOT_TESTED) не имеют баллов и **не включены в 15 строк**.
- **DeepSeek R1 0/120** — пройденный технический прогон с 15 непригодными для CLEAN ответами, не путать с отсутствующим результатом. У остальных моделей `status=ok` не гарантирует содержательно правильного ответа.

Результаты исторического CPU/GPU quick-triage, полных CLEAN v1 /80 и llama-bench от 19–20 октября **не объединены** с новым CLEAN v2 /120. Версии исходных тестов и системного промпта не менялись.


## Добавлены модели 16–25 (22.10.2026)

- [RuadaptQwen3-8B-Hybrid Q4_K_M](16-ruadapt8b-hybrid/report.md) — **79/120**, HF 7, 21.71 ток/с; [покейсные баллы](16-ruadapt8b-hybrid/scores.csv), [GPU summary](16-ruadapt8b-hybrid/gpu-summary.csv)
- [QVikhr-3-8B-Instruction IQ4_XS](17-qvikhr3-8b-iq4xs/report.md) — **92/120**, HF 2, 25.01 ток/с; [покейсные баллы](17-qvikhr3-8b-iq4xs/scores.csv), [GPU summary](17-qvikhr3-8b-iq4xs/gpu-summary.csv)
- [RuadaptQwen3-4B-Instruct Q4_K_M](18-ruadapt4b-instruct/report.md) — **73/120**, HF 5, 33.24 ток/с; [покейсные баллы](18-ruadapt4b-instruct/scores.csv), [GPU summary](18-ruadapt4b-instruct/gpu-summary.csv)
- [Saiga YandexGPT 8B Q4_K_M](19-saiga-yandexgpt8b/report.md) — **67/120**, HF 7, 21.88 ток/с; [покейсные баллы](19-saiga-yandexgpt8b/scores.csv), [GPU summary](19-saiga-yandexgpt8b/gpu-summary.csv)
- [GigaChat 3.1 Lightning 10B/A1.8B IQ3_M](20-gigachat31-lightning/report.md) — **76/120**, HF 4, 34.67 ток/с; [покейсные баллы](20-gigachat31-lightning/scores.csv), [GPU summary](20-gigachat31-lightning/gpu-summary.csv)
- [A-vibe 8B Q4_K_M](21-avibe8b/report.md) — **80/120**, HF 6, 22.37 ток/с; [покейсные баллы](21-avibe8b/scores.csv), [GPU summary](21-avibe8b/gpu-summary.csv)
- [QVikhr-3-4B-Instruction Q6_K](22-qvikhr3-4b-q6k/report.md) — **76/120**, HF 4, 26.23 ток/с; [покейсные баллы](22-qvikhr3-4b-q6k/scores.csv), [GPU summary](22-qvikhr3-4b-q6k/gpu-summary.csv)
- [Qwen3-4B-Instruct-2507 Q5_K_M](23-qwen3-4b-2507-q5km/report.md) — **73/120**, HF 6, 29.84 ток/с; [покейсные баллы](23-qwen3-4b-2507-q5km/scores.csv), [GPU summary](23-qwen3-4b-2507-q5km/gpu-summary.csv)
- [Cotype Nano Q8_0](24-cotype-nano-q8/report.md) — **36/120**, HF 12, 54.4 ток/с; [покейсные баллы](24-cotype-nano-q8/scores.csv), [GPU summary](24-cotype-nano-q8/gpu-summary.csv)
- [Aya Expanse 8B Q4_K_M](25-aya-expanse8b/report.md) — **61/120**, HF 8, 19.44 ток/с; [покейсные баллы](25-aya-expanse8b/scores.csv), [GPU summary](25-aya-expanse8b/gpu-summary.csv)

Общий рейтинг 25 моделей: [GPU_CLEAN_V2_FULL_25_MODELS_2026-10-22.md](../../../GPU_CLEAN_V2_FULL_25_MODELS_2026-10-22.md). Новые файлы не подменяют оригинальные ZIP/CSV, их контрольные суммы перечислены в [источниках](../NEW_RUN_SOURCE_ARCHIVES_2026-10-22.csv).
