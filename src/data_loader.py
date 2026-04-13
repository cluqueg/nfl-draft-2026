"""
Utility functions for loading and validating NFL Draft CSV data.
"""

import pandas as pd
from pathlib import Path

DATA_RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
DATA_PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"


def load_csv(filename: str, directory: Path = DATA_RAW_DIR) -> pd.DataFrame:
    """Load a CSV file from the given directory into a DataFrame."""
    filepath = directory / filename
    return pd.read_csv(filepath)


def save_processed(df: pd.DataFrame, filename: str) -> None:
    """Save a processed DataFrame as a CSV to the processed data directory."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_PROCESSED_DIR / filename
    df.to_csv(filepath, index=False)
