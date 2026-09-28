"""
Build weeks/06/class_w06d1_handout.pdf -- the printed in-class activities for
Week 6 Monday (kNN) -- from its editable source,
weeks/06/class_w06d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
penguins as the notebook (datasets/penguins.csv): the model learns from the
2007-2008 penguins ("known"); 2009 brings the new ones.

    mystery    the 223 known penguins + the notebook's three new 2009 penguins
               A (49.1, 14.5), B (44.1, 18.0), C (50.8, 18.5) as stars
    zoom       a 5 mm x 5 mm window around B, equal aspect with a 1 mm grid,
               so "nearest" can be judged by eye (its 5 nearest are within 1.4 mm)
    maps       kNN's map for k = 1, 5, 100 (as in the notebook), with hatching so
               the three regions stay apart in black-and-white print, and a
               blank under each map
    accuracy   accuracy vs. k (odd k, 1-149) on the known and on the new penguins

Species keep the notebook's colors and a marker shape each (circle = Adelie,
triangle = Chinstrap, square = Gentoo) for black-and-white print.

Usage:  python scripts/make_w06d1_handout.py
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
from sklearn.neighbors import KNeighborsClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "06" / "class_w06d1_handout.md"
OUT_PDF = ROOT / "weeks" / "06" / "class_w06d1_handout.pdf"

FEATURES = ["bill_length_mm", "bill_depth_mm"]
COLORS = {"Adelie": "#FF8C00", "Chinstrap": "#A034F0", "Gentoo": "#159090"}   # the notebook's COLORS
MARKERS = {"Adelie": "o", "Chinstrap": "^", "Gentoo": "s"}
HATCHES = {"Adelie": None, "Chinstrap": "////", "Gentoo": "...."}
MYSTERY = {"A": (49.1, 14.5), "B": (44.1, 18.0), "C": (50.8, 18.5)}           # the notebook's new penguins
MAP_KS = [1, 5, 100]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def penguin_dots(ax, known, size=16, edge="white"):
    for s in COLORS:
        d = known[known["species"] == s]
        ax.scatter(d["bill_length_mm"], d["bill_depth_mm"], s=size, c=COLORS[s], marker=MARKERS[s],
                   edgecolors=edge, linewidths=0.4, label=s, zorder=3)


def star(ax, letter, x, y, size=190, fontsize=12):
    ax.scatter(x, y, s=size, marker="*", c="black", edgecolors="white", linewidths=0.8, zorder=6)
    ax.annotate(letter, (x, y), xytext=(5, 5), textcoords="offset points", fontsize=fontsize,
                fontweight="bold", zorder=7)


def make_plots(outdir):
    penguins = pd.read_csv(ROOT / "datasets" / "penguins.csv").dropna(subset=FEATURES)
    known = penguins[penguins["year"] <= 2008]
    new = penguins[penguins["year"] == 2009]
    X, y = known[FEATURES], known["species"]
    plots = {}

    # mystery -- all known penguins and the three stars
    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    penguin_dots(ax, known)
    for letter, (bx, by) in MYSTERY.items():
        star(ax, letter, bx, by)
    ax.set_xlim(31, 61); ax.set_ylim(12.8, 21.8)
    ax.set_xlabel("bill length (mm)"); ax.set_ylabel("bill depth (mm)")
    ax.legend(loc="upper right", fontsize=8, markerscale=1.3, framealpha=0.9)
    plots["mystery"] = outdir / "mystery.pdf"; save(fig, plots["mystery"])

    # zoom -- 5 mm x 5 mm around B, true distances
    bx, by = MYSTERY["B"]
    fig, ax = plt.subplots(figsize=(3.3, 3.3))
    window = known[known["bill_length_mm"].between(bx - 2.5, bx + 2.5) & known["bill_depth_mm"].between(by - 2.5, by + 2.5)]
    penguin_dots(ax, window, size=46, edge="black")
    star(ax, "B", bx, by, size=260, fontsize=13)
    ax.set_xlim(bx - 2.5, bx + 2.5); ax.set_ylim(by - 2.5, by + 2.5)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(np.ceil(bx - 2.5), bx + 2.5, 1)); ax.set_yticks(np.arange(np.ceil(by - 2.5), by + 2.5, 1))
    ax.set_xlabel("bill length (mm)"); ax.set_ylabel("bill depth (mm)")
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    plots["zoom"] = outdir / "zoom.pdf"; save(fig, plots["zoom"])

    # maps -- k = 1, 5, 100, with a blank under each
    species = list(COLORS)
    xx, yy = np.meshgrid(np.linspace(31, 61, 400), np.linspace(12.5, 22, 260))
    grid = pd.DataFrame({"bill_length_mm": xx.ravel(), "bill_depth_mm": yy.ravel()})
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.75), sharey=True)
    for ax, k in zip(axes, MAP_KS):
        model = KNeighborsClassifier(n_neighbors=k).fit(X, y)
        z = pd.Series(model.predict(grid)).map(species.index).to_numpy().reshape(xx.shape)
        ax.contourf(xx, yy, z, levels=[-0.5, 0.5, 1.5, 2.5], colors=[COLORS[s] for s in species], alpha=0.22,
                    hatches=[HATCHES[s] for s in species])
        ax.contour(xx, yy, z, levels=[0.5, 1.5], colors="black", linewidths=0.6)
        penguin_dots(ax, known, size=7, edge="none")
        ax.set_title(f"k = {k}")
        ax.set_xlim(31, 61); ax.set_ylim(12.5, 22)
        ax.set_xlabel("bill length (mm)")
        ax.grid(False)
        ax.annotate("_" * 22, xy=(0.5, -0.36), xycoords="axes fraction", ha="center", fontsize=9)
    axes[0].set_ylabel("bill depth (mm)")
    plots["maps"] = outdir / "maps.pdf"; save(fig, plots["maps"])

    # accuracy -- accuracy vs. k on known and new penguins
    ks = list(range(1, 150, 2))
    acc_known, acc_new = [], []
    for k in ks:
        model = KNeighborsClassifier(n_neighbors=k).fit(X, y)
        acc_known.append(accuracy_score(y, model.predict(X)))
        acc_new.append(accuracy_score(new["species"], model.predict(new[FEATURES])))
    fig, ax = plt.subplots(figsize=(4.0, 2.7))
    ax.plot(ks, np.array(acc_known) * 100, color="black", lw=1.4, ls="--", marker="o", ms=2.5,
            label="known penguins (2007–08)")
    ax.plot(ks, np.array(acc_new) * 100, color="#2a78d6", lw=1.8, marker="s", ms=2.5,
            label="new penguins (2009)")
    ax.set_xlim(0, 150); ax.set_ylim(70, 101)
    ax.set_xticks(range(0, 151, 25))
    ax.set_xlabel("k (number of neighbors)"); ax.set_ylabel("accuracy (%)")
    ax.legend(loc="lower left", fontsize=7.5)
    plots["accuracy"] = outdir / "accuracy.pdf"; save(fig, plots["accuracy"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
