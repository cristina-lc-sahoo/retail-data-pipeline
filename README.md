# Retail Data Engineering Pipeline

A hands-on data engineering project demonstrating end-to-end data ingestion, database development, SQL transformations, and data quality testing using Python, PostgreSQL, and dbt.

## Project Overview

This project builds a retail data pipeline that ingests raw CSV files, loads data into PostgreSQL, transforms and organizes the data using dbt, and produces analytical datasets for retail sales reporting.

The objective is to demonstrate practical data engineering skills, including ETL development, data ingestion, relational database management, SQL transformations, data quality validation, and pipeline automation.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | ETL development and CSV ingestion |
| PostgreSQL 17 | Relational database and data storage |
| SQL | Data manipulation and transformation |
| dbt Core 1.7.17 | Data modeling and transformation |
| dbt-postgres | PostgreSQL integration for dbt |
| Git / GitHub | Version control and project management |

## Project Architecture

          Source CSV Files
                 |
                 v
          Python ETL Script
          (load_csv.py)
                 |
                 v
           PostgreSQL
             Database
                 |
                 v
           Raw Schema
                 |
                 v
           dbt Models
                 |
                 v
         Staging Transformations
                 |
                 v
         Analytics Transformations
                 |
                 v
          Sales Reporting


## Data Sources

The project uses three retail datasets:

| Dataset | Records | Description |
|---|---:|---|
| products.csv | 13 | Retail product information |
| sales.csv | 240 | Retail sales transactions |
| stores.csv | 6 | Store information |
| **Total** | **259** | **Source records** |

## ETL Pipeline Development

A Python-based ingestion script (`scripts/load_csv.py`) was developed to automate the loading of CSV files into PostgreSQL.

Key functionality includes:

- Reading and processing CSV files.
- Loading product, sales, and store data into PostgreSQL.
- Managing duplicate records through conflict handling.
- Supporting repeatable and idempotent data loads.
- Logging ingestion activity and execution results.
- Tracking record counts and rejected records.

The ingestion process was successfully executed multiple times, confirming that existing records were not duplicated during subsequent loads.

## PostgreSQL Database Design

The project uses a PostgreSQL database named `retail_dw` with separate schemas for raw data and analytics.

| Schema | Purpose |
|---|---|
| raw | Stores ingested source data |
| analytics | Stores transformed data models |

This structure separates source data from analytical transformations.

## dbt Data Transformations

dbt was configured to connect to PostgreSQL and manage SQL-based transformations.

### Staging Model: `stg_sales`

The staging model prepares raw sales data for analytical processing.

Transformations include:

- Casting sales dates into appropriate date formats.
- Trimming whitespace from product, region, and salesperson fields.
- Standardizing selected fields for downstream analysis.

### Analytics Model: `sales_by_region`

The analytics model aggregates sales data by region.

Metrics calculated include:

- Total number of orders.
- Total quantity sold.
- Total sales revenue.

The model uses dbt's `ref()` function to establish dependencies between transformation models.

## Data Quality Testing

dbt tests were implemented to validate the integrity of the staging sales data.

| Test | Column | Purpose |
|---|---|---|
| not_null | order_id | Ensures order IDs are populated |
| unique | order_id | Ensures order IDs are unique |

The project successfully completed `dbt build`, executing both transformation models and their associated data quality tests.

**Build results:**
- 2 dbt models successfully built.
- 2 data quality tests passed.

## Analytical Results

The regional sales aggregation produced the following results:

| Metric | Result |
|---|---:|
| Total Orders | 240 |
| Total Units Sold | 1,108 |
| Total Sales Revenue | $142,437.14 |
| Highest Revenue Region | Central |
| Central Region Revenue | $30,787.94 |

These results demonstrate the successful ingestion, transformation, and aggregation of retail sales data.

## Repository Structure

retail-data-pipeline/
│
├── data/
│   ├── products.csv
│   ├── sales.csv
│   └── stores.csv
│
├── scripts/
│   └── load_csv.py
│
├── retail_dbt/
│   ├── models/
│   │   └── staging/
│   │       ├── stg_sales.sql
│   │       ├── sales_by_region.sql
│   │       └── schema.yml
│   │
│   ├── dbt_project.yml
│   └── ...
│
├── .gitignore
└── README.md


## Future Enhancements

The next phase of this project will focus on expanding pipeline orchestration and cloud data engineering capabilities.

Planned enhancements include:

- **Apache Airflow:** Orchestrate Python ingestion and dbt transformation tasks through scheduled and dependency-based workflows.
- **Cloud Integration:** Extend the pipeline to a cloud-based data platform.
- **Expanded Data Quality:** Add additional validation rules and monitoring.
- **Pipeline Monitoring:** Improve execution tracking, error handling, and operational visibility.

*Airflow orchestration is currently planned but has not yet been executed.*

## Skills Demonstrated

- Python ETL Development
- CSV Data Ingestion and Processing
- PostgreSQL Database Management
- SQL Query Development and Data Transformation
- dbt Data Modeling
- Data Quality Testing
- Idempotent Data Loading
- Data Pipeline Development
- Git and GitHub Version Control

---

**Project:** Retail Data Engineering Pipeline  
**Status:** Core ETL and dbt implementation completed; Airflow orchestration planned.