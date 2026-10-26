"""
Build datasets/census.csv -- the same 2,000 people as datasets/income.csv
(Reading 6), with every column of the UCI "Adult" census income data, for
Reading 7 (Week 9: scaling, one-hot encoding, pipelines and missing data,
weeks/09/reading7.md).

Source: Becker, B. & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning
Repository. https://doi.org/10.24432/C5XW20 (CC BY 4.0). Extracted by Barry
Becker from the 1994 Census database (Current Population Survey).

Changes from the original adult.data (32,561 rows):
- the same random sample of 2,000 rows as income.csv (random_state=1);
- the file's "?" entries (its README: "Convert Unknown to '?'") become blanks,
  so pandas reads them as missing: workclass and occupation (125 people,
  the same 125 in both columns) and native_country (30 people);
- `education_num` renamed `education_level` (a 1-16 code for the highest
  degree, e.g. 9 = HS-grad, 13 = Bachelors, 16 = Doctorate -- not years);
- `high_income` added: 1 if income is ">50K", else 0;
- `fnlwgt` (a survey weight, not a fact about the person) and the text
  `income` column are dropped.

Columns: age, workclass, education, education_level, marital_status,
occupation, relationship, race, sex, capital_gain, capital_loss,
hours_per_week, native_country, high_income.

Usage:  python scripts/make_census.py [path/to/adult.data]
        (with no path, the UCI zip is downloaded)
"""

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/2/adult.zip"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "census.csv"
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

adult = pd.read_csv(source, names=COLUMNS, skipinitialspace=True, na_values="?")
census = adult.sample(2000, random_state=1).rename(columns={"education_num": "education_level"})
census["high_income"] = (census["income"] == ">50K").astype(int)
census = census.drop(columns=["fnlwgt", "income"])
census.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(census)} rows, {census['high_income'].sum()} with high_income = 1")
print(census.isna().sum()[lambda n: n > 0].to_string())
