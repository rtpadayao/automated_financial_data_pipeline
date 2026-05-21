# ============================================
# Airflow DAG: GL Pipeline (Incremental)
# Purpose: Automate daily incremental loads
# Steps: Extract → Load → dbt run → dbt test
# ============================================

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests
import psycopg2

def extract_load_incremental():
    """Extract only new transactions from Flask API and load into Postgres"""
    conn = psycopg2.connect(
        dbname="finance_demo",
        user="postgres",
        password="123learn",
        host="postgres",
        port="5432"
    )
    cur = conn.cursor()

    # Find latest date in Postgres
    cur.execute("SELECT COALESCE(MAX(date), '1900-01-01') FROM finance.gl_transactions;")
    last_date = cur.fetchone()[0]

    # Call API for incremental data
    response = requests.get(f"http://flaskapi:5000/api/gl/incremental/{last_date}")
    data = response.json()

    # Ensure table exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS finance.gl_transactions (
        entry_no VARCHAR(20) PRIMARY KEY,
        date DATE,
        territory_key INT,
        account_key INT,
        details TEXT,
        debit NUMERIC,
        credit NUMERIC
    );
    """)

    # Insert new rows
    for row in data:
        cur.execute("""
            INSERT INTO finance.gl_transactions (entry_no, date, territory_key, account_key, details, debit, credit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (entry_no) DO NOTHING;
        """, (
            row["EntryNo"],
            row["Date"],
            row["Territory_key"],
            row["Account_key"],
            row["Details"],
            row["Debit"],
            row["Credit"]
        ))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="gl_pipeline_incremental",
    start_date=datetime(2026, 5, 21),
    schedule_interval="@daily",
    catchup=False,
    tags=["finance", "etl", "dbt"]
) as dag:

    extract_load_task = PythonOperator(
        task_id="extract_load_incremental",
        python_callable=extract_load_incremental
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt && dbt test"
    )

    extract_load_task >> dbt_run >> dbt_test
