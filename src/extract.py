"""Extract order data from a CSV or Excel file into a pandas DataFrame.

This module only reads files. It does not validate, transform, or load data.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from .logger import get_logger

SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}
logger = get_logger()


def extract_data(file_path: str | Path) -> pd.DataFrame:
    """Read a CSV or XLSX file and return its rows as a DataFrame.

    Detection is based on the file extension, not the file contents.

    Raises:
        FileNotFoundError: The path does not exist.
        ValueError: The extension is not .csv or .xlsx.
    """
    path = Path(file_path)

    if not path.exists():
        message = f"Input file does not exist: {path}"
        logger.error(message)
        raise FileNotFoundError(message)

    if not path.is_file():
        message = f"Input path is not a file: {path}"
        logger.error(message)
        raise FileNotFoundError(message)

    extension = path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        message = (
            f"Unsupported file extension '{path.suffix}'. "
            "Use .csv or .xlsx."
        )
        logger.error(message)
        raise ValueError(message)

    logger.info("Reading file: %s", path)

    if extension == ".csv":
        dataframe = pd.read_csv(path)
    else:
        dataframe = pd.read_excel(path)

    logger.info("Extracted %s records", len(dataframe))
    return dataframe


def main(argv: list[str] | None = None) -> int:
    """Allow `python -m src.extract <file>` during Step 3."""
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        logger.error("Usage: python -m src.extract <path-to-csv-or-xlsx>")
        return 1

    try:
        extract_data(args[0])
    except (FileNotFoundError, ValueError):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
