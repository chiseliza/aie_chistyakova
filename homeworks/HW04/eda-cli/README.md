# S03 – eda_cli: мини-EDA для CSV

Небольшое CLI-приложение для базового анализа CSV-файлов.
Используется в рамках Семинара 03 курса «Инженерия ИИ».

## Требования

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) установлен в систему

## Инициализация проекта

В корне проекта (S03):

```bash
uv sync
```

Эта команда:

- создаст виртуальное окружение `.venv`;
- установит зависимости из `pyproject.toml`;
- установит сам проект `eda-cli` в окружение.

## Запуск CLI

### Краткий обзор

```bash
uv run eda-cli overview data/example.csv
```

Параметры:

- `--sep` – разделитель (по умолчанию `,`);
- `--encoding` – кодировка (по умолчанию `utf-8`).

### Полный EDA-отчёт

```bash
uv run eda-cli report data/example.csv --out-dir reports
```

В результате в каталоге `reports/` появятся:

- `report.md` – основной отчёт в Markdown;
- `summary.csv` – таблица по колонкам;
- `missing.csv` – пропуски по колонкам;
- `correlation.csv` – корреляционная матрица (если есть числовые признаки);
- `top_categories/*.csv` – top-k категорий по строковым признакам;
- `hist_*.png` – гистограммы числовых колонок;
- `missing_matrix.png` – визуализация пропусков;
- `correlation_heatmap.png` – тепловая карта корреляций.


--title - заголовок отчёта 

--top-k-categories - сколько top-значений показывать для категорий



## Тесты

```bash
uv run pytest -q
```

## HTTP-сервис
### Запуск 
```bash
uv run uvicorn eda_cli.api:app --reload --port 8000
```
Параметры: 
- --reload - перезапуск сервера при обновлении кола
- --port - порт сервиса

## Эндпоинт POST /quality-flags-from-csv

- принимает CSV-файл;
- использует EDA-ядро (summarize_dataset, missing_table, compute_quality_flags);
- возвращает набор флагов качества;
- корректно обрабатывает ошибки чтения и пустой CSV (код 400).

