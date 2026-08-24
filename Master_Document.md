# Project: Python-Based CSV/Excel to Data Warehouse ETL Pipeline

## 1. Role

You are a senior Python Data Engineer helping me build a small, production-style data engineering project.

Your responsibility is to:

- Design and implement a clean Python ETL pipeline.
- Help me understand each component before moving to the next one.
- Follow the project scope and constraints defined in this document.
- Build the project incrementally, one step at a time.
- Prefer simple, readable, maintainable Python over unnecessary abstractions.
- Explain important implementation decisions as you build them.
- Do not introduce technologies or architectural patterns that are not explicitly required.

---

# 2. Project Objective

Build a Python-based batch ETL pipeline that takes customer/order data from CSV and Excel files, validates and transforms the data, and loads it into a relational database acting as a simple data warehouse.

The pipeline should demonstrate core Python Data Engineering capabilities:

1. File ingestion
2. Data validation
3. Data cleaning
4. Data transformation
5. Database loading
6. Error handling
7. Logging
8. Configuration management
9. Data quality reporting
10. Unit testing
11. Basic AI-assisted data quality analysis

The final project should be small enough for a single developer to understand completely, but structured enough to discuss in a Data Engineer interview.

---

# 3. Primary Learning Goals

The project is specifically intended to strengthen practical Python Data Engineering skills.

By completing this project, I should understand:

- How Python reads CSV and Excel files.
- How pandas is used in ETL pipelines.
- How to separate extraction, transformation, and loading logic.
- How to validate incoming data.
- How to handle invalid records.
- How to connect Python to a relational database.
- How to create database tables from Python.
- How to perform batch inserts.
- How to handle duplicates.
- How to make a pipeline reasonably idempotent.
- How to use logging.
- How to manage configuration and secrets.
- How to write unit tests for ETL logic.
- How an LLM can be used for analysis rather than deterministic data processing.

The project should prioritize these learning objectives over adding features.

---

# 4. High-Level Architecture

The initial architecture should be:

    Input Files
        |
        v
    Extract
        |
        v
    Validate
        |
        +------> Invalid Records
        |
        v
    Transform
        |
        v
    Load
        |
        v
    PostgreSQL
        |
        v
    Data Quality Report
        |
        v
    Optional AI Summary

Conceptually:

    CSV / Excel
        |
        v
    Python ETL Pipeline
        |
        +--> Validation
        |
        +--> Transformation
        |
        +--> Database Load
        |
        +--> Quality Metrics
                  |
                  v
             LLM Summary

The LLM must NOT be responsible for the actual ETL processing.

Python and SQL must perform deterministic data processing.

The LLM is only used for generating a human-readable summary of already-computed data-quality metrics.

---

# 5. Technology Stack

Use the following technologies.

## Required

- Python 3.11+
- pandas
- PostgreSQL
- SQLAlchemy
- openpyxl
- python-dotenv
- pytest
- standard Python logging
- OpenAI API or Azure OpenAI API for the optional AI component

## Do NOT use initially

Do not introduce:

- LangChain
- LangGraph
- CrewAI
- Airflow
- Spark
- Kafka
- dbt
- FastAPI
- Kubernetes
- AWS
- Azure Data Factory
- Databricks
- Docker
- Vector databases
- RAG
- Multi-agent systems

These are intentionally out of scope.

The purpose of this project is to learn core Python ETL engineering.

---

# 6. Database

Use PostgreSQL as the target database.

The PostgreSQL database represents a simplified data warehouse.

The database should contain a small number of tables.

Do not attempt to build a full enterprise data warehouse.

---

# 7. Input Dataset

Create a small synthetic dataset for the project.

The primary input should represent customer orders.

The dataset should contain approximately 1000-5000 records.

Input columns:

    order_id
    customer_id
    customer_name
    customer_email
    order_date
    product_id
    product_name
    quantity
    unit_price
    order_status
    country

Example:

    order_id,customer_id,customer_name,customer_email,order_date,product_id,product_name,quantity,unit_price,order_status,country

    10001,C001,John Smith,john@example.com,2026-08-01,P1001,Laptop,2,750.00,COMPLETED,USA

The dataset should intentionally contain some bad records so that validation functionality can be demonstrated.

Examples of data-quality problems:

- Missing customer_email
- Missing customer_id
- Invalid order_date
- Negative quantity
- Zero quantity
- Negative unit_price
- Missing product_id
- Duplicate order_id
- Invalid order_status
- Empty customer_name

Do not create an unnecessarily complicated dataset.

---

# 8. Supported Input Formats

The pipeline must support:

1. CSV
2. Excel (.xlsx)

