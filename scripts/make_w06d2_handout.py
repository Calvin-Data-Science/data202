"""
Build weeks/06/class_w06d2_handout.pdf -- the printed in-class activities for
Week 6 Wednesday (train/test split, confusion matrix, precision and recall) --
from its editable source, weeks/06/class_w06d2_handout.md. Text and layout live
in the .md; the shared engine is scripts/handout.py. This script only draws the
one plot, on the SAME penguins as the notebook (datasets/penguins.csv):

    splits   test accuracy of kNN (k = 5) on 30 random 70/30 splits
             (random_state 0-29, as in the notebook), one dot per split,
             stacked when scores tie; the notebook's split (random_state=24) is a star

(The confusion-matrix and precision/recall parts are tables in the .md -- their
numbers come from the notebook's split: random_state=24, k = 5.)

Usage:  python scripts/make_w06d2_handout.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")   # silences a joblib core-count warning on Windows

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "06" / "class_w06d2_handout.md"
OUT_PDF = ROOT / "weeks" / "06" / "class_w06d2_handout.pdf"
OUR_SPLIT = 24

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    penguins = pd.read_csv(ROOT / "datasets" / "penguins.csv").dropna(subset=["bill_length_mm", "bill_depth_mm"])
    X, y = penguins[["bill_length_mm", "bill_depth_mm"]], penguins["species"]
    scores = []
    for seed in range(30):
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed)
        knn = KNeighborsClassifier(n_neighbors=5).fit(X_tr, y_tr)
        scores.append(accuracy_score(y_te, knn.predict(X_te)) * 100)
    splits = pd.DataFrame({"seed": range(30), "score": scores})
    splits["stack"] = splits.groupby("score").cumcount() + 1

    fig, ax = plt.subplots(figsize=(4.3, 2.4))
    others = splits[splits["seed"] != OUR_SPLIT]
    ours = splits[splits["seed"] == OUR_SPLIT]
    ax.scatter(others["score"], others["stack"], s=70, c="#9a9a9a", edgecolors="black", linewidths=0.6, zorder=3)
    ax.scatter(ours["score"], ours["stack"], s=230, marker="*", c="black", zorder=4, label="our split")
    values = sorted(splits["score"].unique())
    ax.set_xticks(values)
    ax.set_xticklabels([f"{v:.1f}" for v in values], rotation=45)
    ax.set_yticks(range(1, int(splits["stack"].max()) + 2))
    ax.set_ylim(0.3, splits["stack"].max() + 0.9)
    ax.set_xlabel("test accuracy (%)"); ax.set_ylabel("number of splits")
    ax.legend(loc="upper right", fontsize=8)
    plots = {"splits": outdir / "splits.pdf"}
    save(fig, plots["splits"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
