"""
Build weeks/05/class_w05d2_handout.pdf -- the printed in-class activities for
Week 5 Wednesday (PCA) -- from its editable source,
weeks/05/class_w05d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
digits as the notebook (sklearn's load_digits):

    clusters     one row per KMeans(k=10, random_state=42) cluster: its average
                 image, its first 8 members (as in the notebook's grid), and an
                 empty box to write the digit in
    views        300 of the digits drawn as their true digit, in two views:
                 pixel 42 vs pixel 21 (with the notebook's jitter) and PC1 vs PC2
    cumulative   cumulative share of the variance for the 64 components

(The z-score part is a table in the .md -- no plot.)

Usage:  python scripts/make_w05d2_handout.py
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")   # silences a scikit-learn KMeans warning on Windows

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "05" / "class_w05d2_handout.md"
OUT_PDF = ROOT / "weeks" / "05" / "class_w05d2_handout.pdf"
N_SHOWN = 300          # digits drawn in the two views (all 1,797 would be an unreadable blot)

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    digits = load_digits()
    X, y = digits.data, digits.target
    km = KMeans(n_clusters=10, random_state=42, n_init=10).fit(X)
    labels = km.labels_
    plots = {}

    # clusters -- average image | 8 members | empty box, one row per cluster
    fig, axes = plt.subplots(10, 10, figsize=(3.9, 4.1), gridspec_kw=dict(wspace=0.08, hspace=0.08))
    for c in range(10):
        axes[c, 0].imshow(km.cluster_centers_[c].reshape(8, 8), cmap="gray_r")
        for j, image in enumerate(X[labels == c][:8], start=1):
            axes[c, j].imshow(image.reshape(8, 8), cmap="gray_r")
        axes[c, 0].set_ylabel(f"cluster {c}", rotation=0, ha="right", va="center", fontsize=7)
    for ax in axes.flat:
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(True); spine.set_color("#c8c8c8"); spine.set_linewidth(0.5)
    for ax in list(axes[:, 0]) + list(axes[:, 9]):       # average image and the write-in box get a dark frame
        for spine in ax.spines.values():
            spine.set_color("black"); spine.set_linewidth(1.0)
    axes[0, 0].set_title("average", fontsize=7, fontweight="normal")
    axes[0, 9].set_title("digit?", fontsize=7, fontweight="normal")
    left, right = axes[0, 1].get_position(), axes[0, 8].get_position()
    fig.text((left.x0 + right.x1) / 2, left.y1 + 0.012, "8 of its members", ha="center", va="bottom", fontsize=7)
    plots["clusters"] = outdir / "clusters.pdf"; save(fig, plots["clusters"])

    # views -- the same 300 digits, before and after PCA
    jitter = np.random.default_rng(0).uniform(-0.3, 0.3, size=(len(X), 2))    # same jitter as the notebook
    pca = PCA(n_components=2, random_state=42)
    X_2d = pca.fit_transform(X)
    pixel_share = X[:, [42, 21]].var(axis=0).sum() / X.var(axis=0).sum()
    shown = np.random.default_rng(1).choice(len(X), N_SHOWN, replace=False)
    fig, (before, after) = plt.subplots(1, 2, figsize=(7.4, 3.5))
    views = [(before, X[:, 42] + jitter[:, 0], X[:, 21] + jitter[:, 1],
              f"Before: pixel 42 vs. pixel 21  ({pixel_share:.1%} of the variance)", "pixel 42", "pixel 21"),
             (after, X_2d[:, 0], X_2d[:, 1],
              f"After: PC1 vs. PC2  ({pca.explained_variance_ratio_.sum():.1%} of the variance)", "PC1", "PC2")]
    for ax, xs, ys, title, xlabel, ylabel in views:
        for i in shown:
            ax.text(xs[i], ys[i], str(y[i]), fontsize=6.5, ha="center", va="center")
        pad_x, pad_y = 0.04 * np.ptp(xs[shown]), 0.04 * np.ptp(ys[shown])
        ax.set_xlim(xs[shown].min() - pad_x, xs[shown].max() + pad_x)
        ax.set_ylim(ys[shown].min() - pad_y, ys[shown].max() + pad_y)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    fig.tight_layout(w_pad=2.5)
    plots["views"] = outdir / "views.pdf"; save(fig, plots["views"])

    # cumulative -- share of the variance kept by the first n components
    cumulative = np.cumsum(PCA(random_state=42).fit(X).explained_variance_ratio_) * 100
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.plot(range(1, 65), cumulative, color="black", lw=1.6)
    for level in (80, 90):
        ax.axhline(level, ls=":", color="#555555", lw=1)
        ax.text(63.5, level + 1, f"{level}%", ha="right", va="bottom", fontsize=7)
    ax.set_xlim(0, 64); ax.set_ylim(0, 100)
    ax.set_xticks(range(0, 65, 8)); ax.set_xticks(range(0, 65, 2), minor=True)
    ax.grid(which="minor", axis="x", color="#eeeeee", linewidth=0.5)
    ax.set_xlabel("number of components n"); ax.set_ylabel("variance kept (%)")
    plots["cumulative"] = outdir / "cumulative.pdf"; save(fig, plots["cumulative"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