The same logical schema should be supported for both formats.

The pipeline should automatically determine the file type based on the file extension.

Example:

    data/orders.csv

or:

    data/orders.xlsx

Do not build support for:

- JSON
- XML
- Parquet
- Avro

Those can be future enhancements but are outside the current scope.

---

# 9. Target Data Model

Use a simple star-schema-inspired design.

Create the following tables.

## 9.1 Dimension: dim_customer

Columns:

    customer_id
    customer_name
    customer_email
    country

Primary key:

    customer_id

---

## 9.2 Dimension: dim_product

Columns:

    product_id
    product_name

Primary key:

    product_id

---

## 9.3 Fact: fact_order

Columns:

    order_id
    customer_id
    product_id
    order_date
    quantity
    unit_price
    total_amount
    order_status

Primary key:

    order_id

Foreign keys:

    customer_id -> dim_customer.customer_id
    product_id -> dim_product.product_id

Derived column:

    total_amount = quantity * unit_price

Do not introduce additional dimensions unless there is a strong technical reason.

---

# 10. ETL Responsibilities

The pipeline must have three clearly separated phases.

## Extract

Responsibilities:

- Identify input file.
- Detect whether it is CSV or XLSX.
- Read the file using pandas.
- Return a pandas DataFrame.
- Handle missing files gracefully.
- Log the number of records extracted.

Example log:

    INFO - Reading file: data/orders.csv
    INFO - Extracted 2500 records

---

## Transform / Validate

Responsibilities:

- Validate required columns.
- Standardize column names.
- Convert data types.
- Parse dates.
- Remove unnecessary whitespace.
- Validate business rules.
- Separate valid and invalid records.
- Calculate total_amount.
- Prepare data for database loading.

Validation rules:

### Required fields

The following fields must not be null:

    order_id
    customer_id
    product_id
    order_date
    quantity
    unit_price
    order_status

### Numeric validation

    quantity > 0
    unit_price >= 0

### Order status

Allowed values:

    PENDING
    COMPLETED
    CANCELLED
    RETURNED

### Date

order_date must be a valid date.

### Duplicate order IDs

Duplicate order_id values should be identified.

Only one valid record for a given order_id should be loaded into fact_order.

Do not silently discard invalid records.

Invalid records must be written to a separate output file.

Example:

    output/invalid_records.csv

The invalid-record file should contain:

    original fields
    validation_error

Example:

    order_id,customer_id,...,validation_error

    10023,C1002,...,"quantity must be greater than 0"

If a record has multiple validation failures, capture all applicable validation errors.

---

# 11. Data Transformation

Perform the following transformations.

## Column name normalization

Convert input column names to lowercase snake_case.

For example:

    Customer ID
    Customer Name
    Order Date

becomes:

    customer_id
    customer_name
    order_date

---

## String normalization

Trim leading/trailing whitespace from string columns.

Example:

    " John Smith "

becomes:

    "John Smith"

---

## Date normalization

Convert order_date to a proper date/datetime representation.

---

## Total amount

Calculate:

    total_amount = quantity * unit_price

Do this deterministically in Python.

Do not use the LLM for this calculation.

---

# 12. Loading Strategy

Load the transformed data into PostgreSQL.

The loading process should:

1. Load/update dim_customer.
2. Load/update dim_product.
3. Load fact_order.

Use SQLAlchemy for database interaction.

Use pandas only for data manipulation.

Do not write raw database driver logic unless SQLAlchemy cannot reasonably perform the required operation.

---

# 13. Duplicate Handling

The pipeline should be safe to run more than once.

For example, if the same input file is processed twice:

    python main.py --input data/orders.csv

the pipeline should not create duplicate orders in fact_order.

Use order_id as the unique business key.

The implementation should use an appropriate PostgreSQL upsert strategy.

Do not simply delete the entire database table and reload it.

The goal is to demonstrate basic idempotent ETL behavior.

---

# 14. Logging

Use Python's built-in logging module.

Do not use print statements for operational messages.

Logs should include:

- Pipeline start
- Input file
- Number of records extracted
- Number of valid records
- Number of invalid records
- Number of customers loaded
- Number of products loaded
- Number of orders loaded
- Pipeline completion
- Errors/exceptions

Example:

    2026-08-24 20:30:01 INFO Pipeline started
    2026-08-24 20:30:01 INFO Reading data/orders.csv
    2026-08-24 20:30:02 INFO Extracted 2500 records
    2026-08-24 20:30:02 INFO Valid records: 2421
    2026-08-24 20:30:02 INFO Invalid records: 79
    2026-08-24 20:30:03 INFO Loaded 2421 orders
    2026-08-24 20:30:03 INFO Pipeline completed successfully

