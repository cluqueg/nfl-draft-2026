# nfl-draft-2026

[English](README.md) | [Español](README.es.md)

Data analysis project for the 2026 NFL Draft prospect pool.
Player data is ingested from CSV files, transformed, and explored in Jupyter notebooks.

## Project structure

```
nfl-draft-2026/
├── data/
│   ├── raw/                 # Source CSV files
│   └── processed/           # Derived CSV files used in analysis
├── notebooks/
│   ├── data_engineering/
│   │   └── my_big_board.ipynb
│   └── reports/
│       └── player_overview.ipynb
├── src/
│   ├── __init__.py
│   └── data_loader.py       # Reusable CSV loading/saving helpers
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting started

### 1. Install dependencies

Using uv (recommended):

```bash
uv sync
```

Using pip:

```bash
pip install -e .
```

### 2. Add or update input data

Put raw CSV files in `data/raw/`.

### 3. Run notebooks

From the project root:

```bash
jupyter lab
```

Suggested notebook flow:

1. `notebooks/data_engineering/my_big_board.ipynb` to clean and prepare draft board data.
2. `notebooks/reports/player_overview.ipynb` to generate summary tables and visualizations.
