"""Utility functions for loading and validating NFL Draft CSV data."""

from pathlib import Path

import pandas as pd

DATA_RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
DATA_PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
BRUGLER_FILE = "brugler-players.csv"

def load_csv(filename: str, directory: Path = DATA_RAW_DIR) -> pd.DataFrame:
    """Load a CSV file from the given directory into a DataFrame."""
    filepath = directory / filename
    return pd.read_csv(filepath)

def save_processed(df: pd.DataFrame, filename: str) -> None:
    """Save a processed DataFrame as a CSV to the processed data directory."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_PROCESSED_DIR / filename
    df.to_csv(filepath, index=False)

def list_brugler_files(directory: Path = DATA_RAW_DIR) -> list[Path]:
    """Return all Brugler CSV files in the raw data directory."""
    return sorted(directory.glob("brugler-*.csv"))

def save_brugler_data() -> None:
    """Load the original Brugler data, perform any necessary cleaning, and save it to the processed directory."""
    brugler_files = list_brugler_files()
    if not brugler_files:
        raise FileNotFoundError(f"No Brugler files found in {DATA_RAW_DIR}")

    df = pd.concat((pd.read_csv(file_path) for file_path in brugler_files), ignore_index=True)

    # Save the combined DataFrame to the processed directory
    save_processed(df, BRUGLER_FILE)
