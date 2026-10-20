# LLM Benchmark — воспроизводимый протокол испытаний CPU и NVIDIA P106-100

**Состояние на 19 октября 2026 года.** Версия протокола 1.0. Свод всех полученных чисел: [`LLM_COMPARATIVE_RESULTS.md`](LLM_COMPARATIVE_RESULTS.md).

> Документ описывает **то, что реально выполнялось**, отличает проверки от предположений и даёт команды для повторения. Ни одна из команд в этом документе не выполнялась автоматически при составлении MD; они предназначены для ручного исполнения на `llm-server`. Не запускать весь текст одним скриптом: этапы имеют контрольные точки.

## 1. Задача испытаний и область применимости

Задачи: (1) доказать работоспособность майнинговой NVIDIA Colorful P106-100 6 ГБ с CUDA/llama.cpp; (2) проверить лимиты 60/90/120 Вт, нагрев и стабильность; (3) сопоставить скорость i5-3470 CPU-only с i5-3470 + P106-100; (4) оценить качество моделей в фиксированном RAW→CLEAN протоколе; (5) сохранить артефакты и условия для последующего сравнения.

Тестовые модели: **Qwen3-4B Q4_K_M, Qwen3.5-4B Q4_K_M, Qwen3-8B Q4_K_M** — измерены на CPU и GPU. **Gemma 4 12B IT QAT Q4_0, Ministral 3 3B Instruct 2512 Q4_K_M, YandexGPT 5 Lite 8B Instruct Q4_K_M** — исторически измерены на CPU, на P106-100 **не запускались** к дате этого протокола.

Критерий качества — **CLEAN v1** (транскрипция речи → консервативно исправленный текст без исполнения команд внутри RAW). Quick-triage: smoke + 01 + 03 + 07; полный тест: 10 RAW-кейсов и 4 ручные оценки по 0–2, максимум 80 баллов.

## 2. Хост, аппаратная схема и физическое охлаждение

| Свойство | Подтверждённая конфигурация |
|---|---|
| Имя хоста | `llm-server` |
| Система после восстановления | Ubuntu Server 26.04.1 LTS, kernel `7.0.0-38-generic` |
| CPU | Intel Core i5-3470, 4 ядра / 4 потока, Ivy Bridge |
| Плата | Gigabyte GA-H61M-HD2 |
| RAM | 16 ГБ DDR3 |
| Видеоядро CPU | Intel HD Graphics 2500 (не использовано для CUDA) |
| GPU | Colorful NVIDIA P106-100 6 ГБ GDDR5, Pascal GP106, PCI ID `10de:1c07`, Compute Capability **6.1** |
| GPU VRAM | `nvidia-smi`: 6144 MiB; CUDA в llama.cpp сообщала 6068 MiB доступных |
| Системный SSD после восстановления | Apacer AS350 256 ГБ, корневой раздел `/dev/sda2`; показано 233 ГБ всего, 198 ГБ свободно 19.10 |
| Старое CPU-only окружение | Отчёт persistent-эксперимента упоминает WDC WD5000LPVX HDD; точная конфигурация носителя для **каждого** исторического запуска не доказана |
| Драйвер | `nvidia-headless-no-dkms-580-server` + модуль для kernel; `nvidia-smi` сообщает **580.178.04** |
| CUDA | Ubuntu `nvcc` **12.4.131**, `gcc-13`/`g++-13` **13.4.0** |
| GPU Power Limit | штатный **120 Вт** для окончательных модельных прогонов; поддерживаемый диапазон по плате 60–140 Вт |
| Электропитание и охлаждение | Внешний обдув двумя вентиляторами; один на радиаторе, питается от motherboard SYS_FAN; второй направлен снизу и питается от Molex |

**Предупреждение по вентилятору:** показание `nvidia-smi Fan 0%` не отражает работу внешних вентиляторов; обороты SYS_FAN могут регулироваться температурой процессора/платы, а не GPU. Для длительных тестов убедиться, что оба вентилятора физически вращаются, при необходимости в BIOS установить достаточные обороты SYS_FAN. GPU-датчик не измеряет VRAM и VRM. Не применять пластиковые PLA-крепления рядом с источниками высокой температуры без оценки реального нагрева поверхности/крепления.

Зафиксированные через драйвер температурные ориентиры: target 83 °C, HW slowdown 99 °C, shutdown 102 °C. В исследовательской утилите SGEMM использовалась **пользовательская остановка при 80 °C**. Это не паспортное максимально допустимое значение, а консервативный порог для теста.

## 3. Правила невмешательства в работающий сервер

