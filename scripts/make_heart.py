"""
Build datasets/heart.csv -- the South African Heart Disease data for Reading 5
(Week 6, kNN classification, train/test split, metrics, weeks/06/reading5.md).

Source: the "SAheart" dataset from Hastie, Tibshirani & Friedman, The Elements
of Statistical Learning (2nd ed., 2009), taken from a larger study described in
Rousseauw et al. (1983), South African Medical Journal:
https://hastie.su.domains/ElemStatLearn/datasets/SAheart.data
Its description: "A retrospective sample of males in a heart-disease high-risk
region of the Western Cape, South Africa. There are roughly two controls per
case of CHD. Many of the CHD positive men have undergone blood pressure
reduction treatment and other programs to reduce their risk factors after
their CHD event. In some cases the measurements were made after these
treatments."

The only change from the original: the unnamed row-number column is dropped.

Columns: sbp, tobacco, ldl, adiposity, famhist ("Present"/"Absent"), typea,
obesity, alcohol, age, chd (1 = coronary heart disease, 0 = none).
462 rows, 160 with chd = 1.

Usage:  python scripts/make_heart.py [path/to/SAheart.data]
        (with no path, the file is downloaded)
"""

import sys
from pathlib import Path

import pandas as pd

URL = "https://hastie.su.domains/ElemStatLearn/datasets/SAheart.data"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "heart.csv"

source = sys.argv[1] if len(sys.argv) > 1 else URL
heart = pd.read_csv(source).drop(columns="row.names")
heart.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(heart)} rows, {heart['chd'].sum()} with chd = 1")
