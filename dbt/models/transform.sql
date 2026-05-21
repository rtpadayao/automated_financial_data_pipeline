-- ============================================
-- dbt Transformation Model
-- Purpose: Normalize Debit/Credit into Amount
-- ============================================

{{ config(materialized='incremental', unique_key='entry_no') }}

WITH normalized AS (
    SELECT
        entry_no,
        date,
        territory_key,
        account_key,
        details,
        debit,
        credit,
        CASE
            WHEN account_key <= 100
                THEN debit - credit   -- Assets & Expenses (debit-normal)
            WHEN account_key > 100
                THEN credit - debit   -- Liabilities, Equity, Revenue (credit-normal)
            ELSE 0
        END AS amount
    FROM {{ source('finance', 'gl_transactions') }}
)

SELECT *
FROM normalized

{% if is_incremental() %}
  WHERE date > (SELECT MAX(date) FROM {{ this }})
{% endif %}
