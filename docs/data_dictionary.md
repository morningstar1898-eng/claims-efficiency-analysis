# Project 03 Data Dictionary

| Field | Description | Example |
| --- | --- | --- |
| `claim_id` | Synthetic unique claim identifier | `CLM-0000001` |
| `patient_id` | Synthetic patient identifier | `PAT-123456` |
| `provider_id` | Synthetic provider identifier | `PRV-1001` |
| `provider_specialty` | Provider specialty group | `Cardiology` |
| `payer` | Payer category | `Commercial` |
| `service_line` | Operational service category | `Diagnostic Imaging` |
| `claim_status` | Final or current claim disposition | `Approved`, `Denied`, `Pending`, `Reworked` |
| `denial_reason` | Denial or review category | `Prior Authorization` |
| `service_date` | Date care was delivered | `2024-04-15` |
| `submitted_date` | Date claim was submitted | `2024-04-18` |
| `decision_date` | Date claim decision occurred | `2024-05-02` |
| `billed_amount` | Submitted charge amount | `1250.00` |
| `allowed_amount` | Allowed reimbursement amount | `790.00` |
| `paid_amount` | Paid amount after adjudication | `710.00` |
| `touch_count` | Number of operational touches or rework steps | `3` |
| `state` | Provider or claim state | `TX` |
| `processing_days` | Days from submission to decision | `14` |

