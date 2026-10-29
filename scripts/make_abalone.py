"""Build datasets/abalone.csv for Reading 8 (linear regression, MAE/RMSE/R², Ridge and Lasso).

Source: UCI Machine Learning Repository, "Abalone" (id 1), CC BY 4.0.
    Original study: W. J. Nash, T. L. Sellers, S. R. Talbot, A. J. Cawthorn and W. B. Ford (1994),
    "The Population Biology of Abalone (Haliotis species) in Tasmania. I. Blacklip Abalone
    (H. rubra) from the North Coast and Islands of Bass Strait," Sea Fisheries Division,
    Technical Report No. 48. Donated to UCI by Sam Waugh (1995).
    https://archive.ics.uci.edu/dataset/1/abalone

All 4,177 rows are kept, including 4 impossible heights (the reading finds and drops them).
The UCI file stores every measurement divided by 200 (scaled for a neural network); here they are
multiplied back to millimeters and grams. Columns are renamed; sex is spelled out; age_years is
rings + 1.5, as the dataset's documentation says.

Usage:  python scripts/make_abalone.py [path/to/abalone.data]
        (without a path, the UCI zip is downloaded)
"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "abalone.csv"
URL = "https://archive.ics.uci.edu/static/public/1/abalone.zip"
RAW = ["sex", "length_mm", "diameter_mm", "height_mm", "whole_g", "meat_g", "gut_g", "shell_g", "rings"]

if len(sys.argv) > 1:
    abalone = pd.read_csv(sys.argv[1], header=None, names=RAW)
else:
    archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read()))
    abalone = pd.read_csv(archive.open("abalone.data"), header=None, names=RAW)

for col in RAW[1:8]:
    abalone[col] = (abalone[col] * 200).round(1)            # undo the ÷200 scaling: mm and grams
abalone["sex"] = abalone["sex"].map({"M": "male", "F": "female", "I": "infant"})
abalone["age_years"] = abalone["rings"] + 1.5

abalone.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(abalone)} abalone); heights of 0 mm: {(abalone['height_mm'] == 0).sum()}, "
      f"over 60 mm: {(abalone['height_mm'] > 60).sum()}")