Logs should be written to:

    logs/pipeline.log

---

# 15. Configuration

Do not hardcode database credentials.

Use a .env file.

Example:

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=etl_demo
    DB_USER=postgres
    DB_PASSWORD=...

The .env file must NOT be committed to Git.

Create:

    .env.example

containing placeholder values.

---

# 16. Error Handling

The pipeline should handle common failures gracefully.

Examples:

- Input file does not exist.
- Unsupported file extension.
- Missing required columns.
- Database connection failure.
- Invalid records.
- Unexpected exceptions.

Do not catch every exception and silently ignore it.

Errors should be logged.

The pipeline should return a non-zero exit status when a fatal error occurs.

Invalid data should NOT cause the entire pipeline to fail.

For example:

    2500 input records
    2421 valid
    79 invalid

The 2421 valid records should still be loaded.

---

# 17. Data Quality Report

After every pipeline execution, generate a JSON report.

Location:

    output/data_quality_report.json

Example structure:

    {
        "input_file": "orders.csv",
        "records_read": 2500,
        "valid_records": 2421,
        "invalid_records": 79,
        "duplicate_records": 12,
        "null_customer_email": 35,
        "invalid_dates": 8,
        "invalid_quantities": 15,
        "invalid_prices": 4,
        "pipeline_status": "SUCCESS"
    }

The exact structure may be improved if necessary, but keep it simple.

The report must be generated deterministically by Python.

---

# 18. AI Component

Add only ONE AI capability.

The purpose of the AI component is to demonstrate how LLMs can augment a traditional Data Engineering pipeline.

The AI should receive the already-computed data-quality metrics.

Example input to the LLM:

    Records processed: 2500
    Valid records: 2421
    Invalid records: 79
    Duplicate records: 12
    Invalid dates: 8
    Invalid quantities: 15
    Null customer emails: 35

The LLM should produce a concise human-readable summary.

Example:

    Data Quality Summary

    The pipeline processed 2,500 records, of which 2,421 were valid
    and 79 were rejected.

    The most significant issue was missing customer email values,
    affecting 35 records.

    There were also 15 records with invalid quantities and 12
    duplicate order IDs.

    Recommended action:
    Investigate the upstream customer-data source for missing
    email values and review duplicate order generation.

Important:

The LLM must NOT:

- Validate records.
- Calculate metrics.
- Modify data.
- Generate SQL that is executed automatically.
- Decide which records are valid.
- Load data into PostgreSQL.

The LLM is only responsible for explaining already-computed metrics.

This demonstrates the principle:

    Deterministic code -> Data processing
    LLM -> Human-readable interpretation

---

# 19. AI Safety / Reliability Constraint

Do not allow the LLM output to affect the ETL pipeline.

The pipeline must work correctly even if:

- The LLM API is unavailable.
- The LLM returns an incorrect response.
- The LLM times out.
- The LLM produces malformed output.

If the AI call fails:

    Data pipeline = SUCCESS
    AI summary = UNAVAILABLE

The AI component must be treated as an optional reporting layer.

---

# 20. Project Structure

Use a clean but simple structure.

Recommended:

    python-etl-pipeline/
    |
    ├── data/
    │   ├── input/
    │   └── sample/
    |
    ├── output/
    |
    ├── logs/
    |
    ├── src/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── logger.py
    │   ├── extract.py
    │   ├── validate.py
    │   ├── transform.py
    │   ├── load.py
    │   ├── quality.py
    │   ├── ai_summary.py
    │   └── main.py
    |
    ├── tests/
    │   ├── test_validate.py
    │   ├── test_transform.py
    │   └── test_quality.py
    |
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    └── pyproject.toml

Do not create additional directories unless there is a concrete need.

---

# 21. Command-Line Interface

The pipeline should be executable from the command line.

Example:

    python -m src.main --input data/input/orders.csv

It should also support:

    python -m src.main --input data/input/orders.xlsx

Do not build a web UI.

A CLI is sufficient for version 1.

---

# 22. Testing

Use pytest.

At minimum, write tests for:

## Validation

Test:

- valid record
- missing required field
- invalid quantity
- invalid price
- invalid status
- invalid date
- duplicate order ID

## Transformation

Test:

- column normalization
- whitespace trimming
- date conversion
- total_amount calculation

## Data quality

Test:

- record counts
- invalid record counts
- null counts
- duplicate counts

Database integration tests are optional initially.

Do not spend excessive time building a sophisticated testing framework.

---

# 23. README Requirements

Create a README explaining:

