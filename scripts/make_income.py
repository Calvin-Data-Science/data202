"""
Build datasets/income.csv -- a 2,000-person sample of the UCI "Adult" census
income data for Reading 6 (Week 7, decision trees, cross-validation and grid
search, weeks/07/reading6.md).

Source: Becker, B. & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning
Repository. https://doi.org/10.24432/C5XW20 (CC BY 4.0). Its description:
"Extraction was done by Barry Becker from the 1994 Census database. ...
Prediction task is to determine whether a person makes over 50K a year."

Changes from the original adult.data (32,561 rows):
- a random sample of 2,000 rows (random_state=1), so trees overfit visibly and
  every fit in the reading runs instantly;
- `education_num` renamed `education_level` (a 1-16 code for the highest
  degree, e.g. 9 = HS-grad, 13 = Bachelors, 16 = Doctorate -- not years);
- `married` added: 1 if marital_status is "Married-civ-spouse" or
  "Married-AF-spouse" (living with a spouse), else 0;
- `high_income` added: 1 if income is ">50K", else 0;
- only the columns the reading uses are kept.

Columns: age, education, education_level, marital_status, married,
hours_per_week, sex, race, income, high_income.

Usage:  python scripts/make_income.py [path/to/adult.data]
        (with no path, the UCI zip is downloaded)
"""

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/2/adult.zip"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "income.csv"
COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num", "marital_status",
    "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss",
    "hours_per_week", "native_country", "income",
]

if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    with urllib.request.urlopen(URL) as response:
        source = io.BytesIO(zipfile.ZipFile(io.BytesIO(response.read())).read("adult.data"))

adult = pd.read_csv(source, names=COLUMNS, skipinitialspace=True)
income = adult.sample(2000, random_state=1).rename(columns={"education_num": "education_level"})
income["married"] = income["marital_status"].isin(["Married-civ-spouse", "Married-AF-spouse"]).astype(int)
income["high_income"] = (income["income"] == ">50K").astype(int)
income = income[["age", "education", "education_level", "marital_status", "married",
                 "hours_per_week", "sex", "race", "income", "high_income"]]
income.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(income)} rows, {income['high_income'].sum()} with high_income = 1")
