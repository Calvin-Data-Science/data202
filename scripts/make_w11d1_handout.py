"""
Build weeks/11/class_w11d1_handout.pdf -- the printed in-class activities for
Week 11 Monday (logistic regression) -- from its editable source,
weeks/11/class_w11d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
seeds and split as the notebook (datasets/pumpkin.csv, train_test_split(
test_size=0.25, random_state=1): 1,875 training seeds).

    scurve       training seeds at 0/1 by aspect ratio + the logistic S-curve, seeds A, B, C marked
    lengthwidth  training seeds, length vs. width, by variety (students draw a boundary)
    ccurve       5-fold CV accuracy vs. C, all 12 columns scaled

Usage:  python scripts/make_w11d1_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "11" / "class_w11d1_handout.md"
OUT_PDF = ROOT / "weeks" / "11" / "class_w11d1_handout.pdf"
CER, URG = "Çerçevelik", "Ürgüp Sivrisi"
STYLE = {CER: dict(color="#2a78d6", marker="o"), URG: dict(color="#eb6834", marker="^")}
CS = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    seeds = pd.read_csv(ROOT / "datasets" / "pumpkin.csv")
    X, y = seeds.drop(columns="variety"), seeds["variety"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    rng = np.random.default_rng(0)
    plots = {}

    # scurve
    logit = LogisticRegression().fit(X_train[["aspect_ratio"]], y_train)
    ratios = pd.DataFrame({"aspect_ratio": np.linspace(1.1, 3.2, 300)})
    fig, ax = plt.subplots(figsize=(4.2, 2.9))
    for variety, level in [(CER, 0), (URG, 1)]:
        r = X_train.loc[y_train == variety, "aspect_ratio"]
        ax.scatter(r, level + rng.uniform(-0.04, 0.04, len(r)), s=5, alpha=0.25, linewidths=0, **STYLE[variety])
    ax.plot(ratios["aspect_ratio"], logit.predict_proba(ratios)[:, 1], color="black", lw=1.8)
    for name, a in [("A", 1.8), ("B", 2.0), ("C", 2.4)]:
        p = logit.predict_proba(pd.DataFrame({"aspect_ratio": [a]}))[0, 1]
        ax.plot([a], [p], "o", color="black", ms=5, zorder=4)
        ax.annotate(name, (a, p), xytext=(-11, 4), textcoords="offset points", fontsize=9, fontweight="bold")
    ax.set_xlim(1.1, 3.2)
    ax.set_ylim(-0.08, 1.08)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlabel("aspect ratio (length ÷ width)")
    ax.set_ylabel("P(Ürgüp Sivrisi)")
    ax.text(3.15, 0.93, "Ürgüp Sivrisi", ha="right", fontsize=7.5, color=STYLE[URG]["color"])
    ax.text(1.15, 0.05, "Çerçevelik", ha="left", fontsize=7.5, color=STYLE[CER]["color"])
    plots["scurve"] = outdir / "scurve.pdf"
    save(fig, plots["scurve"])

    # lengthwidth
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    for variety in [CER, URG]:
        part = X_train[y_train == variety]
        ax.scatter(part["width"], part["length"], s=6, alpha=0.45, linewidths=0, label=variety, **STYLE[variety])
    ax.set_xlim(150, 310)
    ax.set_ylim(300, 680)
    ax.set_xlabel("width (pixels)")
    ax.set_ylabel("length (pixels)")
    ax.legend(loc="upper right", fontsize=7.5, markerscale=2)
    plots["lengthwidth"] = outdir / "lengthwidth.pdf"
    save(fig, plots["lengthwidth"])

    # ccurve
    search = GridSearchCV(make_pipeline(StandardScaler(), LogisticRegression(max_iter=10_000)),
                          {"logisticregression__C": CS}, cv=5, return_train_score=True).fit(X_train, y_train)
    res = search.cv_results_
    fig, ax = plt.subplots(figsize=(4.1, 2.8))
    ax.plot(CS, res["mean_train_score"], color="black", lw=1.4, ls="--", marker="o", ms=3, label="folds it learned from")
    ax.plot(CS, res["mean_test_score"], color="#2a78d6", lw=1.8, marker="s", ms=3, label="held-out fold")
    ax.set_xscale("log")
    ax.set_xticks(CS)
    ax.set_xticklabels(["0.0001", "0.001", "0.01", "0.1", "1", "10", "100", "1,000"], fontsize=7.5)
    ax.minorticks_off()
    ax.set_ylim(0.80, 0.90)
    ax.set_xlabel("C")
    ax.set_ylabel("accuracy")
    ax.legend(loc="lower right", fontsize=7.5)
    plots["ccurve"] = outdir / "ccurve.pdf"
    save(fig, plots["ccurve"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
