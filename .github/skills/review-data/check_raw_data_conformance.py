#!/usr/bin/env python3
"""Validate data/raw CSV files against naming, presence, and schema rules."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]


def load_rules(rules_path: Path) -> dict[str, Any]:
    with rules_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_required_files(csv_files: list[Path], required_patterns: list[str], errors: list[str]) -> None:
    file_names = [path.name for path in csv_files]
    for pattern in required_patterns:
        if not any(fnmatch(name, pattern) for name in file_names):
            errors.append(f"Missing required file pattern: {pattern}")


def check_filename(filename: str, filename_regex: str | None, errors: list[str]) -> None:
    if filename_regex and re.match(filename_regex, filename) is None:
        errors.append(
            f"{filename}: file name does not match regex '{filename_regex}'"
        )


def check_header(header: list[str], filename: str, errors: list[str]) -> None:
    if not header:
        errors.append(f"{filename}: missing header row")
        return

    cleaned = [column.strip() for column in header]
    if any(column == "" for column in cleaned):
        errors.append(f"{filename}: header contains empty column names")

    duplicates = sorted({column for column in cleaned if cleaned.count(column) > 1})
    if duplicates:
        errors.append(f"{filename}: duplicate header columns found: {duplicates}")


def check_required_columns(
    filename: str,
    header: list[str],
    schema_rules: list[dict[str, Any]],
    warnings: list[str],
    errors: list[str],
) -> None:
    matched = False
    for rule in schema_rules:
        pattern = rule.get("pattern", "")
        required_columns = rule.get("required_columns", [])
        if not fnmatch(filename, pattern):
            continue

        matched = True
        missing = [column for column in required_columns if column not in header]
        if missing:
            errors.append(
                f"{filename}: missing required columns for pattern '{pattern}': {missing}"
            )

    if not matched:
        warnings.append(f"{filename}: no schema rule matched this file")


def check_rows(
    filename: str,
    rows: list[list[str]],
    header_len: int,
    minimum_data_rows: int,
    forbid_blank_rows: bool,
    enforce_row_width: bool,
    errors: list[str],
) -> None:
    if len(rows) < minimum_data_rows:
        errors.append(
            f"{filename}: expected at least {minimum_data_rows} data rows, found {len(rows)}"
        )

    if forbid_blank_rows:
        blank_indices = [
            index + 2 for index, row in enumerate(rows) if all(cell.strip() == "" for cell in row)
        ]
        if blank_indices:
            errors.append(f"{filename}: blank rows found at CSV lines {blank_indices}")

    if enforce_row_width:
        bad_width_rows = [
            index + 2 for index, row in enumerate(rows) if len(row) != header_len
        ]
        if bad_width_rows:
            errors.append(
                f"{filename}: row width mismatch at CSV lines {bad_width_rows} (expected {header_len} columns)"
            )


def check_position_values(
    filename: str,
    header: list[str],
    rows: list[list[str]],
    position_rule: dict[str, Any],
    errors: list[str],
) -> None:
    position_columns = list(position_rule.get("columns", []))
    allowed_values = list(position_rule.get("allowed_values", []))
    if not position_columns or not allowed_values:
        return

    allowed_upper = {value.upper() for value in allowed_values}

    for column_name in position_columns:
        if column_name not in header:
            continue

        column_index = header.index(column_name)
        invalid_values: dict[str, list[int]] = {}

        for row_index, row in enumerate(rows, start=2):
            if column_index >= len(row):
                continue

            value = row[column_index].strip()
            if value.upper() in allowed_upper:
                continue

            invalid_values.setdefault(value, []).append(row_index)

        if invalid_values:
            details = ", ".join(
                f"'{value}' at lines {lines}"
                for value, lines in sorted(invalid_values.items(), key=lambda item: item[0])
            )
            errors.append(
                f"{filename}: column '{column_name}' has values outside allowed set {allowed_values}: {details}"
            )


def validate_file(
    file_path: Path,
    schema_rules: list[dict[str, Any]],
    position_rule: dict[str, Any],
    filename_regex: str | None,
    minimum_data_rows: int,
    forbid_blank_rows: bool,
    enforce_row_width: bool,
    errors: list[str],
    warnings: list[str],
) -> None:
    filename = file_path.name
    check_filename(filename, filename_regex, errors)

    if file_path.stat().st_size == 0:
        errors.append(f"{filename}: file is empty")
        return

    try:
        with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            all_rows = list(reader)
    except UnicodeDecodeError as exc:
        errors.append(f"{filename}: not valid UTF-8 CSV ({exc})")
        return
    except csv.Error as exc:
        errors.append(f"{filename}: CSV parsing error ({exc})")
        return

    if not all_rows:
        errors.append(f"{filename}: no rows found")
        return

    header = all_rows[0]
    rows = all_rows[1:]

    check_header(header, filename, errors)
    check_required_columns(filename, header, schema_rules, warnings, errors)
    check_rows(
        filename,
        rows,
        len(header),
        minimum_data_rows,
        forbid_blank_rows,
        enforce_row_width,
        errors,
    )
    check_position_values(
        filename=filename,
        header=header,
        rows=rows,
        position_rule=position_rule,
        errors=errors,
    )


def validate_data_dir(
    data_dir: Path,
    rules: dict[str, Any],
    target_file: Path | None = None,
) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if target_file is not None:
        csv_files = [target_file]
    else:
        data_glob = str(rules.get("data_glob", "*.csv"))
        csv_files = sorted(path for path in data_dir.glob(data_glob) if path.is_file())

    if not csv_files:
        data_glob = str(rules.get("data_glob", "*.csv"))
        return ValidationResult(errors=[f"No files matched '{data_glob}' in {data_dir}"], warnings=[])

    if target_file is None:
        required_patterns = list(rules.get("required_file_patterns", []))
        check_required_files(csv_files, required_patterns, errors)

    schema_rules = list(rules.get("schema_rules", []))
    position_rule = dict(rules.get("position_rule", {}))
    checks = dict(rules.get("checks", {}))
    minimum_data_rows = int(checks.get("minimum_data_rows", 1))
    forbid_blank_rows = bool(checks.get("forbid_blank_rows", True))
    enforce_row_width = bool(checks.get("enforce_row_width", True))
    filename_regex = rules.get("filename_regex")
    filename_regex = str(filename_regex) if filename_regex else None

    for file_path in csv_files:
        validate_file(
            file_path=file_path,
            schema_rules=schema_rules,
            position_rule=position_rule,
            filename_regex=filename_regex,
            minimum_data_rows=minimum_data_rows,
            forbid_blank_rows=forbid_blank_rows,
            enforce_row_width=enforce_row_width,
            errors=errors,
            warnings=warnings,
        )

    return ValidationResult(errors=errors, warnings=warnings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Review conformance of data/raw CSV files against rules."
    )
    repo_root = Path(__file__).resolve().parents[3]
    default_data_dir = repo_root / "data" / "raw"
    default_rules_path = Path(__file__).resolve().with_name("rules.json")

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=default_data_dir,
        help=f"Directory containing raw CSV files (default: {default_data_dir})",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=default_rules_path,
        help=f"Path to rules JSON (default: {default_rules_path})",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help="Optional single CSV file to validate. Must be inside --data-dir.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    data_dir: Path = args.data_dir
    rules_path: Path = args.rules
    target_file: Path | None = args.file

    data_dir = data_dir.resolve()

    if target_file is not None:
        target_file = target_file.resolve()

    if not data_dir.exists() or not data_dir.is_dir():
        print(f"ERROR: data directory not found: {data_dir}")
        return 2

    if not rules_path.exists() or not rules_path.is_file():
        print(f"ERROR: rules file not found: {rules_path}")
        return 2

    if target_file is not None:
        if not target_file.exists() or not target_file.is_file():
            print(f"ERROR: file not found: {target_file}")
            return 2
        if target_file.suffix.lower() != ".csv":
            print(f"ERROR: expected a .csv file, got: {target_file}")
            return 2
        try:
            target_file.relative_to(data_dir)
        except ValueError:
            print(f"ERROR: file must be under data directory {data_dir}: {target_file}")
            return 2

    rules = load_rules(rules_path)
    result = validate_data_dir(data_dir, rules, target_file=target_file)

    print(f"Checked directory: {data_dir}")
    if target_file is not None:
        print(f"Checked file: {target_file}")
    print(f"Using rules file: {rules_path}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f" - {warning}")

    if result.errors:
        print("\nConformance check FAILED with the following issues:")
        for issue in result.errors:
            print(f" - {issue}")
        return 1

    print("\nConformance check PASSED. All files match the configured rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
