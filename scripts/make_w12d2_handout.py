"""
Build weeks/12/class_w12d2_handout.pdf -- the printed in-class activities for
Week 12 Wednesday (time-series data) -- from its editable source,
weeks/12/class_w12d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
hours and models as the notebook (datasets/bikes.csv; time split: learn before
2012-07-01, test July-December 2012; RandomForestRegressor(random_state=1)).

    week      bikes rented each hour, Monday Sept 10 to Sunday Sept 16, 2012
    forecast  bikes per day, July-December 2012: actual vs. a forest on clock + weather (no lags)
    circle    left: the 24 hours on a circle (hour_sin, hour_cos); right, noon to noon: the average rentals
              at each hour (Jan 2011-Jun 2012) and two linear regressions on the hour alone, line A with the
              circle, line B with the hour as a number (it jumps at midnight)
    rolling   the daily rentals, and TimeSeriesSplit(5)'s folds on Jan 2011-Jun 2012: fold 1 drawn, folds
              2-5 left for students; each fold's MAE (forest on clock + weather + lags) at the right

Usage:  python scripts/make_w12d2_handout.py   (about 30 seconds)
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "12" / "class_w12d2_handout.md"
OUT_PDF = ROOT / "weeks" / "12" / "class_w12d2_handout.pdf"
CLOCK_WEATHER = ["hour", "day_of_week", "holiday", "temp_c", "humidity", "weather"]
LAGS = ["rentals_1h_ago", "rentals_24h_ago", "rentals_1wk_ago", "mean_last_24h"]
LEARN, CHECK = "#2a78d6", "#eb6834"

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
    fig, ax = plt.subplots(figsize=(7.4, 1.95))
    ax.plot(week["time"], week["rentals"], color=LEARN, lw=1.5)
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
    fig, ax = plt.subplots(figsize=(7.4, 1.75))
    ax.plot(daily.index, daily["rentals"], color=LEARN, lw=1.3, label="what happened")
    ax.plot(daily.index, daily["predicted"], color=CHECK, lw=1.6, ls="--", label="forecast (no lags)")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%B"))
    ax.set_xlim(daily.index[0] - pd.Timedelta(days=1), daily.index[-1] + pd.Timedelta(days=1))
    ax.set_ylim(0, 9000)
    ax.set_ylabel("bikes per day, 2012")
    ax.legend(loc="lower left", fontsize=7.5, ncol=2)
    plots["forecast"] = outdir / "forecast.pdf"
    save(fig, plots["forecast"])

    # same rows as the notebook from Part 2 on: lags computed, the first week dropped
    y_all = bikes["rentals"]
    bikes["rentals_1h_ago"] = y_all.shift(1)
    bikes["rentals_24h_ago"] = y_all.shift(24)
    bikes["rentals_1wk_ago"] = y_all.shift(168)
    bikes["mean_last_24h"] = y_all.shift(1).rolling(24).mean()
    bikes = bikes.dropna().copy()
    bikes["hour_sin"] = np.sin(2 * np.pi * bikes["hour"] / 24)
    bikes["hour_cos"] = np.cos(2 * np.pi * bikes["hour"] / 24)
    y = bikes["rentals"]
    train = bikes["time"] < "2012-07-01"
    test = ~train

    # circle: the clock on a circle, and two straight-line models noon to noon
    fig, (ax_c, ax_l) = plt.subplots(1, 2, figsize=(7.4, 1.75), gridspec_kw={"width_ratios": [1, 2.9]})
    angle = np.linspace(0, 2 * np.pi, 200)
    ax_c.plot(np.sin(angle), np.cos(angle), color="#cccccc", lw=0.8)
    for h in range(24):
        a = 2 * np.pi * h / 24
        ax_c.scatter(np.sin(a), np.cos(a), s=14, color=LEARN, zorder=3)
        ax_c.text(1.25 * np.sin(a), 1.25 * np.cos(a), str(h), ha="center", va="center", fontsize=6.5)
    ax_c.set_aspect("equal")
    ax_c.set_xlim(-1.45, 1.45)
    ax_c.set_ylim(-1.45, 1.45)
    ax_c.set_xticks([-1, 0, 1])
    ax_c.set_yticks([-1, 0, 1])
    ax_c.tick_params(labelsize=7)
    ax_c.set_xlabel("hour_sin", fontsize=8)
    ax_c.set_ylabel("hour_cos", fontsize=8)
    ax_c.grid(visible=False)

    by_hour = bikes[train].groupby("hour")["rentals"].mean()
    clock = pd.DataFrame({"hour": range(24)})
    clock["hour_sin"] = np.sin(2 * np.pi * clock["hour"] / 24)
    clock["hour_cos"] = np.cos(2 * np.pi * clock["hour"] / 24)
    order = list(range(12, 24)) + list(range(12))                     # noon to noon: midnight in the middle
    lines = {}
    for name, columns in [("A", ["hour_sin", "hour_cos"]), ("B", ["hour"])]:
        line = LinearRegression().fit(bikes.loc[train, columns], y[train])
        lines[name] = line.predict(clock[columns])
        print(f"line {name} {columns}: test MAE {mean_absolute_error(y[test], line.predict(bikes.loc[test, columns])):.0f};"
              f" 11 pm {lines[name][23]:.0f}, midnight {lines[name][0]:.0f}")
    x = np.arange(24)
    ax_l.bar(x, by_hour.loc[order].values, color="#d9d9d9", width=0.8, label="average rentals")
    ax_l.plot(x, lines["A"][order], color=CHECK, lw=2, marker="o", ms=3, label="line A")
    ax_l.plot(x, lines["B"][order], color="#1f4e99", lw=2, ls="--", marker="s", ms=3, label="line B")
    ax_l.set_xticks([0, 3, 6, 9, 12, 15, 18, 21])
    ax_l.set_xticklabels(["noon", "3 pm", "6 pm", "9 pm", "midnight", "3 am", "6 am", "9 am"], fontsize=7)
    ax_l.set_xlim(-0.6, 23.6)
    ax_l.set_ylabel("bikes per hour")
    ax_l.legend(loc="upper right", fontsize=7)
    ax_l.grid(axis="x", visible=False)
    plots["circle"] = outdir / "circle.pdf"
    save(fig, plots["circle"])

    # rolling: TimeSeriesSplit's folds on the 18 months before the test
    X_dev, y_dev = bikes.loc[train], y[train]
    features = CLOCK_WEATHER + LAGS
    folds = []
    for learn, check in TimeSeriesSplit(n_splits=5).split(X_dev):
        forest.fit(X_dev[features].iloc[learn], y_dev.iloc[learn])
        mae = mean_absolute_error(y_dev.iloc[check], forest.predict(X_dev[features].iloc[check]))
        folds.append((X_dev["time"].iloc[learn[0]], X_dev["time"].iloc[check[0]], X_dev["time"].iloc[check[-1]], mae))
    print("fold MAEs:", [round(f[3]) for f in folds])
    dev_daily = X_dev.resample("D", on="time")["rentals"].sum()
    fig, (ax_s, ax_f) = plt.subplots(2, 1, figsize=(7.4, 2.0), sharex=True, gridspec_kw={"height_ratios": [0.85, 1.5]})
    ax_s.plot(dev_daily.index, dev_daily.values, color="#555555", lw=0.9)
    ax_s.set_ylim(0, 9000)
    ax_s.set_yticks([0, 4000, 8000])
    ax_s.set_ylabel("per day", fontsize=7.5)
    ax_s.grid(axis="x", visible=False)
    edges = [folds[0][0]] + [f[1] for f in folds] + [folds[-1][2] + pd.Timedelta(hours=1)]
    for ax in (ax_s, ax_f):
        for edge in edges:
            ax.axvline(edge, color="#aaaaaa", lw=0.6, ls=":")
    for k, (start, check_start, check_end, mae) in enumerate(folds):
        lane = 5 - k
        ax_f.add_patch(plt.Rectangle((mdates.date2num(edges[0]), lane - 0.34),
                                     mdates.date2num(edges[-1]) - mdates.date2num(edges[0]), 0.68,
                                     facecolor="none", edgecolor="#dddddd", lw=0.6))
        ax_f.text(1.01, (lane - 0.4) / 5.2, f"MAE {mae:.0f}", transform=ax_f.transAxes, fontsize=8, va="center")
    start, check_start, check_end, _ = folds[0]
    ax_f.add_patch(plt.Rectangle((mdates.date2num(start), 5 - 0.34), mdates.date2num(check_start) - mdates.date2num(start),
                                 0.68, facecolor=LEARN, alpha=0.35, edgecolor=LEARN))
    ax_f.add_patch(plt.Rectangle((mdates.date2num(check_start), 5 - 0.34),
                                 mdates.date2num(check_end) - mdates.date2num(check_start), 0.68,
                                 facecolor="white", edgecolor=CHECK, lw=1.6, hatch="////"))
    ax_f.text(mdates.date2num(start) + 45, 5, "learn", ha="center", va="center", fontsize=7.5)
    ax_f.text(mdates.date2num(check_start) + 45, 5, "check", ha="center", va="center", fontsize=7.5,
              bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
    ax_f.set_ylim(0.4, 5.6)
    ax_f.set_yticks([5, 4, 3, 2, 1])
    ax_f.set_yticklabels([f"fold {k}" for k in range(1, 6)], fontsize=8)
    ax_f.grid(visible=False)
    ax_f.set_xlim(mdates.date2num(edges[0]) - 4, mdates.date2num(edges[-1]) + 4)
    ax_f.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax_f.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax_f.tick_params(axis="x", labelsize=7.5)
    for side in ["top", "right"]:
        ax_f.spines[side].set_visible(False)
    plots["rolling"] = outdir / "rolling.pdf"
    save(fig, plots["rolling"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
