-- Project 03: Claims Efficiency Analysis
-- Purpose: Create raw, analytics, and reporting structures for claims operations KPIs.

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS reporting;

DROP TABLE IF EXISTS raw.claims_efficiency_raw;

CREATE TABLE raw.claims_efficiency_raw (
    claim_id TEXT PRIMARY KEY,
    patient_id TEXT,
    provider_id TEXT,
    provider_specialty TEXT,
    payer TEXT,
    service_line TEXT,
    claim_status TEXT,
    denial_reason TEXT,
    service_date DATE,
    submitted_date DATE,
    decision_date DATE,
    billed_amount NUMERIC(12,2),
    allowed_amount NUMERIC(12,2),
    paid_amount NUMERIC(12,2),
    touch_count INTEGER,
    state TEXT,
    processing_days INTEGER,
    is_denied INTEGER,
    is_reworked INTEGER,
    is_approved INTEGER
);

DROP TABLE IF EXISTS analytics.claims_efficiency_clean;

CREATE TABLE analytics.claims_efficiency_clean AS
SELECT
    claim_id,
    patient_id,
    provider_id,
    provider_specialty,
    payer,
    service_line,
    claim_status,
    denial_reason,
    service_date,
    submitted_date,
    decision_date,
    billed_amount,
    allowed_amount,
    paid_amount,
    touch_count,
    state,
    processing_days,
    CASE WHEN claim_status = 'Denied' THEN 1 ELSE 0 END AS denied_flag,
    CASE WHEN claim_status = 'Reworked' THEN 1 ELSE 0 END AS rework_flag,
    CASE WHEN claim_status = 'Approved' THEN 1 ELSE 0 END AS approved_flag,
    DATE_TRUNC('month', submitted_date)::DATE AS submitted_month,
    CASE
        WHEN processing_days <= 7 THEN '0-7 days'
        WHEN processing_days <= 14 THEN '8-14 days'
        WHEN processing_days <= 30 THEN '15-30 days'
        ELSE '31+ days'
    END AS turnaround_bucket
FROM raw.claims_efficiency_raw;

