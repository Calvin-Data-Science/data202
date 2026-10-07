"""
Build datasets/autism.csv -- blood metabolites of children with and without
autism, for Week 7 (decision trees, cross-validation, grid search:
weeks/07/class_w07d1.ipynb and class_w07d2.ipynb).

Source: S1 Dataset of Howsmon, Kruger, Melnyk, James & Hahn (2017),
"Classification and adaptive behavior prediction of children with autism
spectrum disorder based upon multivariate data analysis of markers of oxidative
stress and DNA methylation", PLOS Computational Biology 13(3): e1005385,
https://doi.org/10.1371/journal.pcbi.1005385 (CC BY 4.0).
Children aged 3-10 from the Arkansas Children's Hospital Research Institute's
autism IMAGE study.

The only change from the original: its second row (the units of each column,
e.g. uM, nM) is dropped, so the file reads with a plain pd.read_csv.
fGSH, GSSG and tGSH are in micromolar (uM).

Columns: Group (ASD = diagnosed with autism, NEU = neurotypical, SIB =
sibling of an ASD child without a diagnosis), 24 metabolite columns, and
Vineland ABC (a life-skills score, measured for some ASD children only).
206 rows: 83 ASD, 76 NEU, 47 SIB.

Usage:  python scripts/make_autism.py [path/to/pcbi.1005385.s001.csv]
        (with no path, the file is downloaded)
"""

import sys
from pathlib import Path

import pandas as pd

URL = "https://doi.org/10.1371/journal.pcbi.1005385.s001"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "autism.csv"

source = sys.argv[1] if len(sys.argv) > 1 else URL
autism = pd.read_csv(source, skiprows=[1])      # row 1 holds the units
autism.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(autism)} rows;", autism["Group"].value_counts().to_dict())
