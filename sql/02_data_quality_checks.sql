-- Project 03: Data quality checks
-- Purpose: Validate claims data before KPI reporting.

SELECT COUNT(*) AS total_rows
FROM analytics.claims_efficiency_clean;

SELECT claim_id, COUNT(*) AS duplicate_count
FROM analytics.claims_efficiency_clean
GROUP BY claim_id
HAVING COUNT(*) > 1;

SELECT
    SUM(CASE WHEN provider_id IS NULL THEN 1 ELSE 0 END) AS missing_provider_id,
    SUM(CASE WHEN payer IS NULL THEN 1 ELSE 0 END) AS missing_payer,
    SUM(CASE WHEN claim_status IS NULL THEN 1 ELSE 0 END) AS missing_claim_status,
    SUM(CASE WHEN submitted_date IS NULL THEN 1 ELSE 0 END) AS missing_submitted_date,
    SUM(CASE WHEN decision_date IS NULL THEN 1 ELSE 0 END) AS missing_decision_date
FROM analytics.claims_efficiency_clean;

SELECT *
FROM analytics.claims_efficiency_clean
WHERE decision_date < submitted_date
   OR submitted_date < service_date
   OR billed_amount < 0
   OR allowed_amount < 0
   OR paid_amount < 0;

