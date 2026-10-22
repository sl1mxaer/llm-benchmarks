# CLEAN v2 — результаты 25 конфигураций

**25 моделей / квантовок × 15 одинаковых RAW-кейсов = 375 независимых технически успешных запусков**. Тесты выполнялись на Intel i5-3470, 16 GiB DDR3, NVIDIA Colorful P106-100 6 GiB (Power Limit 120 Вт), `llama.cpp b11338-dcd387a41`. Для каждой модели фиксированы prompt, кейсы, параметры, системный промпт; `temp=0.7` без seed. Баллы вручную выставлялись по 8-балльной шкале, суммарно 120; hard failures учитываются отдельно.

## Первоисточник для новых десяти моделей

[Подробная автономная сводка](../CHAT_SOURCE_SUMMARY_10_MODELS_2026-10-22.md) сохраняет полный контекст оценки, 150 первичных ответов, 15 RAW/REFERENCE, хеши исходных файлов и разбор сильных и слабых сторон. В `scores.csv` и нормализованном индексе покейсные комментарии связаны с конкретными проверками; компоненты 0–2 для этих десяти серий не реконструированы из общей оценки 0–8.

## Все 25 моделей (в хронологии добавления)

| № | Модель / квантование | CLEAN v1 | Extra | Итого | HF | Gen, ток/с | Данные |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | [Ministral 3 8B Instruct 2512 Q4_K_M](01-ministral3-instruct/report.md) | 42/80 | 26/40 | **68/120** | 6 | 20.35 | [баллы](01-ministral3-instruct/scores.csv) · [GPU](01-ministral3-instruct/gpu.csv) |
| 2 | [Ministral 3 8B Reasoning 2512 Q4_K_M](02-ministral3-reasoning/report.md) | 49/80 | 22/40 | **71/120** | 6 | 20.39 | [баллы](02-ministral3-reasoning/scores.csv) · [GPU](02-ministral3-reasoning/gpu.csv) |
| 3 | [T-lite-it-2.1 Q4_K_M](03-tlite-2-1/report.md) | 61/80 | 33/40 | **94/120** | 2 | 21.21 | [баллы](03-tlite-2-1/scores.csv) · [GPU](03-tlite-2-1/gpu.csv) |
| 4 | [Gemma 4 E4B IT IQ4_XS](04-gemma4-e4b/report.md) | 63/80 | 30/40 | **93/120** | 3 | 29.56 | [баллы](04-gemma4-e4b/scores.csv) · [GPU](04-gemma4-e4b/gpu.csv) |
| 5 | [IBM Granite 4.0 H-Tiny Q4_K_M](05-granite4-htiny/report.md) | 46/80 | 21/40 | **67/120** | 5 | 53.46 | [баллы](05-granite4-htiny/scores.csv) · [GPU](05-granite4-htiny/gpu.csv) |
| 6 | [DeepSeek-R1-0528-Qwen3-8B IQ4_XS](06-deepseek-r1/report.md) | 0/80 | 0/40 | **0/120** | 15 | 24.89 | [баллы](06-deepseek-r1/scores.csv) · [GPU](06-deepseek-r1/gpu.csv) |
| 7 | [Qwen3-8B Q4_K_M](07-qwen3-8b/report.md) | 60/80 | 31/40 | **91/120** | 2 | 21.19 | [баллы](07-qwen3-8b/scores.csv) · [GPU](07-qwen3-8b/gpu.csv) |
| 8 | [Qwen3.5-9B Q4_K_M](08-qwen35-9b/report.md) | 53/80 | 36/40 | **89/120** | 3 | 19.28 | [баллы](08-qwen35-9b/scores.csv) · [GPU](08-qwen35-9b/gpu.csv) |
| 9 | [YandexGPT 5 Lite 8B Instruct Q4_K_M](09-yandexgpt-q4km/report.md) | 53/80 | 29/40 | **82/120** | 5 | 21.95 | [баллы](09-yandexgpt-q4km/scores.csv) · [GPU](09-yandexgpt-q4km/gpu.csv) |
| 10 | [Gemma 4 12B IT IQ3_XS](10-gemma4-12b-iq3xs/report.md) | 64/80 | 34/40 | **98/120** | 3 | 11.58 | [баллы](10-gemma4-12b-iq3xs/scores.csv) · [GPU](10-gemma4-12b-iq3xs/gpu.csv) |
| 11 | [Qwen3.5-9B IQ4_XS](11-qwen35-9b-iq4xs/report.md) | 56/80 | 36/40 | **92/120** | 3 | 22.39 | [баллы](11-qwen35-9b-iq4xs/scores.csv) · [GPU](11-qwen35-9b-iq4xs/gpu.csv) |
| 12 | [Qwen3.5-9B IQ3_M](12-qwen35-9b-iq3m/report.md) | 56/80 | 34/40 | **90/120** | 2 | 17.24 | [баллы](12-qwen35-9b-iq3m/scores.csv) · [GPU](12-qwen35-9b-iq3m/gpu.csv) |
| 13 | [Mistral NeMo 12B Instruct 2407 IQ3_XS](13-mistral-nemo12b-iq3xs/report.md) | 31/80 | 23/40 | **54/120** | 8 | 12.64 | [баллы](13-mistral-nemo12b-iq3xs/scores.csv) · [GPU](13-mistral-nemo12b-iq3xs/gpu.csv) |
| 14 | [Phi-4 Mini Instruct 3.8B Q4_K_M](14-phi4-mini-q4km/report.md) | 34/80 | 10/40 | **44/120** | 11 | 30.22 | [баллы](14-phi4-mini-q4km/scores.csv) · [GPU](14-phi4-mini-q4km/gpu.csv) |
| 15 | [Meta Llama 3.1 8B Instruct Q4_K_M](15-llama31-8b-q4km/report.md) | 39/80 | 15/40 | **54/120** | 13 | 21.90 | [баллы](15-llama31-8b-q4km/scores.csv) · [GPU](15-llama31-8b-q4km/gpu.csv) |
| 16 | [RuadaptQwen3-8B-Hybrid Q4_K_M](16-ruadapt8b-hybrid/report.md) | 45/80 | 34/40 | **79/120** | 7 | 21.71 | [баллы](16-ruadapt8b-hybrid/scores.csv) · [GPU](16-ruadapt8b-hybrid/gpu.csv) · [ZIP](../source-archives/20261022-160053_RuadaptQwen3-8B-Hybrid-Q4_K_M_874705b453_b2a7bb.zip) |
| 17 | [QVikhr-3-8B-Instruction IQ4_XS](17-qvikhr3-8b-iq4xs/report.md) | 60/80 | 32/40 | **92/120** | 2 | 25.01 | [баллы](17-qvikhr3-8b-iq4xs/scores.csv) · [GPU](17-qvikhr3-8b-iq4xs/gpu.csv) · [ZIP](../source-archives/20261022-164412_QVikhr-3-8B-Instruction-IQ4_XS_eb530f630d_f1edca.zip) |
| 18 | [RuadaptQwen3-4B-Instruct Q4_K_M](18-ruadapt4b-instruct/report.md) | 52/80 | 21/40 | **73/120** | 5 | 33.24 | [баллы](18-ruadapt4b-instruct/scores.csv) · [GPU](18-ruadapt4b-instruct/gpu.csv) · [ZIP](../source-archives/20261022-170739_RuadaptQwen3-4B-Instruct-Q4_K_M_1abbf99e0e_0e9b6b.zip) |
| 19 | [Saiga YandexGPT 8B Q4_K_M](19-saiga-yandexgpt8b/report.md) | 41/80 | 26/40 | **67/120** | 7 | 21.88 | [баллы](19-saiga-yandexgpt8b/scores.csv) · [GPU](19-saiga-yandexgpt8b/gpu.csv) · [ZIP](../source-archives/20261022-173310_saiga_yandexgpt_8b.zip) |
| 20 | [GigaChat 3.1 Lightning 10B/A1.8B IQ3_M](20-gigachat31-lightning/report.md) | 54/80 | 22/40 | **76/120** | 4 | 34.67 | [баллы](20-gigachat31-lightning/scores.csv) · [GPU](20-gigachat31-lightning/gpu.csv) · [ZIP](../source-archives/20261022-182544_GigaChat3.1-Lightning-10B-A1.zip) |
| 21 | [A-vibe 8B Q4_K_M](21-avibe8b/report.md) | 44/80 | 36/40 | **80/120** | 6 | 22.37 | [баллы](21-avibe8b/scores.csv) · [GPU](21-avibe8b/gpu.csv) · [ZIP](../source-archives/20261022-185836_A-vibe-8B-Q4_K_M_0a493e9e40_9e6ead.zip) |
| 22 | [QVikhr-3-4B-Instruction Q6_K](22-qvikhr3-4b-q6k/report.md) | 52/80 | 24/40 | **76/120** | 4 | 26.23 | [баллы](22-qvikhr3-4b-q6k/scores.csv) · [GPU](22-qvikhr3-4b-q6k/gpu.csv) · [ZIP](../source-archives/20261022-194140_QVikhr-3-4B-Instruction-Q6_K_4b75f6682b_834072.zip) |
| 23 | [Qwen3-4B-Instruct-2507 Q5_K_M](23-qwen3-4b-2507-q5km/report.md) | 50/80 | 23/40 | **73/120** | 6 | 29.84 | [баллы](23-qwen3-4b-2507-q5km/scores.csv) · [GPU](23-qwen3-4b-2507-q5km/gpu.csv) · [ZIP](../source-archives/20261022-195326_Qwen3-4B-Instruct-2507-Q5_K_M_66713ce35a_1df0b6.zip) |
| 24 | [Cotype Nano Q8_0](24-cotype-nano-q8/report.md) | 26/80 | 10/40 | **36/120** | 12 | 54.40 | [баллы](24-cotype-nano-q8/scores.csv) · [GPU](24-cotype-nano-q8/gpu.csv) · [ZIP](../source-archives/20261022-200802_Cotype-Nano-Q8_0_e946a7990f_929d03.zip) |
| 25 | [Aya Expanse 8B Q4_K_M](25-aya-expanse8b/report.md) | 38/80 | 23/40 | **61/120** | 8 | 19.44 | [баллы](25-aya-expanse8b/scores.csv) · [GPU](25-aya-expanse8b/gpu.csv) · [ZIP](../source-archives/20261022-203435_Aya-Expanse-8B-Q4_K_M_9592bad943_60f16b.zip) |


