"""Generate realistic synthetic claims data for Project 03.

The output is intentionally synthetic and safe for GitHub. It is designed to
support SQL, Python, and Tableau portfolio work without using PHI.
"""

from __future__ import annotations

from pathlib import Path
import random

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"


def weighted_choice(values: list[str], weights: list[float], size: int) -> list[str]:
    return random.choices(values, weights=weights, k=size)


def main() -> None:
    random.seed(42)
    np.random.seed(42)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    n = 8500
    start_dates = pd.to_datetime(
        np.random.choice(pd.date_range("2024-01-01", "2025-03-31"), size=n)
    )
    payers = weighted_choice(
        ["Medicare", "Medicaid", "Commercial", "Medicare Advantage", "Self Pay"],
        [0.29, 0.18, 0.34, 0.15, 0.04],
        n,
    )
    specialties = weighted_choice(
        ["Primary Care", "Cardiology", "Orthopedics", "Emergency Medicine", "Oncology", "Radiology"],
        [0.26, 0.16, 0.15, 0.18, 0.10, 0.15],
        n,
    )
    providers = [f"PRV-{i:04d}" for i in np.random.randint(1001, 1140, size=n)]
    claim_status = weighted_choice(
        ["Approved", "Denied", "Pending", "Reworked"],
        [0.70, 0.12, 0.10, 0.08],
        n,
    )
    denial_reasons = {
        "Approved": "Not Applicable",
        "Pending": "Under Review",
        "Reworked": random.choice(["Missing Documentation", "Coding Review", "Eligibility Review"]),
        "Denied": random.choice(["Prior Authorization", "Medical Necessity", "Eligibility", "Coding Error", "Timely Filing"]),
    }

    base_days = np.random.gamma(shape=3.2, scale=4.8, size=n).round().astype(int)
    payer_delay = pd.Series(payers).map(
        {"Medicare": 2, "Medicaid": 5, "Commercial": 4, "Medicare Advantage": 6, "Self Pay": 8}
    ).to_numpy()
    status_delay = pd.Series(claim_status).map({"Approved": 0, "Denied": 9, "Pending": 15, "Reworked": 12}).to_numpy()
    processing_days = np.clip(base_days + payer_delay + status_delay, 1, 95)

    submitted_dates = start_dates + pd.to_timedelta(np.random.randint(0, 6, size=n), unit="D")
    decision_dates = submitted_dates + pd.to_timedelta(processing_days, unit="D")
    billed_amount = np.round(np.random.lognormal(mean=7.2, sigma=0.55, size=n), 2)
    allowed_amount = np.round(billed_amount * np.random.uniform(0.42, 0.78, size=n), 2)
    paid_amount = np.where(
        pd.Series(claim_status).eq("Denied"),
        0,
        np.round(allowed_amount * np.random.uniform(0.72, 0.98, size=n), 2),
    )

    df = pd.DataFrame(
        {
            "claim_id": [f"CLM-{i:07d}" for i in range(1, n + 1)],
            "patient_id": [f"PAT-{i:06d}" for i in np.random.randint(10000, 99999, size=n)],
            "provider_id": providers,
            "provider_specialty": specialties,
            "payer": payers,
            "service_line": weighted_choice(
                ["Office Visit", "Surgery", "Diagnostic Imaging", "Emergency", "Infusion", "Lab"],
                [0.30, 0.13, 0.19, 0.17, 0.08, 0.13],
                n,
            ),
            "claim_status": claim_status,
            "denial_reason": [denial_reasons[status] for status in claim_status],
            "service_date": start_dates,
            "submitted_date": submitted_dates,
            "decision_date": decision_dates,
            "billed_amount": billed_amount,
            "allowed_amount": allowed_amount,
            "paid_amount": paid_amount,
            "touch_count": np.where(pd.Series(claim_status).isin(["Denied", "Reworked"]), np.random.randint(2, 6, size=n), np.random.randint(1, 3, size=n)),
            "state": weighted_choice(["TX", "FL", "GA", "NC", "AZ", "OH", "PA"], [0.22, 0.17, 0.12, 0.13, 0.12, 0.12, 0.12], n),
        }
    )
    df["processing_days"] = (df["decision_date"] - df["submitted_date"]).dt.days
    df["is_denied"] = df["claim_status"].eq("Denied").astype(int)
    df["is_reworked"] = df["claim_status"].eq("Reworked").astype(int)
    df["is_approved"] = df["claim_status"].eq("Approved").astype(int)

    raw_path = RAW_DIR / "claims_efficiency_synthetic.csv"
    processed_path = PROCESSED_DIR / "claims_efficiency_clean.csv"
    df.to_csv(raw_path, index=False)
    df.to_csv(processed_path, index=False)
    print(f"Wrote {raw_path}")
    print(f"Wrote {processed_path}")


if __name__ == "__main__":
    main()

