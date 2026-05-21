-- ============================================
-- dbt Test: Duplicate Entry Check
-- Purpose: Ensure entry_no is unique
-- ============================================

SELECT entry_no, COUNT(*) AS dup_count
FROM {{ ref('transform') }}
GROUP BY entry_no
HAVING COUNT(*) > 1