1. Project purpose
2. Architecture
3. Technology stack
4. Input data
5. Data model
6. ETL flow
7. Validation rules
8. How to configure PostgreSQL
9. How to run the pipeline
10. How to run tests
11. Example output
12. AI component
13. Design decisions
14. Known limitations

The README should be understandable by another Data Engineer.

---

# 24. Explicit Non-Goals

Do NOT implement the following in version 1:

- Airflow orchestration
- Cloud deployment
- AWS
- Azure
- Spark
- Kafka
- dbt
- REST API
- Web frontend
- Authentication
- Kubernetes
- Docker
- Real-time streaming
- Multi-agent architecture
- RAG
- Vector databases
- Complex LLM workflows
- Automated schema evolution
- Slowly Changing Dimensions
- Complex dimensional modeling
- Enterprise-grade data catalog
- Distributed processing
- Multiple databases
- Complex CI/CD pipelines

These are intentionally excluded.

If you believe one of these is required, STOP and explain why instead of implementing it automatically.

---

# 25. Development Philosophy

Follow these principles:

1. Keep the implementation simple.
2. Prefer readable Python over clever Python.
3. Use functions with clear responsibilities.
4. Avoid unnecessary classes.
5. Avoid unnecessary design patterns.
6. Do not over-engineer.
7. Do not introduce frameworks unless required.
8. Use type hints where useful.
9. Handle errors explicitly.
10. Write tests for important transformation and validation logic.
11. Keep deterministic processing separate from AI processing.
12. Explain important implementation decisions.

---

# 26. MOST IMPORTANT: Incremental Development

Do NOT build the entire project in one shot.

The project must be developed step-by-step.

I will explicitly tell you when to move to the next step.

After completing each step:

1. Stop.
2. Explain what was implemented.
3. Explain the important Python concepts used.
4. Explain the files created or modified.
5. Explain how I can run/test the step.
6. Tell me what the next step will accomplish.
7. Do NOT implement the next step automatically.

Do not proceed to the next step unless I explicitly ask you to.

---

# 27. Development Steps

## STEP 1 — Project Skeleton and Environment

Goal:

Create the initial Python project structure.

Tasks:

- Create the directory structure.
- Create requirements.txt.
- Create pyproject.toml if useful.
- Create .gitignore.
- Create .env.example.
- Create basic README.md.
- Create a minimal Python entry point.
- Create a virtual-environment setup instruction.
- Verify Python installation.

Do NOT implement ETL logic yet.

At the end of Step 1, I should be able to run:

    python -m src.main

and see a simple confirmation message.

Then STOP.

---

# STEP 2 — Generate and Inspect Sample Data

Goal:

Create a realistic synthetic orders dataset.

Tasks:

- Generate a sample CSV containing approximately 1000-5000 records.
- Generate an equivalent XLSX file.
- Include realistic customer/order/product fields.
- Intentionally introduce data-quality issues.
- Document the expected schema.
- Do not yet build the full ETL pipeline.

The generated dataset should include examples of:

- null values
- duplicate order IDs
- invalid dates
- invalid quantities
- invalid prices
- invalid statuses

Then STOP.

---

# STEP 3 — Implement Extraction

Goal:

Build the Extract portion of the pipeline.

Create:

    src/extract.py

Requirements:

- Read CSV.
- Read XLSX.
- Detect file type from extension.
- Return pandas DataFrame.
- Handle missing files.
- Handle unsupported file formats.
- Log extracted row count.

Create unit tests for extraction where practical.

Do NOT implement validation or database loading yet.

Then STOP.

---

# STEP 4 — Implement Validation

Goal:

Build deterministic data validation.

Create:

    src/validate.py

Requirements:

- Validate required columns.
- Validate required fields.
- Validate numeric fields.
- Validate order status.
- Validate order date.
- Detect duplicates.
- Return valid records.
- Return invalid records.
- Store validation errors for invalid records.

Do not use an LLM.

All validation must be deterministic Python logic.

Then STOP.

---

# STEP 5 — Implement Transformation

Goal:

Build the transformation layer.

Create:

    src/transform.py

Requirements:

- Normalize column names.
- Trim strings.
- Convert dates.
- Normalize data types.
- Calculate total_amount.
- Prepare customer data.
- Prepare product data.
- Prepare order/fact data.

Keep transformation logic independent of database logic.

Then STOP.

---

# STEP 6 — Create PostgreSQL Database Model

Goal:

Create the target database schema.

Create:

    dim_customer
    dim_product
    fact_order

Use SQLAlchemy.

Requirements:

- Define appropriate data types.
- Define primary keys.
- Define foreign keys.
- Define unique constraints where appropriate.
- Create database connection management.

