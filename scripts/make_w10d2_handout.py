"""
Build weeks/10/class_w10d2_handout.pdf -- the printed in-class activities for
Week 10 Wednesday (Ridge and Lasso) -- from its editable source,
weeks/10/class_w10d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
25 houses and 18 number columns as the notebook (datasets/ames.csv,
train_test_split(test_size=0.25, random_state=1), then X_train.sample(25, random_state=19)).

    fit         predicted vs. actual price: the 25 houses (black) and the 732 test houses (gray), no legend
    slopes      the line's 18 slopes, learned from the 25 houses vs. from all 2,193 training houses
    alphas      Ridge's 18 slopes for alpha = 0, 10 and 1,000 (three panels)
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
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "10" / "class_w10d2_handout.md"
OUT_PDF = ROOT / "weeks" / "10" / "class_w10d2_handout.pdf"
ALPHAS = [0.01, 0.1, 1, 10, 100, 1000]
BLUE = "#2a78d6"
LIGHT = "#c4c4c4"

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def model(alpha):
    """The notebook's pipeline: fill blanks, scale, then least squares (alpha = 0) or Ridge."""
    last = LinearRegression() if alpha == 0 else Ridge(alpha=alpha)
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), last)


def make_plots(outdir):
    ames = pd.read_csv(ROOT / "datasets" / "ames.csv")
    X, y = ames.drop(columns="price"), ames["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    columns = [c for c in X.columns if c not in ("neighborhood", "year_sold", "second_floor_area")]
    few = X_train.sample(25, random_state=19)[columns]
    few_price = y_train[few.index]
    line = model(0).fit(few, few_price)
    rows = np.arange(len(columns))
    plots = {}

    # fit: predicted vs. actual; students label which dots are the 25
    fig, ax = plt.subplots(figsize=(3.3, 3.1))
    ax.scatter(y_test / 1000, line.predict(X_test[columns]) / 1000, s=7, facecolors="none",
               edgecolors="#9a9a9a", linewidths=0.5)
    ax.scatter(few_price / 1000, line.predict(few) / 1000, s=16, color="black", zorder=3)
    ax.plot([0, 650], [0, 650], color=BLUE, lw=1.3, ls="--", zorder=2)
    ax.set_xlim(0, 650); ax.set_ylim(-60, 650)
    ax.set_xlabel("actual price ($1000s)"); ax.set_ylabel("predicted price ($1000s)")
    plots["fit"] = outdir / "fit.pdf"
    save(fig, plots["fit"])

    # slopes: 25 houses vs. all 2,193 training houses
    everything = model(0).fit(X_train[columns], y_train)
    fig, ax = plt.subplots(figsize=(3.7, 4.3))
    ax.barh(rows - 0.2, line[-1].coef_ / 1000, height=0.4, color=BLUE, label="our 25 houses")
    ax.barh(rows + 0.2, everything[-1].coef_ / 1000, height=0.4, color=LIGHT, label="all 2,193 houses")
    ax.set_yticks(rows); ax.set_yticklabels(columns, fontsize=7.5); ax.invert_yaxis()
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xlim(-70, 120)
    ax.set_xlabel("slope ($1000s per typical step)")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", fontsize=7)
    plots["slopes"] = outdir / "slopes.pdf"
    save(fig, plots["slopes"])

    # alphas: Ridge's slopes in three panels
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.3), sharey=True, sharex=True)
    for ax, alpha in zip(axes, [0, 10, 1000]):
        coefs = model(alpha).fit(few, few_price)[-1].coef_
        ax.barh(rows, coefs / 1000, height=0.65, color=BLUE)
        ax.axvline(0, color="black", lw=0.6)
        ax.set_title(f"alpha = {alpha:,}")
        ax.set_xlim(-70, 120)
        ax.set_xlabel("slope ($1000s)")
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(rows); axes[0].set_yticklabels(columns, fontsize=7.5); axes[0].invert_yaxis()
    plots["alphas"] = outdir / "alphas.pdf"
    save(fig, plots["alphas"])

    # ridgecurve: 5-fold CV on the 25 houses
    search = GridSearchCV(model(1), {"ridge__alpha": ALPHAS}, cv=5,
                          scoring="neg_root_mean_squared_error", return_train_score=True).fit(few, few_price)
    res = search.cv_results_
    fig, ax = plt.subplots(figsize=(4.1, 2.8))
    ax.plot(ALPHAS, -res["mean_train_score"] / 1000, color="black", lw=1.4, ls="--", marker="o", ms=3,
            label="folds it learned from")
    ax.plot(ALPHAS, -res["mean_test_score"] / 1000, color=BLUE, lw=1.8, marker="s", ms=3,
            label="held-out fold")
    ax.set_xscale("log"); ax.set_xticks(ALPHAS); ax.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1,000"])
    ax.minorticks_off()
    ax.set_ylim(0, 130)
    ax.set_xlabel("alpha"); ax.set_ylabel("RMSE ($1000s)")
    ax.legend(loc="upper right", fontsize=7.5)
    plots["ridgecurve"] = outdir / "ridgecurve.pdf"
    save(fig, plots["ridgecurve"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
