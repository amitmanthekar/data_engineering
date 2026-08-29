# Python CSV/Excel to PostgreSQL ETL Pipeline

A small, interview-style batch ETL project. It will read customer/order data from CSV or Excel, validate and transform it in Python, then load it into PostgreSQL.

This repository is being built step by step. **Steps 1–2 are complete.** There is still no ETL logic — only a runnable skeleton and sample input files.

## Requirements

- Python 3.11 or newer (verified on this machine: Python 3.14)
- PostgreSQL (needed from Step 6 onward, not required for Step 1)
- An OpenAI or Azure OpenAI API key (needed from Step 10 onward, optional)

## Project layout

```
data/input/                 # files you want the pipeline to process
data/sample/orders.csv      # sample orders (CSV)
data/sample/orders.xlsx     # same sample orders (Excel)
generate_sample_data.py     # script that recreates the sample files
output/                     # invalid records and quality reports
logs/                       # pipeline.log (added in a later step)
src/                        # Python package (ETL modules will live here)
tests/                      # pytest tests (added in later steps)
.env.example                # placeholder for secrets (copy to .env; never commit .env)
requirements.txt
pyproject.toml
```

## Setup (Windows PowerShell)

From the project root (`d:\AI\Test`):

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks script activation, run this once, then try Activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Copy the example environment file and fill in real values later (not needed for Step 1):

```powershell
Copy-Item .env.example .env
```

## Run the skeleton

```powershell
python -m src.main
```

Expected output:

```text
ETL pipeline skeleton is ready. No data processing yet.
```

## Sample data (Step 2)

The pipeline will later read customer orders. Both files have the same 2,500 rows and the same columns:

| Column | Meaning | Example |
|--------|---------|---------|
| `order_id` | Unique business key for an order | `10001` |
| `customer_id` | Customer key | `C001` |
| `customer_name` | Customer display name | `John Smith` |
| `customer_email` | Customer email | `john@example.com` |
| `order_date` | Order date (`YYYY-MM-DD` when valid) | `2026-08-01` |
| `product_id` | Product key | `P1001` |
| `product_name` | Product display name | `Laptop` |
| `quantity` | Units ordered | `2` |
| `unit_price` | Price per unit | `750.00` |
| `order_status` | Allowed later: `PENDING`, `COMPLETED`, `CANCELLED`, `RETURNED` | `COMPLETED` |
| `country` | Customer country | `USA` |

Most rows are valid. These issues were added on purpose so validation can be demonstrated later:

| Issue | Count |
|-------|------:|
| Missing `customer_email` | 35 |
| Missing `customer_id` | 10 |
| Invalid `order_date` | 8 |
| Negative `quantity` | 10 |
| Zero `quantity` | 5 |
| Negative `unit_price` | 4 |
| Missing `product_id` | 10 |
| Invalid `order_status` | 10 |
| Empty `customer_name` | 8 |
| Duplicate `order_id` values | 12 |

A few otherwise valid names also have extra spaces (for example `" John Smith "`) so a later transform step can trim them.

Regenerate the files:

```powershell
python generate_sample_data.py
```

Expected console output includes `Total records: 2500` and the issue counts above.

## What comes next

- **Step 3:** extract — read CSV/Excel into a pandas DataFrame
- Later steps: validate, transform, load to PostgreSQL, quality report, optional AI summary, tests