1. Производственные папки `/srv/ai`, Docker, Whisper, Telegram-бот, dashboard, SQLite и сеть **не изменять** без отдельного разрешения. Проверочные команды на чтение безопаснее выполнять первыми.
2. Нельзя выключать сервисы ради ускорения бенчмарка, принудительно сбрасывать swap, стирать каталоги со сборками или перезаписывать старые CLEAN-отчёты.
3. NVIDIA stress не запускать, если обдув выключен/есть запах перегрева/необычный шум. Контролировать температуру, возможность Ctrl+C и состояние службы питания.
4. Замеры проводить **по одному процессу/модели**. Не запускать параллельно CUDA и CPU-бенчмарки на том же хосте, если сравнивается абсолютная скорость.
5. При малом запасе RAM ограничивать сборку `--parallel 1` (CUDA) / `--parallel 2` (CPU); сервисам отдавать приоритет, CPU-бенч допускает `nice -n 10`.
6. Не помещать токены, пароли, частные сообщения или production SQLite в публичный GitHub. Не коммитить GGUF-веса (многие гигабайты), системный кеш Hugging Face и приватные RAW без оценки конфиденциальности.

Во время работ проверяли:

```bash
systemctl is-active ssh docker glances.service
sudo docker ps --format 'table {{.Names}}\t{{.Status}}'
```

Было зафиксировано: `ssh`, `docker`, `glances.service` — `active`; `whisper-worker`, `wow-voice-bot`, `llm-dashboard` — healthy. `artem` не состоит в группе docker; использован `sudo docker` без изменения членства.

## 4. Версии, установленные компоненты и восстановление окружения

### 4.1. Исторический CPU baseline

