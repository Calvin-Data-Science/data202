"""
Build weeks/10/class_w10d1_handout.pdf -- the printed in-class activities for
Week 10 Monday (linear regression, MAE / RMSE / R²) -- from its editable source,
weeks/10/class_w10d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
houses and split as the notebook (datasets/ames.csv, train_test_split(test_size=0.25,
random_state=1)).

    scatter    price vs. living area for the 2,193 training houses, on a grid to draw a line
    overunder  average percentage error by price fifth (test houses), for the one-line model
               and the 47-column pipeline

Usage:  python scripts/make_w10d1_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "10" / "class_w10d1_handout.md"
OUT_PDF = ROOT / "weeks" / "10" / "class_w10d1_handout.pdf"

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    ames = pd.read_csv(ROOT / "datasets" / "ames.csv")
    X, y = ames.drop(columns="price"), ames["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    plots = {}

    # scatter -- training houses on a grid
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.scatter(X_train["living_area"], y_train / 1000, s=5, color="#2a78d6", alpha=0.45, linewidths=0)
    ax.set_xlim(0, 4000); ax.set_ylim(0, 650)
    ax.set_xticks(range(0, 4001, 500)); ax.set_yticks(range(0, 651, 50))
    ax.grid(True, color="#e2e2e2", linewidth=0.5)
    ax.set_xlabel("living area (sq ft)"); ax.set_ylabel("sale price ($1000s)")
    plots["scatter"] = outdir / "scatter.pdf"; save(fig, plots["scatter"])

    # overunder -- percentage error by price fifth
    line = LinearRegression().fit(X_train[["living_area"]], y_train)
    numeric = [c for c in X.columns if c not in ("neighborhood", "year_sold")]
    model = Pipeline([("prep", ColumnTransformer([("num", SimpleImputer(strategy="median"), numeric),
                                                  ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"])])),
                      ("line", LinearRegression())]).fit(X_train, y_train)
    groups = pd.qcut(y_test, 5, labels=["cheapest", "2nd", "3rd", "4th", "priciest"])
    one = ((line.predict(X_test[["living_area"]]) - y_test) / y_test * 100).groupby(groups, observed=True).mean()
    full = ((model.predict(X_test) - y_test) / y_test * 100).groupby(groups, observed=True).mean()
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    pos = np.arange(5)
    b1 = ax.bar(pos - 0.2, one.values, width=0.38, color="#eb6834", label="one line (living area)", hatch="////",
                edgecolor="white")
    b2 = ax.bar(pos + 0.2, full.values, width=0.38, color="#2a78d6", label="all 47 columns")
    for bars in (b1, b2):
        for bar in bars:
            v = bar.get_height()
            label = "0%" if abs(v) < 0.5 else f"{v:+.0f}%"
            ax.text(bar.get_x() + bar.get_width() / 2, v + (2 if v >= 0 else -6), label, ha="center", fontsize=8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(pos); ax.set_xticklabels(one.index)
    ax.set_ylim(-25, 60); ax.set_ylabel("average error (%)")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right", fontsize=8)
    plots["overunder"] = outdir / "overunder.pdf"; save(fig, plots["overunder"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
