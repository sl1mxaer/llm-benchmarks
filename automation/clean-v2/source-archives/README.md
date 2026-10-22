# CLEAN v2 — десять оригинальных ZIP архивов

Все десять ZIP — **побайтно идентичные** файлам, полученным от пользователя 22.10.2026. Имена не изменены. Хеши SHA-256 находятся в [SHA256SUMS.txt](SHA256SUMS.txt); исходные Git blob SHA-1 проверены при переносе. ZIP содержат `manifest.json`, `run.log`, `metrics.csv`, 15 наборов `raw.txt`, `reference_clean.txt`, `response.txt`, `result.json`, `time.txt`, `prompt.txt` и другие данные прогона.

Ежесекундные оригинальные данные NVIDIA находятся по пути `../results/<model-slug>/gpu.csv` (каждый байтово совпадает с загруженным CSV). [Покейсные метрики](../NEW_CASE_METRICS_10_MODELS.csv), [общие баллы и SHA моделей](../RESULTS_INDEX.csv), [все индивидуальные отчёты](../results/README.md). Веса GGUF намеренно отсутствуют.

Для проверки ZIP после скачивания используйте SHA256SUMS.txt, например `sha256sum -c SHA256SUMS.txt` в Linux.
