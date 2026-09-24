"""
Generate datasets/applicants.csv -- the teaching dataset for Reading 4
(weeks/05/reading4.md: k-means, scaling, PCA, and turning PCA into a score).

300 fake credit applicants at a fictional credit union, five numbers each:
    annual_income           US dollars per year
    credit_history_years    years since the applicant's first credit account
    late_payments           late payments in the last 2 years (a count)
    credit_utilization_pct  % of available credit currently in use (0-100)
    open_accounts           number of open credit accounts

There is deliberately NO label column (no "repaid"/"defaulted"): the reading
is about finding structure without an answer key.

Four loose groups generate the data (their names are NOT saved):
    established  -- high income, long history, almost never late, low utilization
    stretched    -- middle income, several late payments, high utilization
    new to credit-- lower income, SHORT history, few accounts, almost never late
    struggling   -- low income, many late payments, utilization near 100%
The "new to credit" group is the point of the reading's last page: on a single
PCA-based score it ranks BELOW the stretched group, despite almost never
paying late -- being barely visible to the credit system counts against you.

Income is in dollars on purpose: unscaled, it swamps every other column
(unscaled PCA puts ~100% of the variance on it), which motivates scaling.

Usage:  python scripts/make_applicants.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# n, income (mean, sd), history years (mean, sd), late-payment rate, utilization % (mean, sd), accounts (mean, sd)
GROUPS = [
    (90, (92000, 18000), (19, 5),   0.4, (18, 8),  (7, 2)),     # established
    (80, (58000, 12000), (10, 4),   3.5, (68, 12), (6, 2)),     # stretched
    (70, (40000, 10000), (2, 1.2),  0.3, (28, 12), (1.5, 0.8)), # new to credit
    (60, (34000, 8000),  (11, 5),   7.0, (88, 8),  (4, 1.5)),   # struggling
]


def main():
    rng = np.random.default_rng(1)
    blocks = []
    for n, income, history, late_rate, util, accounts in GROUPS:
        blocks.append(pd.DataFrame({
            "annual_income": np.clip(rng.normal(*income, n), 12000, None).round(-2).astype(int),
            "credit_history_years": np.clip(rng.normal(*history, n), 0.3, None).round(1),
            "late_payments": rng.poisson(late_rate, n),
            "credit_utilization_pct": np.clip(rng.normal(*util, n), 0, 100).round(0).astype(int),
            "open_accounts": np.clip(rng.normal(*accounts, n), 1, None).round(0).astype(int),
        }))
    applicants = pd.concat(blocks).sample(frac=1, random_state=1).reset_index(drop=True)  # shuffle: row order hides the groups
    applicants.insert(0, "applicant_id", [f"A{i:03d}" for i in range(1, len(applicants) + 1)])

    out = ROOT / "datasets" / "applicants.csv"
    applicants.to_csv(out, index=False, lineterminator="\n")
    print(f"Wrote {out} ({len(applicants)} rows)")


if __name__ == "__main__":
    main()