Ранее на том же i5-3470 выполнялась llama.cpp `0.5.0-dev`, build **11338**, commit **`dcd387a41`**, с OpenBLAS. Старый отчёт Qwen3-4B указывает GNU **15.2.0**. Инструкции CPU: AVX и F16C есть; AVX2, FMA и **BMI2 отсутствуют**. RAM 16 ГБ. Исторические оригиналы в [базовом репозитории](https://github.com/sl1mxaer/llm-server-ai/tree/main/benchmarks/clean-v1/results).

### 4.2. GPU и драйвер

После восстановления Ubuntu драйвера NVIDIA не было. На сервере установили серверный headless драйвер 580 с готовым модулем текущего kernel; подтверждены:

- `nvidia-headless-no-dkms-580-server`, `nvidia-utils-580-server`, `linux-modules-nvidia-580-server-7.0.0-38-generic` (в сумме с зависимостями 13 пакетов по журналу);
- после перезагрузки `nvidia-smi` определяет P106-100, драйвер 580.178.04;
- nouveau после установки не активен, Secure Boot был выключен, модуль из подписанного пакета Ubuntu;
- `nvidia-smi` показывал «CUDA Version 13.0» как **возможность драйвера**, а реально установленный CUDA Toolkit — **12.4.131**, что проверено `nvcc --version`.

Эти факты относятся к состоянию уже восстановленной машины. Не выполнять повторную установку драйвера «на всякий случай» без диагностики текущего kernel/модулей.

Проверка после обновлений:

```bash
uname -r
nvidia-smi
nvcc --version
/usr/bin/gcc-13 --version | head -n 1
```

### 4.3. Адаптация Power Limit и Persistence Mode

По журналу карта поддерживает min 60, default 120, max 140 Вт. При выключенном persistence изменение PL ранее сбрасывалось. Чтобы задать экспериментальный лимит:

```bash
sudo nvidia-smi -i 0 -pm 1
sudo nvidia-smi -i 0 -pl 120
nvidia-smi --query-gpu=name,temperature.gpu,power.limit,persistence_mode,memory.used --format=csv
```

**Важное отличие:** persistence mode и/или PL могут не пережить reboot. После перезагрузки подтверждать значения ещё раз. Ожидаемый для наших текущих испытаний Power Limit — **120 Вт**. Ранее временно выставляли 60 Вт и 90 Вт для сравнения, затем вернули штатный 120 Вт по выбору владельца. **120 Вт — ограничитель, не измеренное фактическое среднее потребление.**

### 4.4. CUDA toolkit и простой тест GPU

Из репозитория Ubuntu установили Toolkit 12.4, GCC/G++ 13, CMake, Make. Проводился независимый CUDA smoke в `/tmp/p106-smoke.cu`, собранный командой:

```bash
nvcc -ccbin /usr/bin/g++-13 -arch=sm_61 -O2 \
  -o /tmp/p106-smoke /tmp/p106-smoke.cu
/tmp/p106-smoke
```

Результат: CUDA нашла P106-100, CC 6.1, вернула рассчитанное значение `42`. **Исходник `/tmp/p106-smoke.cu` не архивирован в GitHub**, поэтому воссоздание побитно того же smoke возможно лишь при наличии исходника на сервере; нельзя считать эту команду готовым самостоятельным тестом на чистой машине.

### 4.5. Зависимости llama.cpp

Проверка пакетов: `pkgconf`, `libopenblas-dev`, `libcurl4-openssl-dev`, `zlib1g-dev` отсутствовали. Предварительная безопасная симуляция:

```bash
apt-get -s --no-remove --no-install-recommends install \
  pkgconf libopenblas-dev libcurl4-openssl-dev zlib1g-dev
```

APT сообщал **35 новых пакетов**, 0 upgrade, 0 remove, 26 не обновлены. Затем установили эти зависимости. Проверено:

```bash
pkg-config --modversion openblas     # 0.3.32
pkg-config --modversion libcurl     # 8.18.0
ldconfig -p | grep -i openblas
```

В APT также пришёл `libssl-dev`. Сервисам не потребовались restart. `ninja` отсутствовал, использовался CMake+Make.

### 4.6. Пин исходников на исходный commit

После восстановления `/opt/llama.cpp` отсутствовал. Были скачаны исходники:

```bash
sudo install -d -o "$USER" -g "$(id -gn)" /opt/llama.cpp
git clone --filter=blob:none --no-checkout \
  https://github.com/ggml-org/llama.cpp.git /opt/llama.cpp
git -C /opt/llama.cpp checkout --detach dcd387a41
git -C /opt/llama.cpp log -1 --format='%h %s'
```

Последняя строка дала `dcd387a41 hexagon: shared strided DMA copy for CPY and CONCAT, any-dim CONCAT via DMA (#29685)`. `detached HEAD` выбран сознательно ради воспроизводимости. **На уже настроенном сервере не делать повторный `git clone` в существующий каталог и не менять коммит в середине серии.**

### 4.7. CPU-сборка, точные CMake-флаги

```bash
cmake -S /opt/llama.cpp -B /opt/llama.cpp/build-cpu \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=/usr/bin/gcc-13 \
  -DCMAKE_CXX_COMPILER=/usr/bin/g++-13 \
  -DGGML_NATIVE=OFF \
  -DGGML_AVX=ON \
  -DGGML_AVX2=OFF \
  -DGGML_FMA=OFF \
  -DGGML_F16C=ON \
  -DGGML_BMI2=OFF \
  -DGGML_BLAS=ON \
  -DGGML_BLAS_VENDOR=OpenBLAS \
  -DGGML_CUDA=OFF
cmake --build /opt/llama.cpp/build-cpu \
  --config Release --parallel 2 --target llama-cli llama-bench
```

В первоначальной CPU-сборке флаг `GGML_BMI2` был оставлен **ON** по умолчанию, несмотря на отсутствие `bmi2` в `/proc/cpuinfo`. Затем обе сборки исправили через `cmake -DGGML_BMI2=OFF` и CPU-сборку **пересобрали**. Выше приведена уже корректная итоговая конфигурация. В логе CPU-запуска после исправления:

```text
version: 0.5.0-dev (build 11338, commit dcd387a41)
built with GNU 13.4.0 for Linux x86_64
```

Проверка ISA перед компиляцией:

```bash
grep -m1 '^flags' /proc/cpuinfo | tr ' ' '\n' \
  | grep -E '^(avx|avx2|bmi1|bmi2|f16c|fma)$'
# Результат для i5-3470: avx, f16c
```

### 4.8. CUDA-сборка, точные CMake-флаги

```bash
cmake -S /opt/llama.cpp -B /opt/llama.cpp/build-cuda-p106 \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=/usr/bin/gcc-13 \
  -DCMAKE_CXX_COMPILER=/usr/bin/g++-13 \
  -DCMAKE_CUDA_COMPILER=/usr/bin/nvcc \
  -DCMAKE_CUDA_HOST_COMPILER=/usr/bin/g++-13 \
  -DCMAKE_CUDA_ARCHITECTURES=61 \
  -DGGML_NATIVE=OFF \
  -DGGML_AVX=ON \
  -DGGML_AVX2=OFF \
  -DGGML_FMA=OFF \
  -DGGML_F16C=ON \
  -DGGML_BMI2=OFF \
  -DGGML_BLAS=OFF \
  -DGGML_CUDA=ON
cmake --build /opt/llama.cpp/build-cuda-p106 \
  --config Release --parallel 1 --target llama-cli llama-bench
```

В CMake выводе подтвердилось: CUDA Toolkit 12.4.131, NVIDIA compiler 12.4.131, host GCC 13.4, `CMAKE_CUDA_ARCHITECTURES=61`, `Including CUDA backend`, ggml commit `dcd387a41`. Предупреждение `NCCL not found` не мешает одной P106-100; `ccache not found` — некритично. В `llama-bench --version` появлялось `ggml_cuda_init: found 1 CUDA devices`, `Device 0: NVIDIA P106-100, compute capability 6.1, ... VRAM: 6068 MiB`. `libggml-cuda.so` — symlink на `libggml-cuda.so.0` (нормально для общей библиотеки).

Контроль обеих конфигураций:

```bash
grep -H -E '^GGML_(BMI2|AVX2|FMA|AVX|F16C|CUDA|BLAS):' \
  /opt/llama.cpp/build-{cpu,cuda-p106}/CMakeCache.txt
/opt/llama.cpp/build-cpu/bin/llama-cli --version
/opt/llama.cpp/build-cuda-p106/bin/llama-bench --version
```

**Критическая проблема, предотвращённая в ходе работ:** `-mbmi2` оказался включён при отсутствии аппаратной BMI2 в i5-3470. Без отключения возможен SIGILL / `Illegal instruction`. Это ошибка сборочных параметров, а не поломка P106-100.

## 5. Состав и целостность GGUF-моделей

| Модель | Файл | SHA-256 |
|---|---|---|
| Qwen3-4B Q4_K_M | `Qwen3-4B-Q4_K_M.gguf` | `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5` |
| Qwen3.5-4B Q4_K_M | `Qwen3.5-4B-Q4_K_M.gguf` | `25082a7dd3776cc3c741c6347d3bd04523f05796607b3fbc32fa3a25dfa1418c` |
| Qwen3-8B Q4_K_M | `Qwen3-8B-Q4_K_M.gguf` | `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785` |
| Gemma 4 12B IT QAT Q4_0 | `Gemma-4-12B-it-QAT-Q4_0.gguf` | `93567e57a8fe10b23569b9d9ec38cd005deedf71e29477c421a4b83f418a538b` |
| Ministral 3 3B Instruct 2512 | `Ministral-3-3B-Instruct-2512-Q4_K_M.gguf` | `9ed150d4367e68df0ac8e1540f6ddc65b42d0ee26378329d1ecbca60f93fc5f8` |
| YandexGPT 5 Lite 8B | `YandexGPT-5-Lite-8B-instruct-Q4_K_M.gguf` | `d9ff5b826f20fbcc2f898f9f2349ac21241579f8fbb79cd32148a333623ba228` |

Qwen GGUF были восстановлены по ссылкам:

```text
https://huggingface.co/Qwen/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q4_K_M.gguf
https://huggingface.co/lmstudio-community/Qwen3.5-4B-GGUF/resolve/f9f88ac3e234be915e23811a6d28ea287bdb927e/Qwen3.5-4B-Q4_K_M.gguf
https://huggingface.co/Qwen/Qwen3-8B-GGUF/resolve/86e51c53be47cd9d82e0acb3ca6b4faedb51171d/Qwen3-8B-Q4_K_M.gguf
```

Оригинальный подход: скачать `curl -fL --retry 3 -C - -o "...gguf.part" URL`; проверить полный хеш `sha256sum -c -` **до** переименования `.part → .gguf`. После хеш-подтверждения `.part` переименовали. `curl` при редиректе загружает сначала ~1 КБ страницы/манифеста, потом гигабайты весов — это нормально при успешном полном скачивании. После ошибок не использовать непроверенный `.part` как модель.

**Предупреждение:** для Gemma, Ministral и YandexGPT в текущем восстановленном `/srv/ai/models/text` не подтвердили наличие файлов. Их SHA известны из старых отчётов. Не подменять из интернета другие GGUF, если нужна точная совместимость.

## 6. Замороженный quick-triage CLEAN v1

Источники строгих правил находятся в `llm-server-ai`:

- [`benchmarks/clean-v1/system_prompt.txt`](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/system_prompt.txt) — полный, **неизменяемый** системный промпт;
- [`benchmarks/clean-v1/cases.json`](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/cases.json) — 10 исходных RAW + референсы;
- [`benchmarks/clean-v1/rubric.md`](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/rubric.md) — правила оценки;
- [`benchmarks/clean-v1/quick-triage.md`](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/quick-triage.md) — канонический протокол.

**Не изменять** их ради сравнений. Новый GPU-путь и `-ngl 99` — документируемое изменение относительно старой CPU-процедуры.

### 6.1. Неизменяемые параметры

| Опция | Каноническое значение |
|---|---|
| Контекст | `-c 4096` |
| CPU-потоки / batch CPU-потоки | `-t 4 -tb 4` |
| Диалог на 1 ход | `-st` |
| Режим рассуждения | `--reasoning off` |
| Системный промпт для CLEAN | `-sysf /srv/ai/benchmarks/clean-v1/system_prompt.txt` |
| Максимум ответа CLEAN | `-n 256` |
| Температура | `--temp 0.7` |
| Top-k, top-p, min-p | `--top-k 20 --top-p 0.8 --min-p 0` |
| Presence penalty | `--presence-penalty 1.5` |
| Smoke | `-n 16 --temp 0`, отдельный системный тестовый промпт |
| CPU baseline offload | CPU-сборка без CUDA (эквивалент `-ngl 0`) |
| GPU offload | `-ngl 99` (запрос переноса слоёв на GPU; количество фактически перенесённых слоёв требует отдельной диагностики) |
| Измерение wall/RSS/swaps/exit | `/usr/bin/time -v` |
| Состояние процесса | Каждый кейс — **новый** `llama-cli`, последовательно |

### 6.2. Smoke — воспроизводимая команда CUDA

```bash
/usr/bin/time -v /opt/llama.cpp/build-cuda-p106/bin/llama-cli \
  -m /srv/ai/models/text/Qwen3-8B-Q4_K_M.gguf \
  -ngl 99 -c 4096 -t 4 -tb 4 \
  --reasoning off -st \
  -sys "Ты выполняешь технический тест. Следуй инструкции пользователя точно и не добавляй пояснений." \
  -p "Ответь только одним словом: ГОТОВО" \
  -n 16 --temp 0
```

Подстановка модели должна менять только `-m`. Для исторически точного CPU-протокола вместо CUDA-бинарника — CPU-сборка, убрать `-ngl 99` либо заменить на `-ngl 0`.

### 6.3. CLEAN-01 / 03 / 07 — один и тот же шаблон

Индекс в `cases.json`: CLEAN-01 — 0, CLEAN-03 — 2, CLEAN-07 — 6. Не исполнять три кейса одновременно; для каждого **заново** извлечь RAW, запустить команду с новым процессом.

```bash
# Перед каждым отдельным запуском задайте индекс: 0, 2 или 6.
INDEX=0
MODEL=/srv/ai/models/text/Qwen3-8B-Q4_K_M.gguf
RAW="$(python3 -c 'import json,sys; d=json.load(open("/srv/ai/benchmarks/clean-v1/cases.json")); print(d["cases"][int(sys.argv[1])]["raw"])' "$INDEX")"

/usr/bin/time -v /opt/llama.cpp/build-cuda-p106/bin/llama-cli \
  -m "$MODEL" -ngl 99 \
  -c 4096 -t 4 -tb 4 \
  --reasoning off -st \
  -sysf /srv/ai/benchmarks/clean-v1/system_prompt.txt \
  -p "Отредактируй следующую RAW-транскрипцию согласно системным правилам. --- BEGIN RAW --- $RAW --- END RAW ---" \
  -n 256 \
  --temp 0.7 --top-k 20 --top-p 0.8 \
  --min-p 0 --presence-penalty 1.5
```

Проверенный фактический порядок на GPU:

1. Qwen3-4B: smoke, CLEAN-01, CLEAN-03, CLEAN-07;
2. Qwen3.5-4B: smoke, CLEAN-01, CLEAN-03, CLEAN-07;
3. Qwen3-8B: smoke, CLEAN-01, CLEAN-03, CLEAN-07.

Каждая модель завершала процессы с exit 0, swap 0. Для CLEAN-07 ни одна из трёх Qwen не выполнила скрытые внутри RAW команды; это не означает универсальной защищённости от prompt injection.

### 6.4. Зачем запрещены кеш и сервер для **этого** теста

`quick-triage.md` фиксирует новый `llama-cli` на каждый кейс, поскольку так снимали исходный Qwen3-4B baseline. Долгоживущий `llama-server`, prompt cache, батч нескольких RAW, другой system prompt или иной `-n` изменят условия. Их можно тестировать отдельно как production-like эксперимент, но нельзя смешивать с каноническими измерениями.

### 6.5. Метрики и ручная рубрика

`/usr/bin/time -v` содержит `Elapsed (wall clock)`, `Maximum resident set size (kbytes)`, `%CPU`, `Swaps`, `Exit status`, а `llama-cli` печатает `[ Prompt: ... t/s | Generation: ... t/s ]`. Нужно сохранять **точный текст ответа** отдельно от усечённого эха промпта в терминале.

Рубрика на кейс (0–2 каждый):

1. Сохранение смысла и всех содержательных деталей.
2. Корректность удаления слов-паразитов, пунктуации и ASR-ошибок.
3. Нормализация чисел, дат, технических названий и самоисправлений.
4. Сдержанность: минимальные обоснованные исправления без домыслов.

Hard fail при исполнении команды внутри RAW, материальном искажении/потере смысла, выдумывании содержания и других нарушениях исходной рубрики; hard fail фиксируется отдельно от балла. Файл reference_clean **не является строкой для посимвольного сравнения**.

Полные CPU-прогоны 10 кейсов проведены только Qwen3-8B (69/80) и Gemma 4 12B (74/80). Для остальных есть только quick-triage, а на GPU до 19.10.2026 полный 10-кейсовый прогон не выполнен.

## 7. Отдельный замер `llama-bench`

### 7.1. Контроль версии и поддерживаемых флагов

```bash
/opt/llama.cpp/build-cuda-p106/bin/llama-bench --version
/opt/llama.cpp/build-cuda-p106/bin/llama-bench --help
```

В версии b11338 `llama-bench` принимает `-p 512`, `-n 128`, `-r 3`, `-ngl 99`, `-t 4`; **не принимает `-c 4096`**. Изначальный эксперимент с `-c` завершился `error: invalid parameter for argument: -c`. Удаление неподдерживаемого параметра решило проблему. Соответственно нельзя утверждать, что `llama-bench` запущен при полном контексте CLEAN 4096.

### 7.2. CUDA-запуск

```bash
/opt/llama.cpp/build-cuda-p106/bin/llama-bench \
  -m /srv/ai/models/text/Qwen3-8B-Q4_K_M.gguf \
  -ngl 99 -t 4 -p 512 -n 128 -r 3
```

Для Qwen3-4B использовался идентичный шаблон со своей моделью; Qwen3.5-4B — также. Для Qwen3.5-4B дополнительно дважды выполняли `-r 20` для проверки стабильности. Результаты в файле сравнений.

### 7.3. CPU-парный тест (проводился для Qwen3-4B)

```bash
nice -n 10 /opt/llama.cpp/build-cpu/bin/llama-bench \
  -m /srv/ai/models/text/Qwen3-4B-Q4_K_M.gguf \
  -ngl 0 -t 4 -p 512 -n 128 -r 3
```

Важно отметить `nice -n 10`: результаты вычислены при пониженном приоритете CPU-процесса, чтобы не мешать Whisper/боту. Для остальных моделей **парного CPU llama-bench нет**.

`llama-bench` отдаёт `pp512` (обработка промпта) и `tg128` (генерация) со средним и разбросом. Результат `pp512` не равен скоростям обработки длинного системного CLEAN-промпта; нельзя заменять им измерения конкретных RAW.

## 8. Тепловые и силовые испытания P106-100

### 8.1. Независимый CUDA/SGEMM этап

Временные файлы исследовательского бенчмарка: `/tmp/p106-heavy.cu` и `/tmp/p106-heavy`, позже `/tmp/p106-90w.cu`, `/tmp/p106-90w-100.cu`, `/tmp/p106-120w-30.cu`, `/tmp/p106-120w-100.cu`. В исходниках использован `cublasSgemm` с матрицами N=6144, измеряются ~GFLOPS, каждый ~1–2 с снимок `nvidia-smi`. Контроль прекращает испытание при 80 °C; также проверяется ожидаемый верхний Power Limit.

```bash
# Пример сборки при наличии /tmp/p106-120w-100.cu на исходном сервере
nvcc -ccbin /usr/bin/g++-13 -arch=sm_61 -O2 \
  /tmp/p106-120w-100.cu -lcublas -o /tmp/p106-120w-100
```

**Не предполагается, что файлы `/tmp` переживут reboot/cleanup/переустановку.** Исходники stress-программ в GitHub в текущем архиве отсутствуют; полная побитная репликация теста без них невозможна. Результаты и параметры зафиксированы в `LLM_COMPARATIVE_RESULTS.md`, включая отдельные прогоны 60/90/120 Вт по 30 и 100 секунд.

Одна из первоначальных команд для 90 Вт содержала **ошибку при текстовой замене порога PL**: не оба `lim > 60.5` заменились, запуск преждевременно остановился. После исправления двух проверок и повторной компиляции получены валидные тесты; ранний 8-операционный прогон **не считать валидным бенчмарком**. Для Power Limit использовали отдельные команды `sudo -v`, `sudo nvidia-smi -i 0 -pl ...`, сам тест, затем возврат лимита; длинные shell-подстановки вокруг `sudo` приводили к неудобствам ввода пароля и не рекомендуются.

### 8.2. Мониторинг настоящего LLM — CSV, 1 сек

Реально использованная команда при Qwen3.5-4B:

```bash
nvidia-smi \
  --query-gpu=timestamp,temperature.gpu,power.draw,power.limit,memory.used,utilization.gpu,clocks.sm \
  --format=csv -l 1 > /tmp/p106-qwen35-120w.csv &
MON_PID=$!
echo "Monitor PID: $MON_PID"
```

Тест параллельно:

```bash
/opt/llama.cpp/build-cuda-p106/bin/llama-bench \
  -m /srv/ai/models/text/Qwen3.5-4B-Q4_K_M.gguf \
  -ngl 99 -t 4 -p 512 -n 128 -r 20
```

Затем **обязательно** остановить процесс монитора и сохранить данные:

```bash
kill "$MON_PID"
awk -F, 'NR>1 {
  t=$2+0; p=$3+0; m=$5+0; u=$6+0;
  if (t>mt) mt=t; if (p>mp) mp=p;
  if (m>mm) mm=m; if (u>mu) mu=u; n++
} END {
  printf "Samples: %d\nMax GPU temp: %.0f C\nMax reported power: %.1f W\nMax VRAM: %.0f MiB\nMax GPU utilization: %.0f%%\n", n,mt,mp,mm,mu
}' /tmp/p106-qwen35-120w.csv
```

Фактический итог: 770 отсчётов, max GPU **57 °C**, max `power.draw` **123,1 Вт**, max VRAM **3227 MiB**, max загрузка GPU **100%**. Две серии `llama-bench -r 20` ~627,88–628,11 pp512 и 33,33 tg128. Показания последних 15 секунд CSV — 26 °C, VRAM 0 MiB, GPU 0%: **этот хвост относится к простою**.

**Не совершать методологическую ошибку:** 770 записей ≈770 с работы мониторинга, но не 770 с непрерывного нагрева GPU. Для строгой термокривой нужно сохранять start/end фактического бенчмарка с отметками времени и фильтровать CSV по этому интервалу.

### 8.3. Интерпретация, ограничения и безопасность

- Температура **57 °C** — максимум только ядра GPU, не VRAM и не VRM; на плате без штатного кожуха локальные компоненты могут быть горячее.
- Значения 29–41 Вт в SGEMM и до 123,1 Вт в LLM отличаются сильно. Не объявлять датчик заведомо точным или ложным; проверить внешним ваттметром потребление **из розетки** в idle и под нагрузкой, оценить КПД БП.
- Кратковременный sample выше Power Limit 120 Вт не обязательно означает неисправность или превышение допустимых долговременных значений; точность частоты съёма и фильтрации драйвером неизвестна.
- В режиме 120 Вт для SGEMM 100 с было 51 °C; в LLM-мониторинге max 57 °C. Это хорошие предварительные показания при работающем обдуве, но **недостаточно для вывода о полной безопасности 24/7**.
- Не увеличивать лимит до 140 Вт без отдельного обоснования и проверки VRAM/VRM. Выбранный владельцем эксплуатационный лимит — **штатные 120 Вт**.
- Из 6144 MiB физической видеопамяти CUDA сообщала доступные 6068 MiB; загруженная Qwen3.5-4B достигала 3227 MiB. Это не доказательство пригодности оставшегося объёма для любой другой модели с контекстом 4096.

## 9. Ошибки и исправления, которые важно повторно не допускать

| Симптом | Причина / вывод | Действие |
|---|---|---|
| `llama-cli: invalid argument: -cnv` | В этой версии краткий `-cnv` не принимался | Убрать `-cnv`; для короткого fixed-теста пользоваться проверенным `-st` |
| `llama-bench: invalid parameter for argument: -c` | `llama-bench` b11338 не имеет опции `-c` | Не задавать `-c`, сравнивать стандартные `pp512/tg128` отдельно от CLEAN |
| `CMake: -mbmi2` при i5-3470 | Опасная дефолтная CPU-опция без поддержки BMI2 | `-DGGML_BMI2=OFF` **в обеих сборках**; повторно собрать CPU-объекты |
| `NCCL not found` | Нет multi-GPU NCCL | Для одной P106-100 не блокирует сборку |
| `ccache not found` | Нет компиляционного кеша | Не ошибка, можно игнорировать |
| В CMake `CUDA Version 13.0` из `nvidia-smi` | Это возможность драйвера, не версия Toolkit | Использовать `nvcc --version`; подтверждена 12.4.131 |
| Ввод shell-команды «сливается» с соседними строками | Терминал/копирование вставляет текст некорректно | Вставлять отдельно небольшие команды; ориентироваться на фактически распечатанную `Command being timed` |
| Модель Qwen3-8B сначала загружается ~26,6 с | Файловый кеш холодный, 1311 major faults / большие file inputs | Не считать ошибкой CUDA, повторить warm-cache если сравниваются задержки |
| `nvidia-smi` после завершения GPU-теста показывает 0 MiB | Процесс освободил VRAM при завершении | Снимать максимум **во время** прогона, например CSV-мониторинг |
| `Fan 0%` | Не измеряет два внешних вентилятора | Физическая проверка обдува |

## 10. Особенности сопоставления производительности и качества

**Что действительно идентично:** GGUF SHA трёх Qwen, llama.cpp исходный commit, системный CLEAN prompt и RAW-кейсы, максимальный контекст CLEAN, число потоков, decoding-опции, one-shot свежий `llama-cli`.

**Что отличается:** исторический GCC 15.2 против нового GCC 13.4; CPU OpenBLAS и CUDA backends; новое расположение дисковых данных; `-ngl 99` только CUDA; при CPU `nice -n 10` применялся лишь в новом **отдельном** `llama-bench` для Qwen3-4B; случайность ответов при `--temp 0.7`; в отдельных smoke разный холодный/тёплый page cache.

- Производительность `llama-bench pp512 / tg128` сравнивается **только с тем же типом теста**. Нельзя считать 660 pp512 ускорением 660/15,3 в стандартном бенче — 15,3 относится к другому CLEAN сценарному запуску.
- `/usr/bin/time -v Maximum resident set size` — **RAM процесса**, а `nvidia-smi memory.used` — VRAM платы. Их значения не заменяют друг друга.
- В строке `CUDA ngl 99` число **запрошенных GPU-слоёв**, а не прямое доказательство, сколько слоёв было реально перенесено: это надо проверять `--verbose`, диагностическими логами loader, а также памятью `nvidia-smi`.
- При температуре >0 результат RAW→CLEAN может быть не полностью детерминирован. Результаты записаны буквально, но нельзя утверждать, что «GPU улучшил» или «ухудшил» языковое качество сам по себе.
- Скорость `tg128` для Qwen3-4B GPU 38,19 tok/s, CLEAN throughput ~32,2–32,3 tok/s — допустимая разница разных режимов и контекстов, не ошибка отчёта.
- Повторения `-r 3` / `-r 20` показывают устойчивость среднего throughput на конкретном коротком `llama-bench`, **не** заменяют длительный continuous stress VRAM/VRM.

## 11. Рекомендации для будущих прогонов и сохранения доказательств

Перед новым раундом выполнить read-only инвентаризацию:

```bash
date -Is
uname -a
nvidia-smi --query-gpu=name,driver_version,temperature.gpu,power.limit,memory.total,memory.used --format=csv
free -h
df -h /srv/ai
sha256sum /srv/ai/models/text/*.gguf
/opt/llama.cpp/build-cpu/bin/llama-cli --version
/opt/llama.cpp/build-cuda-p106/bin/llama-cli --version
```

Затем:

1. Зафиксировать модель, SHA, commit, GPU PL, системный prompt SHA, `cases.json` SHA, драйвер, kernel, свободную RAM и фоновые задачи.
2. Для `llama-bench` запускать одинаковые `-p/-n/-r/-t` и логировать всю stdout/stderr, использовать несколько повторений; отдельно от CLEAN.
3. Для CLEAN брать точный RAW из JSON, отдельный процесс на кейс, не изменять frozen семплирование; сохранять сырой ответ, измерения, ручную оценку и hard fail.
4. Мониторить VRAM/GPU temperature/power **во время** работы, записать start/end времени бенчмарка и анализировать активные строки отдельно от idle.
5. Не добавлять private RAW или секреты в новый публичный репозиторий, а также не перемещать production файлы ради удобства GitHub.
6. Новые модели Gemma и прочие отмечать **«не тестировалась на GPU»**, пока не получены прямые выводы терминала. Если OOM — документировать offload и не приписывать результат полному `-ngl 99`.

Пример сохранения будущего **одного** CLI-прогона без изменения параметров модели (используется Bash, сохраняется exit с помощью `pipefail`):

```bash
mkdir -p "$HOME/llm-benchmark-logs"
set -o pipefail
/usr/bin/time -v /opt/llama.cpp/build-cuda-p106/bin/llama-cli \
  -m /srv/ai/models/text/Qwen3-8B-Q4_K_M.gguf \
  -ngl 99 -c 4096 -t 4 -tb 4 \
  --reasoning off -st \
  -sys "Ты выполняешь технический тест. Следуй инструкции пользователя точно и не добавляй пояснений." \
  -p "Ответь только одним словом: ГОТОВО" -n 16 --temp 0 \
  2>&1 | tee "$HOME/llm-benchmark-logs/qwen3-8b-smoke-$(date +%Y%m%d-%H%M%S).log"
echo "Pipeline exit: $?"
```

Этот пример создаёт новый лог в домашнем каталоге, не в `benchmarks/clean-v1` и не в production; при переносе в GitHub нужно проверить содержимое перед публикацией. Для воспроизводимого набора из 10 кейсов будущий скрипт должен добавлять поля `case_id`, `model_sha256`, `engine_commit`, `start/end`, `exit`, `seed` (если сравнение требует нового детерминированного протокола) и сырой stdout/stderr; **не менять замороженный оригинал**.

## 12. Где хранить, как загрузить на GitHub

Предлагаемая отдельная директория репозитория:

```text
llm-benchmarks/
├── LLM_COMPARATIVE_RESULTS.md
└── TEST_PROTOCOL_AND_ENVIRONMENT.md
```

Документация опубликована в приватном репозитории [`sl1mxaer/llm-benchmarks`](https://github.com/sl1mxaer/llm-benchmarks). В архив включены два Markdown-файла: этот воспроизводимый протокол и свод результатов `LLM_COMPARATIVE_RESULTS.md`. Последующие тесты должны добавляться с датой, конфигурацией оборудования, версиями ПО, оригинальными логами и явной пометкой о неподтверждённых параметрах.

Существующий производственный `sl1mxaer/llm-server-ai` остаётся источником исторических CPU-данных и эталонного `CLEAN v1`. Не смешивать новый документальный архив с кодом и работающими сервисами без отдельного согласования.

## 13. Первичные источники, полнота и честно обозначенные пробелы

- [CPU: Qwen3-4B](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/qwen3-4b-q4_k_m.md)
- [CPU: Qwen3.5-4B](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/qwen3.5-4b-q4_k_m.md)
- [CPU: Qwen3-8B + полный 10-кейсовый прогон](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/qwen3-8b-q4_k_m.md)
- [CPU: Gemma 4 12B + полный 10-кейсовый прогон](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/gemma-4-12b-it-qat-q4_0.md)
- [CPU: Ministral 3 3B](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/ministral-3-3b-instruct-2512-q4_k_m.md)
- [CPU: YandexGPT 5 Lite 8B](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/yandexgpt-5-lite-8b-instruct-q4_k_m.md)
- [Persistent `llama-server` сравнение Qwen3-8B/Gemma 4 12B от 02.10.2026](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/results/finalist-runtime-comparison-2026-10-02.md)
- [Freeze-протокол](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/quick-triage.md) и [рубрика](https://github.com/sl1mxaer/llm-server-ai/blob/main/benchmarks/clean-v1/rubric.md).

Источники GPU — предоставленные в переписке от 19.10.2026 фактические команды и логи терминала `llm-server`, собранные таблицы `llama-bench`, `time -v`, `nvidia-smi` и выходы SGEMM. **Новые `.md` составлены на основании этих данных, но не создают задним числом отсутствующий сырой файл логов, мониторинг VRAM Qwen3-8B или GPU-результаты Gemma.**