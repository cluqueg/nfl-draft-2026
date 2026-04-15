---
name: review-data
description: "Use when reviewing data/raw CSV quality, validating raw file conformance, checking required columns, or running pre-ingestion data rules for this NFL Draft project."
argument-hint: "[file] Optional CSV file path under data/raw to review; omit to validate all raw files"
---

# Review Data

Use this skill to verify that `data/raw` files match expected file names, core schemas, and basic CSV quality constraints before ingestion.

## Usage

- Optional input: `file` (for example, `data/raw/brugler-qb.csv`).
- If `file` is omitted, the skill validates all matching CSVs in `data/raw`.
- If `file` is provided, the skill validates only that file against schema and CSV quality rules.

## What This Skill Checks

- Required raw file patterns are present.
- File names follow lowercase kebab-case plus `.csv`.
- Files are non-empty and valid UTF-8 CSV.
- Header row exists.
- Header has no empty or duplicate column names.
- Source-specific required columns are present.
- Position values in `POSITION`/`Position`/`Pos` are limited to the configured allowed set.
- Each file has at least one data row.
- No blank data rows.
- Every data row has the same column count as the header.

Rules are defined in `rules.json` and can be edited as the pipeline evolves.

## Run The Validation

From the repository root, run:

```bash
python3 .github/skills/review-data/check_raw_data_conformance.py
```

Optional overrides:

```bash
python3 .github/skills/review-data/check_raw_data_conformance.py \\
  --data-dir data/raw \
  --rules .github/skills/review-data/rules.json
```

Single-file review:

```bash
python3 .github/skills/review-data/check_raw_data_conformance.py \\
  --file data/raw/brugler-qb.csv
```

## Response Format

When reporting results:

1. Start with `PASSED` or `FAILED`.
2. If failed, list each violation grouped by file.
3. Suggest exact next edits (rename file, add missing column, fix malformed rows, etc.).
4. If passed, mention that files are ready for ingestion.
