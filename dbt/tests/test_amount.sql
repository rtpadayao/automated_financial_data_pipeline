-- ============================================
-- dbt Test: Validate Amount Calculation
-- Purpose: Ensure normalized Amount is correct
-- ============================================

SELECT *
FROM {{ ref('transform') }}
WHERE amount IS NULL
   OR amount = 0
