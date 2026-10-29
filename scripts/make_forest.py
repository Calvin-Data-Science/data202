"""Build datasets/forest.csv for Reading 9 (logistic regression, multiclass, random forests, boosting).

Source: UCI Machine Learning Repository, "Covertype" (id 31), CC BY 4.0.
    Jock A. Blackard and Denis J. Dean, Colorado State University (donated 1998).
    Blackard, J. A. and D. J. Dean (2000), "Comparative accuracies of artificial neural networks and
    discriminant analysis in predicting forest cover types from cartographic variables,"
    Computers and Electronics in Agriculture 24(3), 131-151.
    https://archive.ics.uci.edu/dataset/31/covertype
    The documentation asks that the copyright notice for Jock A. Blackard and Colorado State
    University be retained: Copyright Jock A. Blackard and Colorado State University.

Each row is one 30 x 30 m plot in four wilderness areas of the Roosevelt National Forest, northern
Colorado; the label is the main tree cover the US Forest Service recorded there. The full file has
581,012 plots, 85% of them spruce/fir or lodgepole pine. Blackard's own training set was its first
11,340 rows, which hold exactly 1,620 plots of each of the 7 cover types; this file takes 500 plots of
each type from those rows (random_state=1), 3,500 in all.

Kept: the 10 map measurements (renamed with units), and the 4 wilderness 0/1 columns turned back into
one word column. Dropped: the 40 soil-type 0/1 columns (codes of the Forest Service's land survey).

Usage:  python scripts/make_forest.py [path/to/covtype.data.gz]
        (without a path, the UCI zip is downloaded)
"""
import gzip
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "forest.csv"
URL = "https://archive.ics.uci.edu/static/public/31/covertype.zip"
NUMBERS = ["elevation_m", "aspect_deg", "slope_deg", "water_dist_m", "water_height_m", "road_dist_m",
           "shade_9am", "shade_noon", "shade_3pm", "fire_dist_m"]
WILDERNESS = ["Rawah", "Neota", "Comanche Peak", "Cache la Poudre"]
SPECIES = {1: "spruce/fir", 2: "lodgepole pine", 3: "ponderosa pine", 4: "cottonwood/willow",
           5: "aspen", 6: "Douglas-fir", 7: "krummholz"}

if len(sys.argv) > 1:
    raw = pd.read_csv(sys.argv[1], header=None, nrows=11_340)
else:
    archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read()))
    raw = pd.read_csv(gzip.open(archive.open("covtype.data.gz")), header=None, nrows=11_340)

plots = raw.iloc[:, :10].set_axis(NUMBERS, axis=1)
plots["wilderness"] = np.array(WILDERNESS)[raw.iloc[:, 10:14].to_numpy().argmax(axis=1)]
plots["species"] = raw.iloc[:, 54].map(SPECIES)
assert (plots["species"].value_counts() == 1_620).all()

forest = plots.groupby("species", group_keys=False).sample(500, random_state=1).sort_index().reset_index(drop=True)
forest.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(forest)} plots)")
print(forest["species"].value_counts().to_string())
