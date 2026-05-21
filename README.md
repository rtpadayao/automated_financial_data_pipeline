# Financial Analytics Pipeline (Mock API → Postgres → dbt → Power BI)

## Overview

This project demonstrates a containerized, automated data pipeline:

- **Flask API** simulates ERP/CRM transactions.
- **Postgres** stores raw GL transactions.
- **Airflow DAG** orchestrates daily incremental loads.
- **dbt** transforms raw data into analytics marts.
- **Power BI** visualizes KPIs.

## Features

- Incremental ingestion (API → Postgres).
- Incremental transformation (dbt models).
- Normalized Amount calculation (Debit/Credit logic).
- Data quality tests (Amount validation, duplicate entry check).
- Containerized setup with Docker Compose.

## Setup

1. Clone repo.
2. Add credentials to `.env`.
3. Run `docker-compose up`.
4. Access services:
   - Flask API → `http://localhost:5000/api/gl`
   - pgAdmin → `http://localhost:8080`
   - Airflow → `http://localhost:8081`

## Folder Structure

- `postgres/` → schema init script
- `flaskapi/` → mock API + dataset
- `dags/` → Airflow DAG
- `dbt/` → dbt project, models, tests
- `airflow_logs/` → persisted logs
- `postgres_data/` → persisted database

## Recruiter Demo Flow

1. Show API returning transactions.
2. Show DAG graph in Airflow UI.
3. Show dbt run + tests passing.
4. Show Power BI dashboard refreshing.
