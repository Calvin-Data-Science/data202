"""Build datasets/ames.csv for Week 10 (linear regression, Ridge and Lasso).

Source: the Ames, Iowa housing data (De Cock 2011, Journal of Statistics Education 19(3)),
from the Ames City Assessor's Office: 2,930 residential sales, 2006-2010.
https://jse.amstat.org/v19n3/decock/AmesHousing.txt

Changes:
* remove the 5 houses with more than 4,000 sq ft of living area, as De Cock recommends
  (3 partial sales that don't reflect market value, 2 very large houses) -> 2,925 sales
* keep 20 columns, renamed in snake_case; neighborhood codes spelled out
* missing values are left missing (mas_vnr_area 23, total_bsmt_sf 1, garage_cars 1,
  garage_area 1): the pipelines impute them, as in Week 9

Usage: python scripts/make_ames.py [AmesHousing.txt]
"""
import sys
from pathlib import Path

import pandas as pd

SRC = "https://jse.amstat.org/v19n3/decock/AmesHousing.txt"
OUT = Path(__file__).resolve().parent.parent / "datasets" / "ames.csv"

COLUMNS = {
    "Neighborhood": "neighborhood",
    "Gr Liv Area": "living_area",          # above-ground living area, sq ft
    "Lot Area": "lot_area",                # sq ft
    "Overall Qual": "quality",             # overall material and finish, 1-10
    "Overall Cond": "condition",           # overall condition, 1-10
    "Year Built": "year_built",
    "Year Remod/Add": "year_remodeled",
    "Total Bsmt SF": "basement_area",
    "1st Flr SF": "first_floor_area",
    "2nd Flr SF": "second_floor_area",
    "Full Bath": "full_baths",
    "Half Bath": "half_baths",
    "Bedroom AbvGr": "bedrooms",
    "TotRms AbvGrd": "rooms",              # rooms above ground, not counting bathrooms
    "Fireplaces": "fireplaces",
    "Garage Cars": "garage_cars",
    "Garage Area": "garage_area",
    "Wood Deck SF": "deck_area",
    "Open Porch SF": "porch_area",
    "Mas Vnr Area": "masonry_area",        # masonry veneer
    "Yr Sold": "year_sold",
    "SalePrice": "price",
}
NEIGHBORHOODS = {
    "Blmngtn": "Bloomington Heights", "Blueste": "Bluestem", "BrDale": "Briardale", "BrkSide": "Brookside",
    "ClearCr": "Clear Creek", "CollgCr": "College Creek", "Crawfor": "Crawford", "Edwards": "Edwards",
    "Gilbert": "Gilbert", "Greens": "Greens", "GrnHill": "Green Hills", "IDOTRR": "Iowa DOT and Rail Road",
    "Landmrk": "Landmark", "MeadowV": "Meadow Village", "Mitchel": "Mitchell", "NAmes": "North Ames",
    "NoRidge": "Northridge", "NPkVill": "Northpark Villa", "NridgHt": "Northridge Heights",
    "NWAmes": "Northwest Ames", "OldTown": "Old Town", "SWISU": "South & West of ISU", "Sawyer": "Sawyer",
    "SawyerW": "Sawyer West", "Somerst": "Somerset", "StoneBr": "Stone Brook", "Timber": "Timberland",
    "Veenker": "Veenker",
}

df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else SRC, sep="\t")
df = df[df["Gr Liv Area"] <= 4000]
df = df[list(COLUMNS)].rename(columns=COLUMNS)
df["neighborhood"] = df["neighborhood"].map(NEIGHBORHOODS)
assert df["neighborhood"].notna().all()
df.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(df)} rows)")
print(df.isna().sum()[df.isna().sum() > 0].to_string())
