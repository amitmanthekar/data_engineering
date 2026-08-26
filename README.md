# Python CSV/Excel to PostgreSQL ETL Pipeline

A small, interview-style batch ETL project. It will read customer/order data from CSV or Excel, validate and transform it in Python, then load it into PostgreSQL.

This repository is being built step by step. **Step 1 is the project skeleton only.** There is no ETL logic yet.

## Requirements

- Python 3.11 or newer (verified on this machine: Python 3.14)
- PostgreSQL (needed from Step 6 onward, not required for Step 1)
- An OpenAI or Azure OpenAI API key (needed from Step 10 onward, optional)

## Project layout

```
data/input/     # files you want the pipeline to process
data/sample/    # sample datasets (added in Step 2)
output/         # invalid records and quality reports
logs/           # pipeline.log (added in a later step)
src/            # Python package (ETL modules will live here)
tests/          # pytest tests (added in later steps)
.env.example    # placeholder for secrets (copy to .env; never commit .env)
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

## What comes next

- **Step 2:** generate sample CSV and Excel order files with some invalid rows
- Later steps: extract, validate, transform, load to PostgreSQL, quality report, optional AI summary, tests
