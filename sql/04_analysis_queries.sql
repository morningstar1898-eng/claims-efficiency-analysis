-- Project 03: Advanced analysis queries
-- Purpose: Demonstrate CTEs, joins, CASE logic, window functions, and operational interpretation.

WITH payer_metrics AS (
    SELECT
        payer,
        COUNT(*) AS total_claims,
        AVG(processing_days) AS avg_processing_days,
        SUM(denied_flag) AS denied_claims,
        SUM(rework_flag) AS reworked_claims
    FROM analytics.claims_efficiency_clean
    GROUP BY payer
),
portfolio_avg AS (
    SELECT AVG(processing_days) AS portfolio_processing_avg
    FROM analytics.claims_efficiency_clean
)
SELECT
    p.payer,
    p.total_claims,
    ROUND(p.avg_processing_days, 2) AS avg_processing_days,
    ROUND(p.avg_processing_days - a.portfolio_processing_avg, 2) AS days_above_portfolio_avg,
    ROUND(100.0 * p.denied_claims / p.total_claims, 2) AS denial_rate,
    ROUND(100.0 * p.reworked_claims / p.total_claims, 2) AS rework_rate,
    CASE
        WHEN p.avg_processing_days > a.portfolio_processing_avg + 7 THEN 'Review payer workflow'
        WHEN 100.0 * p.denied_claims / p.total_claims > 15 THEN 'Review denial prevention'
        ELSE 'Monitor'
    END AS recommended_action
FROM payer_metrics p
CROSS JOIN portfolio_avg a
ORDER BY days_above_portfolio_avg DESC;

SELECT
    submitted_month,
    total_claims,
    avg_processing_days,
    denial_rate,
    LAG(denial_rate) OVER (ORDER BY submitted_month) AS prior_month_denial_rate,
    ROUND(denial_rate - LAG(denial_rate) OVER (ORDER BY submitted_month), 2) AS denial_rate_change
FROM reporting.vw_claims_efficiency_monthly
ORDER BY submitted_month;

