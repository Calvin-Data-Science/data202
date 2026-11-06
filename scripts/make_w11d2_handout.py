"""
Build weeks/11/class_w11d2_handout.pdf -- the printed in-class activities for
Week 11 Wednesday (ensembles) -- from its editable source,
weeks/11/class_w11d2_handout.md. Text and layout live in the .md (including
Part 1's vote table, typed in from the notebook); the shared engine is
scripts/handout.py. This script only draws the plots, on the SAME seeds and split
as the notebook (datasets/pumpkin.csv, train_test_split(test_size=0.25,
random_state=1): 1,875 training seeds, 5-fold CV). Takes about 30 seconds.

    treeforest  CV accuracy vs. max_depth: one tree and a forest of 100, learned-from and held-out folds
    adaboost    the notebook's 20 seeds (aspect ratio vs. area), two panels: stump 1's cut,
                then each seed drawn by its weight after reweighting (no cut: students draw stump 2)

Usage:  python scripts/make_w11d2_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "11" / "class_w11d2_handout.md"
OUT_PDF = ROOT / "weeks" / "11" / "class_w11d2_handout.pdf"
DEPTHS = [1, 2, 3, 4, 6, 8, 10, 15, None]
BLUE, ORANGE = "#2a78d6", "#eb6834"
UR, CE = "Ürgüp Sivrisi", "Çerçevelik"

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

    # adaboost: the notebook's steps 1-4 on its 20 seeds
    few = X_train.sample(20, random_state=73)[["aspect_ratio", "area"]]
    few_variety = y_train[few.index].to_numpy()
    weight = np.full(20, 1 / 20)
    stump1 = DecisionTreeClassifier(max_depth=1).fit(few, few_variety, sample_weight=weight)
    wrong1 = stump1.predict(few) != few_variety
    say1 = 0.5 * np.log((1 - weight[wrong1].sum()) / weight[wrong1].sum())
    weight = weight * np.where(wrong1, np.exp(say1), np.exp(-say1))
    weight = weight / weight.sum()
    cut = stump1.tree_.threshold[0]
    assert stump1.tree_.feature[0] == 0 and wrong1.sum() == 3, "stump 1 should be the notebook's aspect-ratio cut"

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5), sharex=True, sharey=True)
    for ax, sizes, title in [(axes[0], np.full(20, 34.0), "Stump 1"),
                             (axes[1], 34.0 * weight / weight.min(), "Round 2: each seed drawn by its new weight")]:
        for variety, color, marker, short in [(UR, BLUE, "o", "Ü"), (CE, ORANGE, "D", "Ç")]:
            mask = few_variety == variety
            ax.scatter(few["aspect_ratio"][mask], few["area"][mask], s=sizes[mask], color=color, marker=marker,
                       alpha=0.85, edgecolors="white", linewidths=0.5, label=f"{short} = {variety}")
        ax.set_title(title, loc="left")
        ax.set_xlabel("aspect ratio (length ÷ width)")
    axes[0].axvline(cut, color="#333333", ls="--", lw=1.2)
    top = few["area"].max() * 1.06
    axes[0].text(cut - 0.03, top, "says Ç", ha="right", va="center", fontsize=8)
    axes[0].text(cut + 0.03, top, "says Ü", ha="left", va="center", fontsize=8)
    axes[0].set_ylim(few["area"].min() * 0.92, few["area"].max() * 1.10)
    axes[0].set_ylabel("area (pixels)")
    axes[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    axes[0].legend(loc="lower right", fontsize=7)
    fig.tight_layout()
    plots["adaboost"] = outdir / "adaboost.pdf"
    save(fig, plots["adaboost"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
