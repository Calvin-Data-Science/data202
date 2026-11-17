"""Build datasets/weather.csv for Reading 10 (Week 12: time series and imbalanced data).

Source: NOAA National Centers for Environmental Information, Global Historical Climatology Network
    daily (GHCN-Daily), station USW00094860, Grand Rapids Gerald R. Ford International Airport, Michigan.
    M. J. Menne et al. (2012), "An overview of the Global Historical Climatology Network-Daily
    database," Journal of Atmospheric and Oceanic Technology 29, 897-910; doi:10.7289/V5D21VHZ.
    U.S. government data, public domain.

One row per day, January 1, 2001 to December 31, 2025: 9,131 days, none missing.
(Before 2001 the file has a whole month with no snowfall record, November 1999, and wind
direction only starts in 1996, so the reading uses these 25 complete years.)

GHCN stores metric units (tenths of a degree C, tenths of mm, mm, tenths of m/s). The airport
observes in US units, so converting back and rounding recovers the original numbers:
    high_f, low_f    highest / lowest temperature of the day, degrees Fahrenheit
    precip_in        rain plus melted snow, inches (a "trace" is stored as 0)
    snow_in          new snowfall that day, inches
    snow_depth_in    snow on the ground, inches
    wind_mph         average wind speed, miles per hour (7 days blank: the record is missing)
    wind_dir_deg     direction the day's strongest wind (fastest 2 minutes) came FROM, compass
                     degrees: 90 = east, 180 = south, 270 = west, 360 = north

Usage:  python scripts/make_weather.py [path/to/USW00094860.csv]
        (without a path, the station file is downloaded from NCEI)
"""
import sys
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "weather.csv"
URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/USW00094860.csv"

source = sys.argv[1] if len(sys.argv) > 1 else URL
raw = pd.read_csv(source, parse_dates=["DATE"], low_memory=False)
raw = raw[(raw["DATE"] >= "2001-01-01") & (raw["DATE"] <= "2025-12-31")]

weather = pd.DataFrame({
    "date": raw["DATE"].dt.strftime("%Y-%m-%d"),
    "high_f": (raw["TMAX"] / 10 * 9 / 5 + 32).round().astype(int),
    "low_f": (raw["TMIN"] / 10 * 9 / 5 + 32).round().astype(int),
    "precip_in": (raw["PRCP"] / 254).round(2),
    "snow_in": (raw["SNOW"] / 25.4).round(1),
    "snow_depth_in": (raw["SNWD"] / 25.4).round().astype(int),
    "wind_mph": (raw["AWND"] / 10 * 2.23694).round(1),
    "wind_dir_deg": raw["WDF2"].astype(int),
})

dates = pd.to_datetime(weather["date"])
assert len(weather) == 9131 and (dates.diff().dropna() == pd.Timedelta("1D")).all()
assert weather.drop(columns="wind_mph").notna().all().all() and weather["wind_mph"].isna().sum() == 7

weather.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(weather)} days)")
print(f"days with at least 2 inches of new snow: {(weather['snow_in'] >= 2).sum()}")
