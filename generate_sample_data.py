"""Generate synthetic customer-order files for the ETL project.

This is NOT part of the ETL pipeline. It only creates sample input so we
can later test extract, validate, transform, and load.

Run from the project root:

    python generate_sample_data.py

Outputs:

    data/sample/orders.csv
    data/sample/orders.xlsx
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

N_RECORDS = 2500
OUTPUT_DIR = Path("data") / "sample"

COLUMNS = [
    "order_id",
    "customer_id",
    "customer_name",
    "customer_email",
    "order_date",
    "product_id",
    "product_name",
    "quantity",
    "unit_price",
    "order_status",
    "country",
]

CUSTOMERS = [
    ("C001", "John Smith", "john@example.com"),
    ("C002", "Priya Sharma", "priya.sharma@example.com"),
    ("C003", "Carlos Rivera", "carlos.rivera@example.com"),
    ("C004", "Amina Hassan", "amina.hassan@example.com"),
    ("C005", "Wei Chen", "wei.chen@example.com"),
    ("C006", "Emma Wilson", "emma.wilson@example.com"),
    ("C007", "Noah Patel", "noah.patel@example.com"),
    ("C008", "Sofia Rossi", "sofia.rossi@example.com"),
    ("C009", "Liam O'Brien", "liam.obrien@example.com"),
    ("C010", "Yuki Tanaka", "yuki.tanaka@example.com"),
    ("C011", "Maria Santos", "maria.santos@example.com"),
    ("C012", "Omar Farouk", "omar.farouk@example.com"),
]

PRODUCTS = [
    ("P1001", "Laptop", 750.00),
    ("P1002", "Wireless Mouse", 25.50),
    ("P1003", "USB-C Hub", 39.99),
    ("P1004", "Monitor", 220.00),
    ("P1005", "Keyboard", 45.00),
    ("P1006", "Webcam", 59.99),
    ("P1007", "Headphones", 89.00),
    ("P1008", "Desk Chair", 175.00),
]

COUNTRIES = ["USA", "India", "UK", "Germany", "Canada", "Australia", "Japan", "Brazil"]
STATUSES = ["PENDING", "COMPLETED", "CANCELLED", "RETURNED"]

# Disjoint row groups so each quality problem can be counted on its own.
ISSUE_SLICES = {
    "missing_email": slice(2400, 2435),       # 35 rows
    "missing_customer_id": slice(2435, 2445),  # 10 rows
    "invalid_date": slice(2445, 2453),         # 8 rows
    "negative_quantity": slice(2453, 2463),    # 10 rows
    "zero_quantity": slice(2463, 2468),        # 5 rows
    "negative_price": slice(2468, 2472),       # 4 rows
    "missing_product_id": slice(2472, 2482),   # 10 rows
    "invalid_status": slice(2482, 2492),       # 10 rows
    "empty_name": slice(2492, 2500),           # 8 rows
}

DUPLICATE_SOURCE_START = 0
DUPLICATE_TARGET_START = 100
N_DUPLICATES = 12

INVALID_DATES = [
    "2026-13-40",
    "not-a-date",
    "32/01/2026",
    "2026/99/01",
    "Jan 40 2026",
    "0000-00-00",
    "2026-02-30",
    "99-99-9999",
]

INVALID_STATUSES = [
    "SHIPPED",
    "DONE",
    "complete",
    "UNKNOWN",
    "IN_PROGRESS",
    "OPEN",
    "CLOSED",
    "FAILED",
    "HOLD",
    "PROCESSING",
]


def build_clean_rows() -> list[dict]:
    """Build 2500 realistic, valid order rows."""
    start_date = date(2026, 1, 1)
    rows: list[dict] = []

    for i in range(N_RECORDS):
        customer_id, customer_name, customer_email = CUSTOMERS[i % len(CUSTOMERS)]
        product_id, product_name, list_price = PRODUCTS[i % len(PRODUCTS)]
        order_date = start_date + timedelta(days=i % 200)
        quantity = (i % 5) + 1
        unit_price = round(list_price + (i % 3) * 0.5, 2)

        rows.append(
            {
                "order_id": 10001 + i,
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "order_date": order_date.isoformat(),
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "order_status": STATUSES[i % len(STATUSES)],
                "country": COUNTRIES[i % len(COUNTRIES)],
            }
        )

    return rows


def inject_quality_issues(rows: list[dict]) -> None:
    """Corrupt known row groups so validation can be demonstrated later."""
    for row in rows[ISSUE_SLICES["missing_email"]]:
        row["customer_email"] = ""

    for row in rows[ISSUE_SLICES["missing_customer_id"]]:
        row["customer_id"] = ""

    for index, row in enumerate(rows[ISSUE_SLICES["invalid_date"]]):
        row["order_date"] = INVALID_DATES[index]

    for row in rows[ISSUE_SLICES["negative_quantity"]]:
        row["quantity"] = -3

    for row in rows[ISSUE_SLICES["zero_quantity"]]:
        row["quantity"] = 0

    for row in rows[ISSUE_SLICES["negative_price"]]:
        row["unit_price"] = -12.50

    for row in rows[ISSUE_SLICES["missing_product_id"]]:
        row["product_id"] = ""

    for index, row in enumerate(rows[ISSUE_SLICES["invalid_status"]]):
        row["order_status"] = INVALID_STATUSES[index]

    for row in rows[ISSUE_SLICES["empty_name"]]:
        row["customer_name"] = ""

    for offset in range(N_DUPLICATES):
        source_order_id = rows[DUPLICATE_SOURCE_START + offset]["order_id"]
        rows[DUPLICATE_TARGET_START + offset]["order_id"] = source_order_id

    # A few valid rows with extra whitespace so Step 5 can demonstrate trimming.
    for offset in range(5):
        rows[200 + offset]["customer_name"] = f" {rows[200 + offset]['customer_name']} "


def summarize(df: pd.DataFrame) -> None:
    """Print issue counts so we can inspect the files without opening Excel."""
    print(f"Total records: {len(df)}")
    print(f"Missing customer_email: {(df['customer_email'] == '').sum()}")
    print(f"Missing customer_id: {(df['customer_id'] == '').sum()}")
    print(f"Empty customer_name: {(df['customer_name'] == '').sum()}")
    print(f"Missing product_id: {(df['product_id'] == '').sum()}")
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    print(f"Invalid order_date: {parsed_dates.isna().sum()}")
    print(f"Negative quantity: {(df['quantity'] < 0).sum()}")
    print(f"Zero quantity: {(df['quantity'] == 0).sum()}")
    print(f"Negative unit_price: {(df['unit_price'] < 0).sum()}")
    print(f"Invalid order_status: {(~df['order_status'].isin(STATUSES)).sum()}")
    print(f"Duplicate order_id values: {df['order_id'].duplicated().sum()}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = build_clean_rows()
    inject_quality_issues(rows)
    df = pd.DataFrame(rows, columns=COLUMNS)

    csv_path = OUTPUT_DIR / "orders.csv"
    xlsx_path = OUTPUT_DIR / "orders.xlsx"
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)

    print(f"Wrote {csv_path}")
    print(f"Wrote {xlsx_path}")
    summarize(df)


if __name__ == "__main__":
    main()
