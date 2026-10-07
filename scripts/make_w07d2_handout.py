"""
Build weeks/07/class_w07d2_handout.pdf -- the printed in-class activities for
Week 7 Wednesday (cross-validation and grid search) -- from its editable source,
weeks/07/class_w07d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
children and split as the notebook (datasets/autism.csv, ASD vs. NEU, features
fGSH and GSSG, train_test_split(test_size=0.3, random_state=7)). Parts 1 and 4
are tables in the .md.

    folds     5 rounds x 5 empty fold boxes to shade, each round's score
              (cross_val_score, max_depth=2, cv=5), and a locked test-set box
    cvcurve   mean 5-fold CV accuracy for max_depth 1-8, with +-1 std bars

Usage:  python scripts/make_w07d2_handout.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")   # silences a joblib core-count warning on Windows

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "07" / "class_w07d2_handout.md"
OUT_PDF = ROOT / "weeks" / "07" / "class_w07d2_handout.pdf"

FEATURES = ["fGSH", "GSSG"]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    autism = pd.read_csv(ROOT / "datasets" / "autism.csv")
    kids = autism[autism["Group"] != "SIB"]
    X_train, X_test, y_train, y_test = train_test_split(kids[FEATURES], kids["Group"], test_size=0.3, random_state=7)
    plots = {}

    # folds -- empty boxes to shade, with each round's score
    scores = cross_val_score(DecisionTreeClassifier(max_depth=2, random_state=0), X_train, y_train, cv=5)
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.set_xlim(0, 10.4); ax.set_ylim(-0.2, 5.6); ax.axis("off")
    ax.text(4.1, 5.25, "training set: 111 children", ha="center", fontsize=9, fontweight="bold")
    ax.text(9.5, 5.25, "test set: 48", ha="center", fontsize=9, fontweight="bold")
    for r in range(5):
        y0 = 4.0 - r
        ax.text(0, y0 + 0.35, f"round {r + 1}", va="center", fontsize=9)
        for f in range(5):
            ax.add_patch(Rectangle((1.2 + f * 1.2, y0 + 0.05), 1.1, 0.6, fill=False, lw=0.9, ec="black"))
            if r == 0:
                ax.text(1.75 + f * 1.2, 4.85, f"fold {f + 1}", ha="center", fontsize=7.5, color="#555555")
        ax.text(7.35, y0 + 0.35, f"→ {scores[r]:.3f}", va="center", fontsize=9)
        ax.add_patch(Rectangle((8.95, y0 + 0.05), 1.1, 0.6, fc="#d9d9d9", ec="#999999", lw=0.6))
        ax.text(9.5, y0 + 0.35, "locked", ha="center", va="center", fontsize=7.5, color="#555555")
    plots["folds"] = outdir / "folds.pdf"; save(fig, plots["folds"])

    # cvcurve -- mean CV accuracy vs. depth, +-1 std
    depths = list(range(1, 9))
    means, stds = [], []
    for depth in depths:
        s = cross_val_score(DecisionTreeClassifier(max_depth=depth, random_state=0), X_train, y_train, cv=5)
        means.append(s.mean() * 100); stds.append(s.std() * 100)
    fig, ax = plt.subplots(figsize=(4.0, 2.7))
    ax.errorbar(depths, means, yerr=stds, color="#2a78d6", lw=1.8, marker="o", ms=4, capsize=3, elinewidth=0.9)
    ax.set_xlim(0.5, 8.5); ax.set_ylim(60, 95)
    ax.set_xticks(depths)
    ax.set_xlabel("max_depth"); ax.set_ylabel("5-fold CV accuracy (%)")
    plots["cvcurve"] = outdir / "cvcurve.pdf"; save(fig, plots["cvcurve"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
