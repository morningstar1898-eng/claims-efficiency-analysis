-- Project 03: KPI views
-- Purpose: Create reporting views for claims processing efficiency dashboards.

CREATE OR REPLACE VIEW reporting.vw_claims_efficiency_monthly AS
SELECT
    submitted_month,
    COUNT(*) AS total_claims,
    ROUND(AVG(processing_days), 2) AS avg_processing_days,
    ROUND(100.0 * SUM(approved_flag) / COUNT(*), 2) AS approval_rate,
    ROUND(100.0 * SUM(denied_flag) / COUNT(*), 2) AS denial_rate,
    ROUND(100.0 * SUM(rework_flag) / COUNT(*), 2) AS rework_rate,
    ROUND(SUM(paid_amount), 2) AS total_paid_amount,
    ROUND(SUM(billed_amount), 2) AS total_billed_amount
FROM analytics.claims_efficiency_clean
GROUP BY submitted_month;

CREATE OR REPLACE VIEW reporting.vw_claims_efficiency_provider AS
WITH provider_base AS (
    SELECT
        provider_id,
        provider_specialty,
        COUNT(*) AS total_claims,
        AVG(processing_days) AS avg_processing_days,
        SUM(denied_flag) AS denied_claims,
        SUM(rework_flag) AS reworked_claims,
        SUM(approved_flag) AS approved_claims,
        SUM(paid_amount) AS total_paid_amount
    FROM analytics.claims_efficiency_clean
    GROUP BY provider_id, provider_specialty
),
ranked AS (
    SELECT
        *,
        ROUND(100.0 * denied_claims / NULLIF(total_claims, 0), 2) AS denial_rate,
        ROUND(100.0 * reworked_claims / NULLIF(total_claims, 0), 2) AS rework_rate,
        RANK() OVER (ORDER BY AVG(avg_processing_days) DESC) AS delay_rank,
        RANK() OVER (ORDER BY SUM(denied_claims) DESC) AS denial_volume_rank
    FROM provider_base
    GROUP BY provider_id, provider_specialty, total_claims, avg_processing_days, denied_claims, reworked_claims, approved_claims, total_paid_amount
)
SELECT
    *,
    CASE
        WHEN avg_processing_days >= 30 OR denial_rate >= 20 THEN 'High Operational Risk'
        WHEN avg_processing_days >= 18 OR denial_rate >= 12 THEN 'Moderate Operational Risk'
        ELSE 'Expected Range'
    END AS operational_risk_segment
FROM ranked;

CREATE OR REPLACE VIEW reporting.vw_claims_efficiency_denial_drivers AS
SELECT
    payer,
    service_line,
    denial_reason,
    COUNT(*) AS denied_claims,
    ROUND(SUM(billed_amount), 2) AS denied_billed_amount,
    ROUND(AVG(processing_days), 2) AS avg_processing_days
FROM analytics.claims_efficiency_clean
WHERE denied_flag = 1
GROUP BY payer, service_line, denial_reason;

