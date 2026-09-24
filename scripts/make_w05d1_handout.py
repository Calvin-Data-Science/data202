"""
Build weeks/05/class_w05d1_handout.pdf -- the printed in-class activities for
Week 5 Monday (clustering) -- from its editable source,
weeks/05/class_w05d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
180 listeners as the notebook (datasets/listeners.csv):

    unlabeled   the 180 listeners, no groups
    start       + the notebook's 4 starting centroids (rows 38, 71, 129, 158),
                labeled A-D in the notebook's snapshot colors
    clusters    the KMeans(k=4, random_state=42) result, in the Plotly colors
                shown on screen, with marker shapes for black-and-white print
    elbow       inertia for k = 1..10 (same settings as the notebook)

Listener plots use an equal aspect ratio (1 hour = 1 artist on paper), so
"nearest X" and "halfway between two X's" can be judged by eye.

Usage:  python scripts/make_w05d1_handout.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")   # silences a scikit-learn KMeans warning on Windows

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "05" / "class_w05d1_handout.md"
OUT_PDF = ROOT / "weeks" / "05" / "class_w05d1_handout.pdf"

START_ROWS = [38, 71, 129, 158]                              # same start as the notebook's run_kmeans demo
START_COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]  # the notebook's snapshot COLORS, by centroid
PLOTLY_COLORS = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"] # px.scatter's default colors, by first appearance
MARKERS = ["o", "^", "s", "D"]                               # shapes keep groups apart in black-and-white print
XLIM, YLIM = (0, 40), (0, 44)

plt.rcParams.update(handout.PLOT_STYLE)


def listener_axes(ax):
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.set_xticks(range(0, 41, 5)); ax.set_yticks(range(0, 45, 5))
    ax.set_xlabel("hours of music per week")
    ax.set_ylabel("different artists played")


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    listeners = pd.read_csv(ROOT / "datasets" / "listeners.csv")
    X = listeners[["hours_per_week", "distinct_artists"]].to_numpy()
    plots = {}

    fig, ax = plt.subplots(figsize=(3.7, 4.0))
    ax.scatter(X[:, 0], X[:, 1], s=9, c="#6b6b6b", linewidths=0)
    listener_axes(ax)
    plots["unlabeled"] = outdir / "unlabeled.pdf"; save(fig, plots["unlabeled"])

    fig, ax = plt.subplots(figsize=(3.7, 4.0))
    ax.scatter(X[:, 0], X[:, 1], s=9, c="#9a9a9a", linewidths=0)
    for letter, row, color in zip("ABCD", START_ROWS, START_COLORS):
        cx, cy = X[row]
        ax.scatter(cx, cy, s=170, marker="X", c="black", edgecolors="white", linewidths=1.3, zorder=5)
        ax.annotate(letter, (cx, cy), xytext=(-9, 7), textcoords="offset points",
                    fontsize=13, fontweight="bold", color=color, zorder=6)
    listener_axes(ax)
    plots["start"] = outdir / "start.pdf"; save(fig, plots["start"])

    km = KMeans(n_clusters=4, random_state=42, n_init=10).fit(X)
    appearance = list(pd.unique(km.labels_.astype(str)))      # Plotly colors categories in order of appearance
    fig, ax = plt.subplots(figsize=(3.7, 4.0))
    for j in range(4):
        m = km.labels_ == j
        ax.scatter(X[m, 0], X[m, 1], s=11, c=PLOTLY_COLORS[appearance.index(str(j))], marker=MARKERS[j],
                   linewidths=0.3, edgecolors="white")
    for j, (cx, cy) in enumerate(km.cluster_centers_):
        ax.scatter(cx, cy, s=120, marker="X", c="black", edgecolors="white", linewidths=1.2, zorder=5)
        ax.annotate(f"cluster {j}", (cx, cy), xytext=(6, -11), textcoords="offset points",
                    fontsize=8, fontweight="bold", zorder=6)
    listener_axes(ax)
    plots["clusters"] = outdir / "clusters.pdf"; save(fig, plots["clusters"])

    ks = list(range(1, 11))
    inertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_ for k in ks]
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    ax.plot(ks, np.array(inertias) / 1000, color="black", lw=1.6, marker="o", ms=4)
    ax.set_xticks(ks)
    ax.set_xlabel("number of clusters k"); ax.set_ylabel("inertia (thousands)")
    plots["elbow"] = outdir / "elbow.pdf"; save(fig, plots["elbow"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
