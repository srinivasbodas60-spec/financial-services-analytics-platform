-- Run these checks in CI/orchestration and fail the batch when a critical check > 0.

-- Duplicate business events
SELECT event_id, COUNT(*) AS row_count
FROM fact_transaction
GROUP BY event_id
HAVING COUNT(*) > 1;

-- Orphan foreign keys
SELECT COUNT(*) AS orphan_account_rows
FROM fact_transaction f
LEFT JOIN dim_account a ON f.account_key = a.account_key
WHERE a.account_key IS NULL;

-- Invalid business values
SELECT COUNT(*) AS invalid_status_rows
FROM dim_account
WHERE status NOT IN ('Active', 'Closed', 'Suspended');

-- Negative source amounts are rejected; signed_amount carries transaction direction.
SELECT COUNT(*) AS negative_amount_rows
FROM fact_transaction
WHERE amount < 0;

