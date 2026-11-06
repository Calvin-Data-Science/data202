"""Build datasets/mortgages.csv for Week 11 Monday (logistic regression) and Week 14 (fairness).

Source: Home Mortgage Disclosure Act (HMDA) data, 2025, published by the Consumer Financial Protection
Bureau (CFPB); U.S. government data, public domain. Lenders must report every application.
    https://ffiec.cfpb.gov/data-browser/
Query used (the HMDA Data Browser API, one county, applications that ended in a decision):
    https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?counties=26081&years=2025&actions_taken=1,2,3
    (county 26081 = Kent County, Michigan; actions 1 = originated, 2 = approved but not accepted, 3 = denied)

Kept: applications for the applicant's own home (principal residence), a single-family site-built house,
not for a business, not a reverse mortgage, with a loan purpose (purchase, refinance, cash-out refinance,
home improvement, other). Each row is one application.

Columns:
    decision            approved (originated, or approved but not accepted) / denied: the label
    loan_purpose        purchase, refinance, cash-out refinance, home improvement, other
    lien                first / second (a second mortgage or home-equity loan behind a first one)
    loan_type           conventional, FHA, VA, USDA
    loan_amount         $
    property_value      $
    income              $ per year (HMDA reports thousands of dollars)
    debt_to_income      % of monthly income going to debt payments, including the new loan. HMDA reports
                        the exact value only from 36 to 49; other values come as ranges, replaced here by a
                        middle value: <20% -> 15, 20%-<30% -> 25, 30%-<36% -> 33, 50%-60% -> 55, >60% -> 65
    loan_to_value       % (all loans on the property, divided by its value)
    denial_reason       the lender's first stated reason, for denied applications
    race, ethnicity, sex  HMDA's derived values for the applicant(s) ("Joint" = applicants differ)
    age                 the applicant's age range
    tract_minority_pct  % of the census tract's population that is a racial or ethnic minority
    tract_income_pct    the tract's median family income, as % of the metro area's
    census_tract        11-digit census tract code

Usage:  python scripts/make_mortgages.py [path/to/downloaded.csv]   (without a path, the API is queried)
"""
import io
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "mortgages.csv"
URL = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?counties=26081&years=2025&actions_taken=1,2,3"

if len(sys.argv) > 1:
    raw = pd.read_csv(sys.argv[1], low_memory=False)
else:
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (DATA 202 course data script)"})
    raw = pd.read_csv(io.BytesIO(urllib.request.urlopen(request, timeout=300).read()), low_memory=False)

keep = ((raw["occupancy_type"] == 1) & (raw["total_units"].astype(str) == "1") & (raw["construction_method"] == 1)
        & (raw["business_or_commercial_purpose"] == 2) & (raw["reverse_mortgage"] == 2)
        & raw["loan_purpose"].isin([1, 2, 31, 32, 4]))
h = raw[keep]

DTI_RANGES = {"<20%": 15, "20%-<30%": 25, "30%-<36%": 33, "50%-60%": 55, ">60%": 65}
REASONS = {1: "debt-to-income ratio", 2: "employment history", 3: "credit history", 4: "collateral",
           5: "insufficient cash", 6: "unverifiable information", 7: "incomplete application",
           8: "mortgage insurance denied", 9: "other"}

mortgages = pd.DataFrame({
    "decision": np.where(h["action_taken"] == 3, "denied", "approved"),
    "loan_purpose": h["loan_purpose"].map({1: "purchase", 31: "refinance", 32: "cash-out refinance",
                                           2: "home improvement", 4: "other"}),
    "lien": h["lien_status"].map({1: "first", 2: "second"}),
    "loan_type": h["loan_type"].map({1: "conventional", 2: "FHA", 3: "VA", 4: "USDA"}),
    "loan_amount": h["loan_amount"],
    "property_value": pd.to_numeric(h["property_value"], errors="coerce"),
    "income": pd.to_numeric(h["income"], errors="coerce") * 1000,
    "debt_to_income": h["debt_to_income_ratio"].map(lambda s: DTI_RANGES.get(s, pd.to_numeric(s, errors="coerce"))),
    "loan_to_value": pd.to_numeric(h["loan_to_value_ratio"], errors="coerce").round(1),
    "denial_reason": h["denial_reason-1"].map(REASONS),
    "race": h["derived_race"],
    "ethnicity": h["derived_ethnicity"],
    "sex": h["derived_sex"],
    "age": h["applicant_age"].replace({"8888": np.nan}),
    "tract_minority_pct": h["tract_minority_population_percent"].round(1),
    "tract_income_pct": h["tract_to_msa_income_percentage"].round(1),
    "census_tract": h["census_tract"].astype("Int64"),
})
mortgages.loc[mortgages["income"] <= 0, "income"] = np.nan          # a handful of zero or negative incomes

mortgages.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(mortgages)} applications, {(mortgages['decision'] == 'denied').mean():.1%} denied")
print("blanks:", mortgages.isna().sum()[mortgages.isna().sum() > 0].to_dict())
