"""Tests for the extract step only."""

from pathlib import Path

import pandas as pd
import pytest

from src.extract import extract_data

SAMPLE_CSV = Path("data/sample/orders.csv")
SAMPLE_XLSX = Path("data/sample/orders.xlsx")


def _write_tiny_orders(path: Path) -> pd.DataFrame:
    rows = pd.DataFrame(
        {
            "order_id": [10001, 10002],
            "customer_id": ["C001", "C002"],
            "customer_name": ["John Smith", "Priya Sharma"],
        }
    )
    if path.suffix.lower() == ".csv":
        rows.to_csv(path, index=False)
    else:
        rows.to_excel(path, index=False)
    return rows


def test_extract_csv_returns_dataframe(tmp_path: Path) -> None:
    path = tmp_path / "orders.csv"
    expected = _write_tiny_orders(path)

    result = extract_data(path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == list(expected.columns)
    assert result["order_id"].tolist() == [10001, 10002]


def test_extract_xlsx_returns_dataframe(tmp_path: Path) -> None:
    path = tmp_path / "orders.xlsx"
    _write_tiny_orders(path)

    result = extract_data(path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2


def test_extract_accepts_uppercase_extension(tmp_path: Path) -> None:
    path = tmp_path / "orders.CSV"
    _write_tiny_orders(path)

    result = extract_data(path)

    assert len(result) == 2


def test_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        extract_data(missing)


def test_unsupported_extension_raises_value_error(tmp_path: Path) -> None:
    path = tmp_path / "orders.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file extension"):
        extract_data(path)


def test_extract_sample_csv() -> None:
    result = extract_data(SAMPLE_CSV)

    assert len(result) == 2500
    assert "order_id" in result.columns


def test_extract_sample_xlsx() -> None:
    result = extract_data(SAMPLE_XLSX)

    assert len(result) == 2500
    assert list(result.columns) == list(pd.read_csv(SAMPLE_CSV).columns)
