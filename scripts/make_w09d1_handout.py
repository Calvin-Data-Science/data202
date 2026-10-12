"""
Build weeks/09/class_w09d1_handout.pdf -- the printed in-class activities for
Week 9 Monday (scaling, encoding, pipelines) -- from its editable source,
weeks/09/class_w09d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
passengers and split as the notebook (datasets/titanic.csv, rows with age, fare
and embarked recorded, train_test_split(test_size=0.25, stratify=y, random_state=1)).

    closest  the training passengers by age and fare, once in years and pounds (same
             ruler on both axes) and once in standard deviations, with A, B, C marked
    pipe     the pipeline as boxes, with blanks for the columns in each branch
    kcurve   the pipeline's accuracy vs. k on the learned-from folds and the held-out fold

Usage:  python scripts/make_w09d1_handout.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")   # silences a joblib core-count warning on Windows

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "09" / "class_w09d1_handout.md"
OUT_PDF = ROOT / "weeks" / "09" / "class_w09d1_handout.pdf"

NAMES = {"A": "Colley, Mr. Edward Pomeroy", "B": "Davies, Mr. John Samuel", "C": "Chaffee, Mr. Herbert Fuller"}
NUMERIC = ["pclass", "age", "sibsp", "parch", "fare"]
KS = [1, 3, 5, 9, 15, 25, 51, 101, 201]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    titanic = pd.read_csv(ROOT / "datasets" / "titanic.csv")
    passengers = titanic.dropna(subset=["age", "fare", "embarked"])
    X = passengers[["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]]
    y = passengers["survived"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1)
    abc = passengers.set_index("name").loc[list(NAMES.values()), ["age", "fare"]]
    abc.index = list(NAMES)
    plots = {}

    # closest -- raw (equal ruler) and in standard deviations
    mean, sd = X_train[["age", "fare"]].mean(), X_train[["age", "fare"]].std(ddof=0)
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.5))
    for ax, scaled in zip(axes, [False, True]):
        pts = (X_train[["age", "fare"]] - mean) / sd if scaled else X_train[["age", "fare"]]
        marks = (abc - mean) / sd if scaled else abc
        ax.scatter(pts["age"], pts["fare"], s=5, color="#c8c8c8", zorder=2)
        for label, row in marks.iterrows():
            ax.scatter(row["age"], row["fare"], s=36, color="black", zorder=4)
            ax.annotate(label, (row["age"], row["fare"]), xytext=(4, 4), textcoords="offset points",
                        fontsize=10, fontweight="bold", zorder=5)
        if scaled:
            ax.set_xlim(-2.2, 1.6); ax.set_ylim(-0.9, 1.0)
            ax.set_xlabel("age (standard deviations)"); ax.set_ylabel("fare (standard deviations)")
            ax.set_title("In standard deviations")
        else:
            ax.set_xlim(10, 60); ax.set_ylim(0, 70)
            ax.set_xlabel("age (years)"); ax.set_ylabel("fare (£)")
            ax.set_title("In years and pounds")
        ax.set_aspect("equal")
    plots["closest"] = outdir / "closest.pdf"; save(fig, plots["closest"])

    # pipe -- the pipeline as boxes, with blanks
    fig, ax = plt.subplots(figsize=(7.4, 2.7))
    ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.axis("off")

    def box(x, y, w, h, text, size=8.5, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6", fc="white", ec="black", lw=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
                fontweight="bold" if bold else "normal")

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", lw=0.9))

    box(1, 15, 15, 10, "X_train\n7 columns", bold=True)
    box(27, 26, 26, 11, "num: StandardScaler\n\n______________________")
    box(27, 3, 26, 11, "cat: OneHotEncoder\n\n______________________")
    box(63, 15, 13, 10, "_____\ncolumns")
    box(85, 15, 13, 10, "kNN\nk = 5", bold=True)
    arrow(17, 21, 26, 31); arrow(17, 19, 26, 9)
    arrow(54, 31, 62, 22); arrow(54, 9, 62, 18)
    arrow(77, 20, 84, 20)
    ax.text(40, 39.5, "prep (ColumnTransformer)", ha="center", fontsize=8, style="italic")
    plots["pipe"] = outdir / "pipe.pdf"; save(fig, plots["pipe"])

    # kcurve -- the grid search over k
    preprocess = ColumnTransformer([("num", StandardScaler(), NUMERIC),
                                    ("cat", OneHotEncoder(drop="if_binary"), ["sex", "embarked"])])
    model = Pipeline([("prep", preprocess), ("knn", KNeighborsClassifier(n_neighbors=5))])
    search = GridSearchCV(model, {"knn__n_neighbors": KS}, cv=5, return_train_score=True).fit(X_train, y_train)
    res = search.cv_results_
    fig, ax = plt.subplots(figsize=(4.0, 2.7))
    ax.plot(KS, res["mean_train_score"] * 100, color="black", lw=1.4, ls="--", marker="o", ms=3,
            label="folds it learned from")
    ax.plot(KS, res["mean_test_score"] * 100, color="#2a78d6", lw=1.8, marker="s", ms=3,
            label="held-out fold")
    ax.set_xscale("log"); ax.set_xticks(KS); ax.set_xticklabels([str(k) for k in KS])
    ax.minorticks_off()
    ax.set_ylim(65, 101)
    ax.set_xlabel("k (number of neighbors)"); ax.set_ylabel("accuracy (%)")
    ax.legend(loc="upper right", fontsize=7.5)
    plots["kcurve"] = outdir / "kcurve.pdf"; save(fig, plots["kcurve"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
