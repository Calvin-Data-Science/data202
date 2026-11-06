"""Build datasets/mpg.csv for Practice 08 (linear regression, MAE/RMSE/R², Ridge, Lasso and elastic net).

Source: UCI Machine Learning Repository, "Auto MPG" (id 9), CC BY 4.0.
    From the StatLib library at Carnegie Mellon University; used in the 1983 American Statistical
    Association Exposition, and by R. Quinlan (1993), "Combining Instance-Based and Model-Based
    Learning," Proceedings of the Tenth International Conference on Machine Learning, 236-243.
    https://archive.ics.uci.edu/dataset/9/auto+mpg

398 cars, model years 1970-1982. "The data concerns city-cycle fuel consumption in miles per gallon"
(Quinlan 1993). The 6 blank horsepower values ("?" in the UCI file) are kept as blanks.
Columns are renamed; model years become 1970-1982; origin is spelled out (1 USA, 2 Europe, 3 Japan).

Usage:  python scripts/make_mpg.py [path/to/auto+mpg.zip or auto-mpg.data]
        (without a path, the UCI zip is downloaded)
"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "mpg.csv"
URL = "https://archive.ics.uci.edu/static/public/9/auto+mpg.zip"
RAW = ["mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration", "model_year", "origin", "name"]

if len(sys.argv) > 1 and not sys.argv[1].endswith(".zip"):
    source = open(sys.argv[1], "rb")
else:
    data = open(sys.argv[1], "rb").read() if len(sys.argv) > 1 else urllib.request.urlopen(URL).read()
    source = zipfile.ZipFile(io.BytesIO(data)).open("auto-mpg.data")
cars = pd.read_csv(source, sep=r"\s+", header=None, names=RAW, na_values="?", quotechar='"')

cars["model_year"] = cars["model_year"] + 1900
cars["origin"] = cars["origin"].map({1: "USA", 2: "Europe", 3: "Japan"})
cars["weight"] = cars["weight"].astype(int)
cars = cars[["name", "origin", "model_year", "cylinders", "displacement", "horsepower", "weight", "acceleration", "mpg"]]

cars.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(cars)} cars); blank horsepower: {cars['horsepower'].isna().sum()}")
