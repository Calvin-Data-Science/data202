"""
Build weeks/07/class_w07d1_handout.pdf -- the printed in-class activities for
Week 7 Monday (decision trees) -- from its editable source,
weeks/07/class_w07d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
children and split as the notebook (datasets/autism.csv, ASD vs. NEU, features
fGSH and GSSG, train_test_split(test_size=0.3, random_state=7)).

    onecut   the 111 training children, with a light grid, for drawing one line
    tree2    the depth-2 tree (question, samples, [ASD, NEU] counts, class), no colors
    maps     the maps of depth 1, depth 2 and no limit, hatched for black-and-white
             print, with a blank under each
    depth    training and test accuracy for max_depth 1-10

Groups keep the notebook's colors and a marker shape each (triangle = ASD,
circle = NEU) for black-and-white print.

Usage:  python scripts/make_w07d1_handout.py
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
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "07" / "class_w07d1_handout.md"
OUT_PDF = ROOT / "weeks" / "07" / "class_w07d1_handout.pdf"

FEATURES = ["fGSH", "GSSG"]
COLORS = {"ASD": "#eb6834", "NEU": "#2a78d6"}   # the notebook's COLORS
MARKERS = {"ASD": "^", "NEU": "o"}
HATCHES = {"ASD": "////", "NEU": None}
XLIM, YLIM = (1.0, 5.6), (0.04, 0.68)

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def child_dots(ax, X, y, size=16, edge="white"):
    for group in COLORS:
        pts = X[y == group]
        ax.scatter(pts["fGSH"], pts["GSSG"], s=size, c=COLORS[group], marker=MARKERS[group],
                   edgecolors=edge, linewidths=0.4, label=group, zorder=3)


def make_plots(outdir):
    autism = pd.read_csv(ROOT / "datasets" / "autism.csv")
    kids = autism[autism["Group"] != "SIB"]
    X_train, X_test, y_train, y_test = train_test_split(kids[FEATURES], kids["Group"], test_size=0.3, random_state=7)
    plots = {}

    # onecut -- the training children on a light grid
    fig, ax = plt.subplots(figsize=(7.2, 2.45))
    child_dots(ax, X_train, y_train, size=22, edge="black")
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
    ax.set_xticks(np.arange(1.0, 5.61, 0.5)); ax.set_yticks(np.arange(0.1, 0.66, 0.1))
    ax.grid(True, color="#e4e4e4", linewidth=0.5)
    ax.set_xlabel("fGSH (µM)"); ax.set_ylabel("GSSG (µM)")
    ax.legend(loc="upper right", fontsize=8, markerscale=1.2, framealpha=0.9)
    plots["onecut"] = outdir / "onecut.pdf"; save(fig, plots["onecut"])

    # tree2 -- the depth-2 tree, black and white
    tree2 = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    plot_tree(tree2, feature_names=FEATURES, class_names=list(tree2.classes_), filled=False, impurity=False,
              fontsize=8, ax=ax)
    plots["tree2"] = outdir / "tree2.pdf"; save(fig, plots["tree2"])

    # maps -- depth 1, depth 2, no limit; a blank under each
    xx, yy = np.meshgrid(np.linspace(*XLIM, 500), np.linspace(*YLIM, 380))
    grid = pd.DataFrame({"fGSH": xx.ravel(), "GSSG": yy.ravel()})
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.75), sharey=True)
    for ax, (title, depth) in zip(axes, [("depth 1", 1), ("depth 2", 2), ("no limit", None)]):
        model = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
        z = (model.predict(grid) == "NEU").astype(int).reshape(xx.shape)
        ax.contourf(xx, yy, z, levels=[-0.5, 0.5, 1.5], colors=[COLORS["ASD"], COLORS["NEU"]], alpha=0.22,
                    hatches=[HATCHES["ASD"], HATCHES["NEU"]])
        ax.contour(xx, yy, z, levels=[0.5], colors="black", linewidths=0.6)
        child_dots(ax, X_train, y_train, size=7, edge="none")
        ax.set_title(f"{title} ({model.get_n_leaves()} leaves)")
        ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
        ax.set_xlabel("fGSH (µM)")
        ax.grid(False)
        ax.annotate("_" * 22, xy=(0.5, -0.36), xycoords="axes fraction", ha="center", fontsize=9)
    axes[0].set_ylabel("GSSG (µM)")
    axes[0].legend(loc="upper right", fontsize=7, markerscale=1.5)
    plots["maps"] = outdir / "maps.pdf"; save(fig, plots["maps"])

    # depth -- training and test accuracy vs. max_depth
    depths = list(range(1, 11))
    acc_train, acc_test = [], []
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
        acc_train.append(accuracy_score(y_train, model.predict(X_train)))
        acc_test.append(accuracy_score(y_test, model.predict(X_test)))
    fig, ax = plt.subplots(figsize=(4.0, 2.7))
    ax.plot(depths, np.array(acc_train) * 100, color="black", lw=1.4, ls="--", marker="o", ms=3,
            label="training children (111)")
    ax.plot(depths, np.array(acc_test) * 100, color="#2a78d6", lw=1.8, marker="s", ms=3,
            label="test children (48)")
    ax.set_xlim(0.5, 10.5); ax.set_ylim(65, 102)
    ax.set_xticks(depths)
    ax.set_xlabel("max_depth"); ax.set_ylabel("accuracy (%)")
    ax.legend(loc="lower right", fontsize=7.5)
    plots["depth"] = outdir / "depth.pdf"; save(fig, plots["depth"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
