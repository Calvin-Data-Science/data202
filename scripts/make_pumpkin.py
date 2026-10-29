"""Build datasets/pumpkin.csv for Week 11 (logistic regression; ensembles).

Source: M. Koklu, S. Sarigil and O. Ozbek (2021), "The use of machine learning methods in
    classification of pumpkin seeds (Cucurbita pepo L.)," Genetic Resources and Crop Evolution
    68(7), 2713-2726, doi:10.1007/s10722-021-01226-0. Data shared by the authors at
    https://www.muratkoklu.com/datasets/ (Pumpkin_Seeds_Dataset.xlsx).

2,500 seeds of two Turkish varieties, 1,300 "Çerçevelik" and 1,200 "Ürgüp Sivrisi", each
photographed and measured from the image (lengths in pixels, areas in square pixels).
No missing values. Columns are renamed to snake_case; Major_Axis_Length / Minor_Axis_Length
become length / width (the long and short axes of the ellipse fitted to the seed), and
Aspect_Ration (sic) becomes aspect_ratio (= length / width). Class becomes variety.

Usage:  python scripts/make_pumpkin.py [path/to/Pumpkin_Seeds_Dataset.xlsx]
        (without a path, the copy on the old course site is downloaded)
"""
import io
import sys
import urllib.request
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "pumpkin.csv"
URL = "https://cs.calvin.edu/courses/data/202/fsantos/datasets/pumpkin.xlsx"
NAMES = {"Area": "area", "Perimeter": "perimeter", "Major_Axis_Length": "length", "Minor_Axis_Length": "width",
         "Convex_Area": "convex_area", "Equiv_Diameter": "equiv_diameter", "Eccentricity": "eccentricity",
         "Solidity": "solidity", "Extent": "extent", "Roundness": "roundness", "Aspect_Ration": "aspect_ratio",
         "Compactness": "compactness", "Class": "variety"}

source = sys.argv[1] if len(sys.argv) > 1 else io.BytesIO(urllib.request.urlopen(URL).read())
seeds = pd.read_excel(source).rename(columns=NAMES)
assert list(seeds.columns) == list(NAMES.values()) and seeds.notna().all().all()

seeds.to_csv(OUT, index=False, encoding="utf-8")
print(f"wrote {OUT} ({len(seeds)} seeds)")
print(seeds["variety"].value_counts().to_string())
