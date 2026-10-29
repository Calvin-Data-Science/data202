"""
Build weeks/10/class_w10d2_handout.pdf -- the printed in-class activities for
Week 10 Wednesday (Ridge and Lasso) -- from its editable source,
weeks/10/class_w10d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
30 houses as the notebook (datasets/ames.csv, train_test_split(test_size=0.25,
random_state=1), then X_train.sample(30, random_state=29)).

    thirty      the 30 houses, the straight line and the degree-10 curve
    alphas      Ridge's degree-10 curve for alpha = 0, 10 and 1,000 (three panels)
    ridgecurve  Ridge's 5-fold CV RMSE vs. alpha, on the learned-from folds and the held-out fold

Usage:  python scripts/make_w10d2_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "10" / "class_w10d2_handout.md"
OUT_PDF = ROOT / "weeks" / "10" / "class_w10d2_handout.pdf"
ALPHAS = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
BLUE = "#2a78d6"

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def degree10(alpha):
    """The notebook's curve: area, ..., area^10, scaled, then Ridge (alpha = 0 is plain least squares)."""
    last = LinearRegression() if alpha == 0 else Ridge(alpha=alpha)
    return make_pipeline(PolynomialFeatures(10, include_bias=False), StandardScaler(), last)


def houses(ax, few, few_price):
    ax.scatter(few["living_area"], few_price / 1000, s=14, color="black", zorder=3)
    ax.set_xlim(700, 2900)
    ax.set_ylim(0, 600)
    ax.set_xlabel("living area (sq ft)")


def make_plots(outdir):
    ames = pd.read_csv(ROOT / "datasets" / "ames.csv")
    X, y = ames.drop(columns="price"), ames["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    few = X_train.sample(30, random_state=29)
    few_price = y_train[few.index]
    area = few[["living_area"]]
    sizes = pd.DataFrame({"living_area": np.linspace(808, 2772, 400)})
    plots = {}

    # thirty: the line and the wiggly curve
    line = LinearRegression().fit(area, few_price)
    curve = degree10(0).fit(area, few_price)
    fig, ax = plt.subplots(figsize=(4.1, 2.9))
    houses(ax, few, few_price)
    ax.plot(sizes["living_area"], line.predict(sizes) / 1000, color="#888888", lw=1.6, ls="--", label="straight line")
    ax.plot(sizes["living_area"], curve.predict(sizes) / 1000, color=BLUE, lw=1.6, label="degree-10 curve")
    ax.set_ylabel("sale price ($1000s)")
    ax.legend(loc="upper left", fontsize=7.5)
    plots["thirty"] = outdir / "thirty.pdf"
    save(fig, plots["thirty"])

    # alphas: three panels
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.4), sharey=True)
    for ax, alpha in zip(axes, [0, 10, 1000]):
        houses(ax, few, few_price)
        model = degree10(alpha).fit(area, few_price)
        ax.plot(sizes["living_area"], model.predict(sizes) / 1000, color=BLUE, lw=1.6)
        ax.set_title(f"alpha = {alpha:,}")
    axes[0].set_ylabel("sale price ($1000s)")
    plots["alphas"] = outdir / "alphas.pdf"
    save(fig, plots["alphas"])

    # ridgecurve: 5-fold CV on the 30 houses
    search = GridSearchCV(degree10(1), {"ridge__alpha": ALPHAS}, cv=5,
                          scoring="neg_root_mean_squared_error", return_train_score=True).fit(area, few_price)
    res = search.cv_results_
    fig, ax = plt.subplots(figsize=(4.1, 2.8))
    ax.plot(ALPHAS, -res["mean_train_score"] / 1000, color="black", lw=1.4, ls="--", marker="o", ms=3,
            label="folds it learned from")
    ax.plot(ALPHAS, -res["mean_test_score"] / 1000, color=BLUE, lw=1.8, marker="s", ms=3,
            label="held-out fold")
    ax.set_xscale("log"); ax.set_xticks(ALPHAS); ax.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100", "1,000"])
    ax.minorticks_off()
    ax.set_ylim(0, 130)
    ax.set_xlabel("alpha"); ax.set_ylabel("RMSE ($1000s)")
    ax.legend(loc="upper right", fontsize=7.5)
    plots["ridgecurve"] = outdir / "ridgecurve.pdf"
    save(fig, plots["ridgecurve"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
