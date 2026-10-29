"""
Build weeks/11/class_w11d2_handout.pdf -- the printed in-class activities for
Week 11 Wednesday (ensembles) -- from its editable source,
weeks/11/class_w11d2_handout.md. Text and layout live in the .md (including
Part 1's vote table, typed in from the notebook); the shared engine is
scripts/handout.py. This script only draws the plots, on the SAME seeds and split
as the notebook (datasets/pumpkin.csv, train_test_split(test_size=0.25,
random_state=1): 1,875 training seeds, 5-fold CV). Takes about a minute.

    treeforest  CV accuracy vs. max_depth: one tree and a forest of 100, learned-from and held-out folds
    moretrees   CV accuracy vs. number of trees: boosting (learned-from and held-out) and a forest (held-out)

Usage:  python scripts/make_w11d2_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "11" / "class_w11d2_handout.md"
OUT_PDF = ROOT / "weeks" / "11" / "class_w11d2_handout.pdf"
DEPTHS = [1, 2, 3, 4, 6, 8, 10, 15, None]
BOOST_N = [1, 3, 10, 30, 100, 300, 1000]
FOREST_N = [1, 3, 10, 30, 100, 300]
BLUE, ORANGE = "#2a78d6", "#eb6834"

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def cv(model, X, y):
    scores = cross_validate(model, X, y, cv=5, return_train_score=True)
    return scores["train_score"].mean(), scores["test_score"].mean()


def make_plots(outdir):
    seeds = pd.read_csv(ROOT / "datasets" / "pumpkin.csv")
    X, y = seeds.drop(columns="variety"), seeds["variety"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    plots = {}

    # treeforest
    tree = [cv(DecisionTreeClassifier(max_depth=d, random_state=1), X_train, y_train) for d in DEPTHS]
    forest = [cv(RandomForestClassifier(max_depth=d, random_state=1, n_jobs=-1), X_train, y_train) for d in DEPTHS]
    xs = range(len(DEPTHS))
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.plot(xs, [t[0] for t in tree], color=BLUE, lw=1.3, ls="--", marker="o", ms=3, label="one tree, learned from")
    ax.plot(xs, [t[1] for t in tree], color=BLUE, lw=1.8, marker="o", ms=3, label="one tree, held out")
    ax.plot(xs, [f[0] for f in forest], color=ORANGE, lw=1.3, ls="--", marker="^", ms=3, label="forest, learned from")
    ax.plot(xs, [f[1] for f in forest], color=ORANGE, lw=1.8, marker="^", ms=3, label="forest, held out")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(["1", "2", "3", "4", "6", "8", "10", "15", "none"])
    ax.set_ylim(0.80, 1.01)
    ax.set_xlabel("max_depth")
    ax.set_ylabel("accuracy")
    ax.legend(loc="upper left", fontsize=7)
    plots["treeforest"] = outdir / "treeforest.pdf"
    save(fig, plots["treeforest"])

    # moretrees
    boost = [cv(GradientBoostingClassifier(n_estimators=n, random_state=1), X_train, y_train) for n in BOOST_N]
    forest = [cv(RandomForestClassifier(n_estimators=n, random_state=1, n_jobs=-1), X_train, y_train)[1] for n in FOREST_N]
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.plot(BOOST_N, [b[0] for b in boost], color=BLUE, lw=1.3, ls="--", marker="o", ms=3, label="boosting, learned from")
    ax.plot(BOOST_N, [b[1] for b in boost], color=BLUE, lw=1.8, marker="o", ms=3, label="boosting, held out")
    ax.plot(FOREST_N, forest, color=ORANGE, lw=1.8, marker="^", ms=3, label="forest, held out")
    ax.set_xscale("log")
    ax.set_xticks(BOOST_N)
    ax.set_xticklabels(["1", "3", "10", "30", "100", "300", "1,000"])
    ax.minorticks_off()
    ax.set_ylim(0.80, 1.01)
    ax.set_xlabel("number of trees")
    ax.set_ylabel("accuracy")
    ax.legend(loc="upper left", fontsize=7)
    plots["moretrees"] = outdir / "moretrees.pdf"
    save(fig, plots["moretrees"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
