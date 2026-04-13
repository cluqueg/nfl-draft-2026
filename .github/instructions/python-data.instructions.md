---
description: "Use when editing Python data ingestion, CSV loading, cleaning, or analysis code in this NFL Draft project. Covers data path handling, DataFrame I/O, and notebook-to-src separation."
name: "Python Data Conventions"
applyTo: "src/**/*.py,notebooks/**/*.ipynb"
---
# Python Data Conventions

- Read input files from data/raw and write derived outputs to data/processed.
- Build file paths with pathlib.Path and project-relative constants. Avoid hardcoded absolute paths.
- Keep reusable data logic in src modules; notebooks should focus on orchestration, exploration, and charts.
- Add type hints and concise docstrings for shared helper functions in src.
- When exporting DataFrames to CSV for downstream notebooks, default to index=False unless an index column is explicitly required.
- Validate required columns before transformations and raise clear errors that list missing columns.
- Prefer the existing stack (pandas, numpy, matplotlib, seaborn, openpyxl) unless there is a strong need for a new dependency.
