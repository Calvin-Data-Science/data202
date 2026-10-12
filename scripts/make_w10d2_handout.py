"""
Build weeks/10/class_w10d2_handout.pdf -- the printed in-class activities for
Week 10 Wednesday (Ridge and Lasso) -- from its editable source,
weeks/10/class_w10d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plot, on the SAME
houses, split and pipeline as the notebook (datasets/ames.csv, train_test_split(
test_size=0.25, random_state=1), impute + scale + all products of two numeric
columns, one-hot neighborhood).

    ridgecurve  Ridge's 5-fold CV RMSE vs. alpha, on the learned-from folds and the held-out fold

Usage:  python scripts/make_w10d2_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "10" / "class_w10d2_handout.md"
OUT_PDF = ROOT / "weeks" / "10" / "class_w10d2_handout.pdf"
ALPHAS = [0.1, 1, 10, 30, 100, 300, 1000, 3000, 10000]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    ames = pd.read_csv(ROOT / "datasets" / "ames.csv")
    X, y = ames.drop(columns="price"), ames["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    numeric = [c for c in X.columns if c not in ("neighborhood", "year_sold")]
    prep = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                              PolynomialFeatures(degree=2, include_bias=False)), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"])])
    search = GridSearchCV(Pipeline([("prep", prep), ("regressor", Ridge())]), {"regressor__alpha": ALPHAS}, cv=5,
                          scoring="neg_root_mean_squared_error", return_train_score=True).fit(X_train, y_train)
    res = search.cv_results_

    fig, ax = plt.subplots(figsize=(4.1, 2.8))
    ax.plot(ALPHAS, -res["mean_train_score"] / 1000, color="black", lw=1.4, ls="--", marker="o", ms=3,
            label="folds it learned from")
    ax.plot(ALPHAS, -res["mean_test_score"] / 1000, color="#2a78d6", lw=1.8, marker="s", ms=3,
            label="held-out fold")
    ax.set_xscale("log"); ax.set_xticks(ALPHAS); ax.set_xticklabels(["0.1", "1", "10", "30", "100", "300", "1k", "3k", "10k"])
    ax.minorticks_off()
    ax.set_ylim(15, 42)
    ax.set_xlabel("alpha"); ax.set_ylabel("RMSE ($1000s)")
    ax.legend(loc="upper left", fontsize=7.5)
    plots = {"ridgecurve": outdir / "ridgecurve.pdf"}
    save(fig, plots["ridgecurve"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
