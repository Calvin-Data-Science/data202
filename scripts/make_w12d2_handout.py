"""
Build weeks/12/class_w12d2_handout.pdf -- the printed in-class activities for
Week 12 Wednesday (time-series data) -- from its editable source,
weeks/12/class_w12d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
hours and models as the notebook (datasets/bikes.csv; time split: learn before
2012-07-01, test July-December 2012; RandomForestRegressor(random_state=1)).

    week      bikes rented each hour, Monday Sept 10 to Sunday Sept 16, 2012
    forecast  bikes per day, July-December 2012: actual vs. a forest on clock + weather (no lags)
    horizon   test MAE by hours ahead (1 to 168): clock + weather + the newest known rentals + same hour last week

Usage:  python scripts/make_w12d2_handout.py   (about 30 seconds)
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "12" / "class_w12d2_handout.md"
OUT_PDF = ROOT / "weeks" / "12" / "class_w12d2_handout.pdf"
CLOCK_WEATHER = ["hour", "day_of_week", "holiday", "temp_c", "humidity", "weather"]
HORIZONS = [1, 2, 3, 6, 12, 24, 48, 72, 168]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    bikes = pd.read_csv(ROOT / "datasets" / "bikes.csv", parse_dates=["time"])
    bikes["hour"] = bikes["time"].dt.hour
    bikes["day_of_week"] = bikes["time"].dt.dayofweek
    plots = {}

    # week
    week = bikes[(bikes["time"] >= "2012-09-10") & (bikes["time"] < "2012-09-17")]
    fig, ax = plt.subplots(figsize=(7.4, 2.4))
    ax.plot(week["time"], week["rentals"], color="#2a78d6", lw=1.5)
    ax.set_xlim(pd.Timestamp("2012-09-10"), pd.Timestamp("2012-09-16 23:59"))
    ax.set_ylim(0, 1000)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %b %d"))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[6, 12, 18]))
    ax.grid(which="minor", color="#eeeeee", linewidth=0.5)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("left")
    ax.set_ylabel("bikes rented per hour")
    plots["week"] = outdir / "week.pdf"
    save(fig, plots["week"])

    # forecast
    forest = RandomForestRegressor(random_state=1, n_jobs=-1)
    train = bikes["time"] < "2012-07-01"
    test = ~train
    forest.fit(bikes.loc[train, CLOCK_WEATHER], bikes.loc[train, "rentals"])
    results = bikes.loc[test, ["time", "rentals"]].assign(predicted=forest.predict(bikes.loc[test, CLOCK_WEATHER]))
    daily = results.resample("D", on="time").sum()
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.plot(daily.index, daily["rentals"], color="#2a78d6", lw=1.3, label="what happened")
    ax.plot(daily.index, daily["predicted"], color="#eb6834", lw=1.6, ls="--", label="forecast (no lags)")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_ylim(0, 9000)
    ax.set_ylabel("bikes per day, 2012")
    ax.legend(loc="lower left", fontsize=7.5)
    plots["forecast"] = outdir / "forecast.pdf"
    save(fig, plots["forecast"])

    # horizon (same rows as the notebook's Part 5: lags computed, the first week dropped)
    bikes["rentals_1wk_ago"] = bikes["rentals"].shift(168)
    bikes = bikes.iloc[168:]
    train = bikes["time"] < "2012-07-01"
    test = ~train
    y = bikes["rentals"]
    maes = []
    for h in HORIZONS:
        X_h = bikes[CLOCK_WEATHER].copy()
        X_h["latest_known"] = bikes["rentals"].shift(h)
        X_h["same_hour_last_week"] = bikes["rentals"].shift(168)
        keep = X_h.notna().all(axis=1)
        forest.fit(X_h[train & keep], y[train & keep])
        maes.append(mean_absolute_error(y[test], forest.predict(X_h[test])))
    print("horizon MAEs:", [round(m, 1) for m in maes])
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.plot(HORIZONS, maes, color="#2a78d6", lw=1.8, marker="o", ms=4)
    ax.set_xscale("log")
    ax.set_xticks(HORIZONS)
    ax.set_xticklabels([str(h) for h in HORIZONS])
    ax.minorticks_off()
    ax.set_ylim(0, 70)
    ax.set_xlabel("hours ahead (log scale; 24 = a day, 168 = a week)")
    ax.set_ylabel("test MAE (bikes per hour)")
    plots["horizon"] = outdir / "horizon.pdf"
    save(fig, plots["horizon"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