## Файлы и воспроизводимость

- **`report.md`** — RAW, REFERENCE, фактический RESPONSE, оценки и объяснение ошибок в каждом из 15 кейсов.
- **`scores.csv`** — ручные баллы за кейс и hard failures. Для первых 15 сохранены четыре компонента оценок; для последних 10 исходно зафиксирована только сумма /8, поэтому отсутствующие компонентные оценки оставлены пустыми, без выдумывания.
- **`gpu.csv`** — ежесекундная телеметрия NVIDIA (все 25 моделей). **`gpu-summary.csv`** — агрегаты новых 10 моделей.
- **`responses.json`** — дополнительно сохранены 15 фактических ответов для моделей 16–25.
- **[Исходные ZIP 10 новых моделей](../source-archives/README.md)** — настоящие бинарные архивы, сохранены с исходными именами и SHA-256; `manifest.json`, `run.log`, `metrics.csv`, полные RAW/REFERENCE/RESPONSE и вспомогательные файлы.
- [Сводный индекс](../RESULTS_INDEX.csv), [375 покейсных оценок](../ALL_CASE_SCORES_NORMALIZED.csv), [150 подробных измерений скорости новых моделей](../NEW_CASE_METRICS_10_MODELS.csv), [реестр SHA источников](../NEW_RUN_SOURCE_ARCHIVES_2026-10-22.csv), [методический аудит](../PROTOCOL_AUDIT.md).

## Ключевые результаты

**Первое место:** Gemma 4 12B IT IQ3_XS — **98/120**, HF 3, **11,58 ток/с**, почти полностью использует VRAM. **Сбалансированный вариант:** T-lite-it-2.1 Q4_K_M — **94/120**, HF 2, **21,21 ток/с**. Среди новых лучший **QVikhr-3-8B IQ4_XS** — **92/120**, HF 2, **25,01 ток/с**. Самая быстрая компактная Cotype Nano (54,40 ток/с) имеет всего **36/120 и 12 HF**. У Aya Expanse отдельно зафиксирован неизменный служебный токен во всех 15 ответах, а содержательная оценка — **61/120**.

Hard failures особенно опасны в кейсах CLEAN-07 и CLEAN-15, где RAW содержит команды, которые модель **не должна выполнять**. Техническое завершение `status=ok` не равнозначно правильной очистке. Однократные прогоны при `temp=0.7` не оценивают статистическую устойчивость.

[Полный рейтинг по убыванию качества](../../../GPU_CLEAN_V2_FULL_25_MODELS_2026-10-22.md) · [исторический отчёт первых 15 моделей](../../../GPU_CLEAN_V2_FULL_15_MODELS_2026-10-22.md).
