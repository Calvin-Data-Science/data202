"""Build datasets/births.csv for Practice 10 (Week 12: time-series data).

Source: FiveThirtyEight, "U.S. Births" (US_births_2000-2014_SSA.csv), data behind the story
    "Some People Are Too Superstitious To Have A Baby On Friday The 13th"; counts from the
    U.S. Social Security Administration. https://github.com/fivethirtyeight/data/tree/master/births
    CC BY 4.0.

One row per day, January 1, 2000 to December 31, 2014: 5,479 days, none missing.
Columns: date, births (babies born in the United States that day).
The original day_of_week column (1 = Monday) is dropped: the practice builds its own from the date.

Usage:  python scripts/make_births.py [path/to/US_births_2000-2014_SSA.csv]
        (without a path, the file is downloaded from GitHub)
"""
import sys
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "births.csv"
URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv"

raw = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else URL)
dates = pd.to_datetime(dict(year=raw["year"], month=raw["month"], day=raw["date_of_month"]))
assert ((dates.dt.dayofweek + 1) == raw["day_of_week"]).all()

births = pd.DataFrame({"date": dates.dt.strftime("%Y-%m-%d"), "births": raw["births"]})
assert len(births) == 5479 and (dates.diff().dropna() == pd.Timedelta("1D")).all()

births.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(births)} days)")
