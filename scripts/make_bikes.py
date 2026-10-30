"""Build datasets/bikes.csv for Week 12 Wednesday (time-series data).

Source: H. Fanaee-T (2013), "Bike Sharing," UCI Machine Learning Repository, doi:10.24432/C5W894, CC BY 4.0.
    Paper: H. Fanaee-T and J. Gama (2013), "Event labeling combining ensemble detectors and background
    knowledge," Progress in Artificial Intelligence 2, 113-127.
    Rentals: Capital Bikeshare, Washington, D.C.; weather: freemeteo.com.

One row per hour, 2011-01-01 00:00 to 2012-12-31 23:00 (17,544 hours = 731 days x 24):
    time         the hour, "YYYY-MM-DD HH:00"
    rentals      bikes rented during that hour (casual + registered)
    temp_c       temperature in degrees C   (UCI's normalized temp x 47 - 8, as the UCI page documents)
    humidity     relative humidity in %
    weather      1 = clear or partly cloudy, 2 = mist or cloudy, 3 = light rain or snow, 4 = heavy rain or snow
    holiday      1 = a public holiday in D.C.

UCI's hour.csv has 17,379 rows: 165 hours have no row, and the smallest count in the file is 1, so an hour
with no rentals got no row. Most missing hours are at night (2-5 am); five longer gaps (6 to 36 hours) fall
on storm days, the longest being Hurricane Sandy (Oct 29-30, 2012). So the missing hours are added back with
rentals = 0, and their weather is carried forward from the previous hour. That way every row is exactly one
hour after the one above it, which lag features (shift) rely on.

Usage:  python scripts/make_bikes.py [path/to/hour.csv]
        (without a path, the UCI zip is downloaded)
"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "bikes.csv"
URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"

if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read()))
    source = io.BytesIO(archive.read("hour.csv"))

raw = pd.read_csv(source)
assert len(raw) == 17379
raw["time"] = pd.to_datetime(raw["dteday"]) + pd.to_timedelta(raw["hr"], unit="h")

bikes = pd.DataFrame({
    "time": raw["time"],
    "rentals": raw["cnt"],
    "temp_c": (raw["temp"] * 47 - 8).round(1),
    "humidity": (raw["hum"] * 100).round().astype(int),
    "weather": raw["weathersit"],
    "holiday": raw["holiday"],
})

every_hour = pd.DataFrame({"time": pd.date_range("2011-01-01 00:00", "2012-12-31 23:00", freq="h")})
bikes = every_hour.merge(bikes, on="time", how="left")
missing = bikes["rentals"].isna()
bikes["rentals"] = bikes["rentals"].fillna(0).astype(int)
bikes[["temp_c", "humidity", "weather"]] = bikes[["temp_c", "humidity", "weather"]].ffill()
bikes["holiday"] = bikes.groupby(bikes["time"].dt.date)["holiday"].transform("max")   # same for the whole day
bikes[["humidity", "weather", "holiday"]] = bikes[["humidity", "weather", "holiday"]].astype(int)
assert len(bikes) == 17544 and bikes.notna().all().all()

bikes["time"] = bikes["time"].dt.strftime("%Y-%m-%d %H:%M")
bikes.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(bikes)} hours, {missing.sum()} added back with 0 rentals)")
