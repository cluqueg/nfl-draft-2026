# nfl-draft-2026

[English](README.md) | [Español](README.es.md)

Proyecto de analisis de datos sobre jugadores que se presentan al Draft de NFL en 2026.
Los datos de jugadores se cargan desde archivos CSV, se transforman y se exploran en notebooks de Jupyter.

## Estructura del proyecto

```
nfl-draft-2026/
├── data/
│   ├── raw/                 # Archivos CSV fuente
│   └── processed/           # CSV derivados para analisis
├── notebooks/
│   ├── data_engineering/
│   │   └── my_big_board.ipynb
│   └── reports/
│       └── player_overview.ipynb
├── src/
│   ├── __init__.py
│   └── data_loader.py       # Utilidades reutilizables para carga/guardado de CSV
├── pyproject.toml
├── uv.lock
└── README.md
```

## Primeros pasos

### 1. Instalar dependencias

Con uv (recomendado):

```bash
uv sync
```

Con pip:

```bash
pip install -e .
```

### 2. Agregar o actualizar datos de entrada

Coloca los archivos CSV crudos en `data/raw/`.

### 3. Ejecutar notebooks

Desde la raiz del proyecto:

```bash
jupyter lab
```

Flujo sugerido de notebooks:

1. `notebooks/data_engineering/my_big_board.ipynb` para limpiar y preparar datos del draft board.
2. `notebooks/reports/player_overview.ipynb` para generar tablas de resumen y visualizaciones.
