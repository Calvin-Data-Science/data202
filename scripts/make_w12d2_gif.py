"""
Build weeks/12/images/rolling_window.gif, the animation in class_w12d2.ipynb's Part 4: TimeSeriesSplit's
rolling window on the bike data, one fold per frame, then the real test.

Same rows, features and forest as the notebook: datasets/bikes.csv with the lags (first week dropped),
clock + weather + lags, RandomForestRegressor(random_state=1); TimeSeriesSplit(n_splits=5) on the hours
before July 2012 (fold MAEs 55, 30, 23, 31, 42), then learn all of them and check July-December 2012 (33).

Each frame: on top, bikes per day with the stretch the forest learns from (blue) and the 90 days it checks
(orange: what happened, and the forecast dashed); below, the folds so far as lanes, like the handout's Part 4.

Usage:  python scripts/make_w12d2_gif.py   (about 30 seconds)
"""

import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "weeks" / "12" / "images" / "rolling_window.gif"
FEATURES = ["hour", "day_of_week", "holiday", "temp_c", "humidity", "weather",
            "rentals_1h_ago", "rentals_24h_ago", "rentals_1wk_ago", "mean_last_24h"]
LEARN, CHECK, TEST = "#2a78d6", "#eb6834", "#888888"
START, END = pd.Timestamp("2011-01-01"), pd.Timestamp("2013-01-01")


def day(t):
    return f"{t:%b} {t.day}, {t.year}"


bikes = pd.read_csv(ROOT / "datasets" / "bikes.csv", parse_dates=["time"])
bikes["hour"] = bikes["time"].dt.hour
bikes["day_of_week"] = bikes["time"].dt.dayofweek
bikes["rentals_1h_ago"] = bikes["rentals"].shift(1)
bikes["rentals_24h_ago"] = bikes["rentals"].shift(24)
bikes["rentals_1wk_ago"] = bikes["rentals"].shift(168)
bikes["mean_last_24h"] = bikes["rentals"].shift(1).rolling(24).mean()
bikes = bikes.dropna().reset_index(drop=True)
y = bikes["rentals"]
train = bikes["time"] < "2012-07-01"
dev = bikes[train]
forest = RandomForestRegressor(random_state=1, n_jobs=-1)
daily = bikes.resample("D", on="time")["rentals"].sum()

# each step: (rows learned from, rows checked) as positions in bikes; the five folds, then the real test
steps = [(learn, check) for learn, check in TimeSeriesSplit(n_splits=5).split(dev)]
steps.append((dev.index.to_numpy(), bikes.index[~train].to_numpy()))
results = []
for learn, check in steps:
    forest.fit(bikes.loc[learn, FEATURES], y[learn])
    predicted = pd.Series(forest.predict(bikes.loc[check, FEATURES]), index=bikes.loc[check, "time"])
    results.append({"learn_start": bikes.loc[learn[0], "time"], "check_start": bikes.loc[check[0], "time"],
                    "check_end": bikes.loc[check[-1], "time"] + pd.Timedelta(hours=1),
                    "mae": mean_absolute_error(y[check], predicted.values),
                    "forecast": predicted.resample("D").sum()})
print("MAEs:", [round(r["mae"]) for r in results])

frames = []
for k in range(len(results) + 1):                 # frame 0: the empty lanes
    fig, (ax, lanes) = plt.subplots(2, 1, figsize=(9, 4.9), dpi=100, sharex=True,
                                    gridspec_kw={"height_ratios": [1.5, 1.25], "hspace": 0.12})
    current = results[k - 1] if k else None
    ax.plot(daily.index, daily.values, color="#b5b5b5", lw=0.8)
    test_start = results[-1]["check_start"]
    if k < len(results):
        ax.axvspan(test_start, END, color=TEST, alpha=0.12, lw=0)
        ax.text(test_start + (END - test_start) / 2, 9900, "test (locked)", ha="center", va="top", fontsize=10, color="#555555")
    if current is not None:
        ax.axvspan(current["learn_start"], current["check_start"], color=LEARN, alpha=0.15, lw=0)
        ax.axvspan(current["check_start"], current["check_end"], color=CHECK, alpha=0.15, lw=0)
        ax.text(current["learn_start"] + (current["check_start"] - current["learn_start"]) / 2, 9900, "learn",
                ha="center", va="top", fontsize=11, color=LEARN, fontweight="bold")
        ax.text(current["check_start"] + (current["check_end"] - current["check_start"]) / 2, 9900, "check",
                ha="center", va="top", fontsize=11, color=CHECK, fontweight="bold")
        shown = daily[(daily.index >= current["check_start"]) & (daily.index < current["check_end"])]
        ax.plot(shown.index, shown.values, color="#222222", lw=1.3, label="what happened")
        ax.plot(current["forecast"].index, current["forecast"].values, color=CHECK, lw=1.6, ls="--", label="forecast")
        ax.legend(loc="lower right", fontsize=9, ncol=2, frameon=False)
    ax.set_ylim(0, 10000)
    ax.set_ylabel("bikes per day")
    ax.spines[["top", "right"]].set_visible(False)

    for j, r in enumerate(results):
        lane = len(results) - j
        done = j < k
        alpha = 1.0 if j == k - 1 else 0.35
        lanes.barh(lane, (r["check_end"] - r["check_start"]).days, left=mdates.date2num(r["check_start"]), height=0.62,
                   color=CHECK if done else "none", alpha=alpha if done else 1, edgecolor="#dddddd" if not done else CHECK)
        lanes.barh(lane, (r["check_start"] - r["learn_start"]).days, left=mdates.date2num(r["learn_start"]), height=0.62,
                   color=LEARN if done else "none", alpha=alpha if done else 1, edgecolor="#dddddd" if not done else LEARN)
        if done:
            lanes.text(mdates.date2num(r["check_end"]) + 6, lane, f"MAE {r['mae']:.0f}", va="center", fontsize=10,
                       fontweight="bold" if j == k - 1 else "normal", color="#222222" if j == k - 1 else "#777777")
    lanes.set_yticks(range(len(results), 0, -1))
    lanes.set_yticklabels([f"fold {j}" for j in range(1, len(results))] + ["test"])
    lanes.set_ylim(0.4, len(results) + 0.6)
    lanes.set_xlim(START, END)
    lanes.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    lanes.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    lanes.spines[["top", "right"]].set_visible(False)

    if k == 0:
        title, subtitle = "TimeSeriesSplit(n_splits=5): replay the past", "learn from everything before a date, check the next 90 days, move the date forward"
    elif k < len(results):
        title = f"Fold {k} of 5:  MAE {current['mae']:.0f} bikes per hour"
        subtitle = (f"learn {day(current['learn_start'])} to {day(current['check_start'] - pd.Timedelta(hours=1))}, "
                    f"then check the next 90 days")
    else:
        title = f"The real future:  MAE {current['mae']:.0f} bikes per hour"
        subtitle = "learn everything before July 2012, then check July to December 2012"
    fig.text(0.1, 0.965, title, fontsize=12.5, fontweight="bold", ha="left", va="top")
    fig.text(0.1, 0.915, subtitle, fontsize=10.5, ha="left", va="top", color="#444444")
    fig.subplots_adjust(left=0.1, right=0.89, top=0.86, bottom=0.08)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    frames.append(Image.open(buffer).convert("RGB").quantize(colors=64, method=Image.Quantize.MEDIANCUT))

durations = [1800] + [2600] * (len(results) - 1) + [4500]
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {len(frames)} frames)")
