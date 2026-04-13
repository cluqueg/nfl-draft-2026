# nfl-draft-2026

Data analysis project for the 2026 NFL Draft prospect pool.  
Player data is ingested as CSV files and analyzed using JupyterHub notebooks.

## Project structure

```
nfl-draft-2026/
├── data/
│   ├── raw/            # Raw CSV uploads (not tracked by git if large)
│   └── processed/      # Cleaned / transformed data ready for analysis
├── notebooks/
│   ├── data_engineering/
│   │   └── 01_data_ingestion.ipynb   # Load, clean and save raw CSV data
│   └── reports/
│       └── player_overview.ipynb     # Summary statistics and visualizations
├── src/
│   ├── __init__.py
│   └── data_loader.py  # Shared helpers for loading and saving data
├── requirements.txt    # Python dependencies
└── README.md
```

## Getting started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add player data

Place your raw CSV file(s) inside `data/raw/`.

### 3. Run notebooks

Open the project in JupyterHub or start JupyterLab locally from the project root:

```bash
jupyter lab
```

Run the notebooks in order:

1. `notebooks/data_engineering/01_data_ingestion.ipynb` — cleans the raw CSV and saves the result to `data/processed/`.
2. `notebooks/reports/player_overview.ipynb` — builds summary statistics and charts from the processed data.