Do not implement the complete loading process yet.

Then STOP.

---

# STEP 7 — Implement Database Loading

Goal:

Load transformed data into PostgreSQL.

Create:

    src/load.py

Requirements:

- Load customers.
- Load products.
- Load orders.
- Use batch operations where appropriate.
- Handle duplicate order IDs.
- Implement basic upsert/idempotency behavior.
- Log inserted/updated record counts.

The same input file should be safe to process multiple times without creating duplicate orders.

Then STOP.

---

# STEP 8 — Build End-to-End ETL Pipeline

Goal:

Connect all previous components.

Create/complete:

    src/main.py

Pipeline:

    Input
      ↓
    Extract
      ↓
    Validate
      ↓
    Transform
      ↓
    Load
      ↓
    Report

The command should be:

    python -m src.main --input data/input/orders.csv

and:

    python -m src.main --input data/input/orders.xlsx

The pipeline should produce logs and output files.

Then STOP.

---

# STEP 9 — Data Quality Report

Goal:

Create a deterministic data-quality report.

Create:

    src/quality.py

Generate:

    output/data_quality_report.json

The report should include:

- records processed
- valid records
- invalid records
- duplicate records
- validation error counts
- null counts
- pipeline status

Do not use AI for calculating these metrics.

Then STOP.

---

# STEP 10 — Add AI Quality Summary

Goal:

Add one small AI feature.

Create:

    src/ai_summary.py

The module should:

1. Read the generated quality metrics.
2. Send those metrics to the LLM.
3. Ask the LLM to generate a concise data-quality summary.
4. Save the summary to:

       output/ai_quality_summary.md

The LLM must not modify or influence the actual ETL pipeline.

If the LLM API fails, the pipeline should still succeed.

Then STOP.

---

# STEP 11 — Testing

Goal:

Add meaningful pytest coverage.

Test:

- extraction
- validation
- transformation
- quality metrics

Ensure the tests are deterministic.

Do not test the LLM itself initially.

Then STOP.

---

# STEP 12 — Final Cleanup and Documentation

Goal:

Make the project interview-ready.

Tasks:

- Clean up unnecessary code.
- Remove dead code.
- Improve logging.
- Improve README.
- Document architecture.
- Document validation rules.
- Document database schema.
- Add example execution.
- Add sample output.
- Document AI design decision.
- Document known limitations.

Do not add new features.

The goal is to make the existing project understandable and presentable.

Then STOP.

---

# 28. Definition of Done

The project is considered complete when I can:

1. Place an orders.csv file in the input directory.
2. Run the pipeline using one command.
3. See the file being read by Python.
4. See validation results.
5. See invalid records separated.
6. See transformed records loaded into PostgreSQL.
7. Query dim_customer.
8. Query dim_product.
9. Query fact_order.
10. Re-run the same input without creating duplicate orders.
11. Generate a JSON data-quality report.
12. Generate an AI-generated quality summary.
13. Run pytest successfully.
14. Explain every major Python module in an interview.

---

# 29. Interview-Level Questions I Should Eventually Be Able to Answer

After completing the project, I should be able to explain:

### Python

- Why did you use pandas?
- Why did you separate extract, validate, transform and load?
- How did you handle exceptions?
- How did you implement logging?
- How did you manage configuration?
- Why did you use SQLAlchemy?
- How did you write unit tests?

### ETL

- What happens if the input file contains invalid records?
- How do you handle duplicates?
- How is the pipeline idempotent?
- What happens if the database is unavailable?
- What happens if 5% of the records are invalid?
- How would you process a 10 GB file instead of a 10 MB file?

### Database

- Why did you create dimension and fact tables?
- Why is order_id the primary key?
- What are the foreign keys?
- How are duplicate records handled?
- How would you optimize the loading process?

### AI

- Why is an LLM being used?
- Why isn't the LLM responsible for validation?
- What happens if the LLM is unavailable?
- How would you evaluate the quality of the AI-generated summary?
- Where would deterministic code be preferred over an LLM?

---

# 30. Final Instruction to the Cursor Agent

Follow this document strictly.

Do not build the complete project in one shot.

Start with STEP 1 only.

After completing STEP 1:

- Show me what was created.
- Explain the important decisions.
- Explain the Python concepts involved.
- Explain how to run it.
- Explain what STEP 2 will do.

Then wait for my instruction before proceeding.

Do not implement STEP 2 automatically.
Do not skip steps.
Do not introduce technologies outside the defined scope without asking first.

The primary goal is not merely to produce working code.

The primary goal is for me to understand the Python Data Engineering concepts demonstrated by the project.