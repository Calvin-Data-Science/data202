"""Build datasets/titanic.csv for Week 9 (preprocessing, pipelines, missing data).

Source: titanic3, the passenger list of the RMS Titanic compiled by Thomas Cason from
Encyclopedia Titanica and distributed by Frank Harrell (Vanderbilt Biostatistics),
https://hbiostat.org/data/repo/titanic3.csv -- 1,309 passengers (crew not included).

Changes:
* keep name, pclass, sex, age, sibsp, parch, fare, cabin, embarked, survived
  (drop ticket, and boat / body / home.dest, which were recorded after the sinking)
* embarked codes spelled out: C -> Cherbourg, Q -> Queenstown, S -> Southampton
* missing values are left missing (age 263, cabin 1,014, embarked 2, fare 1): they are
  Wednesday's topic

Usage: python scripts/make_titanic.py [titanic3.csv]
"""
import sys
from pathlib import Path

import pandas as pd

SRC = "https://hbiostat.org/data/repo/titanic3.csv"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "titanic.csv"

df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else SRC)
df["embarked"] = df["embarked"].map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
df = df[["name", "pclass", "sex", "age", "sibsp", "parch", "fare", "cabin", "embarked", "survived"]]
df.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(df)} rows)")
print(df.isna().sum().to_string())
