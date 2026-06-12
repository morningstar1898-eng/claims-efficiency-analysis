# Project 03: Claims Efficiency Analysis

**Portfolio owner:** Meagan Parsons  
**Portfolio focus:** Claims operations, denial management, revenue cycle KPIs, SQL, Python, Tableau, and business intelligence  
**Status:** Build-ready framework; needs dataset, SQL implementation, Python analysis, dashboard screenshots, and executive findings

## Business Problem

Healthcare organizations lose time and revenue when claims move slowly through the billing cycle, require repeated rework, or are denied for preventable reasons. Operations leaders need visibility into where claims stall, which denial categories create the greatest burden, and which payer or service-line patterns indicate avoidable reimbursement friction.

## Project Objective

Build a claims efficiency analytics framework that evaluates claim lifecycle performance, denial behavior, reimbursement trends, and operational bottlenecks. The goal is to translate claims activity into decision-ready KPIs for revenue cycle, operations, and finance stakeholders.

## Tools Used

- SQL and PostgreSQL for claims-level querying, aggregation, and KPI views
- Python and pandas for data cleaning, trend analysis, and dashboard extract preparation
- Tableau for executive dashboard design and operational monitoring
- Markdown documentation for KPI definitions, workflow notes, and recruiter review

## Workflow

1. Ingest raw claims data into a structured analytics workspace.
2. Validate required fields such as claim ID, payer, provider, service date, claim status, billed amount, allowed amount, paid amount, and denial reason.
3. Standardize dates, claim status categories, payer groups, and service-line labels.
4. Build SQL views for claims volume, denial rate, reimbursement rate, processing cycle time, and aging buckets.
5. Use Python to profile trends, identify outliers, and prepare Tableau-ready extracts.
6. Design a Tableau dashboard that supports executive review and operational drilldown.

## Exact Build Instructions

1. Generate synthetic claims data:

```bash
python scripts/generate_claims_efficiency_data.py
```

2. Create PostgreSQL tables with:

```text
sql/01_schema.sql
```

3. Import `data/processed/claims_efficiency_clean.csv` into `raw.claims_efficiency_raw`.
4. Run SQL scripts in order:

```text
sql/02_data_quality_checks.sql
sql/03_kpi_views.sql
sql/04_analysis_queries.sql
```

5. Build the Tableau dashboard using:

```text
tableau/dashboard_spec.md
```

6. Add screenshots to `screenshots/` and update the executive summary.

## KPIs Analyzed

- Total claims submitted
- Clean claim rate
- Denial rate
- Rework rate
- Average processing cycle time
- Paid-to-billed ratio
- Allowed-to-billed ratio
- Net reimbursement variance
- Claims aging by payer and service line
- Top denial categories by financial impact

## SQL Skills Demonstrated

- Claims-level aggregation and status classification
- Common table expressions for staged transformations
- Window functions for payer and provider ranking
- Date logic for cycle time and aging buckets
- KPI view creation for dashboard consumption
- Data quality checks for missing, duplicate, and invalid claim records

## Python Skills Demonstrated

- Data cleaning and normalization with pandas
- Claims trend profiling by month, payer, and service line
- Outlier detection for reimbursement and cycle-time patterns
- Dashboard extract generation
- Reproducible notebook documentation

## Tableau and Dashboard Skills Demonstrated

- Executive KPI scorecards
- Claims funnel and denial trend visualizations
- Payer-level operational benchmarking
- Service-line drilldowns
- Dashboard filters for payer, provider, status, and time period
- Clear distinction between summary KPIs and operational detail

## Healthcare Business Relevance

Claims efficiency analysis is directly relevant to revenue cycle management, billing operations, payer relations, reimbursement analytics, and revenue integrity. This project shows the ability to connect transactional claim data to operational decisions that can reduce rework, accelerate payment, and improve financial visibility.

## Executive Summary Placeholder

`[Add final executive summary after analysis is completed: 3-5 bullets covering key findings, business interpretation, and recommended actions.]`

## Screenshots Placeholder

Store final dashboard screenshots in:

```text
project-03-claims-efficiency-analysis/screenshots/
```

Recommended files:

- `claims_efficiency_dashboard_overview.png`
- `denial_trends_by_payer.png`
- `claims_aging_operational_view.png`

## Architecture Diagram Placeholder

```text
Raw Claims Data -> SQL Staging Tables -> KPI Views -> Python Validation -> Tableau Dashboard Extracts -> Executive Dashboard
```

## Supporting Documentation

- [Data Dictionary](docs/data_dictionary.md)
- [Notebook Structure](docs/notebook_structure.md)
- [Tableau Dashboard Spec](tableau/dashboard_spec.md)

## Future Improvements

- Add payer contract benchmarks for expected reimbursement variance.
- Incorporate denial appeal outcomes and overturn rates.
- Build automated monthly refresh scripts.
- Add claim-line-level analysis for CPT, HCPCS, and revenue code patterns.
- Expand quality checks into a formal validation suite.

## Recruiter Skill Highlights

- Revenue cycle analytics
- Claims operations KPIs
- SQL-based healthcare metric development
- Python data preparation
- Tableau executive dashboarding
- Business communication for healthcare stakeholders

## Portfolio Links

- LinkedIn: [www.linkedin.com/in/meagan-parsons-37321a177](https://www.linkedin.com/in/meagan-parsons-37321a177)
- GitHub: [github.com/morningstar1898-eng](https://github.com/morningstar1898-eng)
- Tableau Public: [public.tableau.com/app/profile/meagan.parsons/vizzes](https://public.tableau.com/app/profile/meagan.parsons/vizzes)
