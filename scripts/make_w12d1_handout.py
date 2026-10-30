"""
Build weeks/12/class_w12d1_handout.pdf -- the printed in-class activities for
Week 12 Monday (imbalanced data) -- from its editable source,
weeks/12/class_w12d1_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
candidates and split as the notebook (datasets/pulsars.csv, train_test_split(
test_size=0.25, random_state=1, stratify=y): 13,423 training candidates).

    line        training candidates, profile_mean vs. profile_sd, with logistic regression's 50% line
    thresholds  recall and precision vs. threshold, all 8 columns, 5-fold cross_val_predict on the training set
    smote       a zoom on a few training pulsars (A-H) among noise, for doing SMOTE by hand

Usage:  python scripts/make_w12d1_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "12" / "class_w12d1_handout.md"
OUT_PDF = ROOT / "weeks" / "12" / "class_w12d1_handout.pdf"
NOISE = dict(color="#2a78d6", marker="o")
PULSAR = dict(color="#eb6834", marker="^")
TWO = ["profile_mean", "profile_sd"]
# SMOTE zoom: training pulsars labeled A-H (row numbers of datasets/pulsars.csv), and the window around them
ZOOM_PULSARS = {"A": 4841, "B": 3759, "C": 3456, "D": 2403, "E": 3330, "F": 3114, "G": 650, "H": 19}
ZOOM_X, ZOOM_Y = (50, 110), (32, 50)

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    candidates = pd.read_csv(ROOT / "datasets" / "pulsars.csv")
    X, y = candidates.drop(columns="pulsar"), candidates["pulsar"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)
    plots = {}

    # line
    model2 = LogisticRegression().fit(X_train[TWO], y_train)
    b0 = model2.intercept_[0]
    b_mean, b_sd = model2.coef_[0]
    fig, ax = plt.subplots(figsize=(4.3, 3.3))
    noise, pulsars = X_train[y_train == 0], X_train[y_train == 1]
    ax.scatter(noise["profile_mean"], noise["profile_sd"], s=3, alpha=0.25, linewidths=0, label="noise", **NOISE)
    ax.scatter(pulsars["profile_mean"], pulsars["profile_sd"], s=6, alpha=0.6, linewidths=0, label="pulsar", **PULSAR)
    means = np.linspace(0, 200, 50)
    ax.plot(means, -(b0 + b_mean * means) / b_sd, color="black", lw=1.6, label="50% line")
    ax.set_xlim(0, 200)
    ax.set_ylim(25, 85)
    ax.set_xlabel("profile mean")
    ax.set_ylabel("profile standard deviation")
    ax.legend(loc="upper right", fontsize=7.5, markerscale=2)
    plots["line"] = outdir / "line.pdf"
    save(fig, plots["line"])

    # thresholds
    model = make_pipeline(StandardScaler(), LogisticRegression())
    p_train = cross_val_predict(model, X_train, y_train, cv=5, method="predict_proba")[:, 1]
    ts = np.arange(0.02, 0.99, 0.02)
    recall = [recall_score(y_train, p_train >= t) for t in ts]
    precision = [precision_score(y_train, p_train >= t) for t in ts]
    fig, ax = plt.subplots(figsize=(4.2, 2.9))
    ax.plot(ts, recall, color="#eb6834", lw=1.8, label="recall: share of pulsars found")
    ax.plot(ts, precision, color="#2a78d6", lw=1.8, ls="--", label="precision: share of flags that are pulsars")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.3, 1.0)
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_xlabel("threshold: call it a pulsar if P(pulsar) is at least ...")
    ax.legend(loc="lower right", fontsize=7)
    plots["thresholds"] = outdir / "thresholds.pdf"
    save(fig, plots["thresholds"])

    # smote
    fig, ax = plt.subplots(figsize=(4.3, 3.1))
    inside = X_train[(X_train["profile_mean"].between(*ZOOM_X)) & (X_train["profile_sd"].between(*ZOOM_Y))]
    near_noise = inside[y_train[inside.index] == 0].sample(220, random_state=1)
    ax.scatter(near_noise["profile_mean"], near_noise["profile_sd"], s=7, alpha=0.5, linewidths=0, label="noise", **NOISE)
    for name, row in ZOOM_PULSARS.items():
        x, ysd = X.loc[row, "profile_mean"], X.loc[row, "profile_sd"]
        ax.scatter([x], [ysd], s=40, linewidths=0, zorder=3, **PULSAR)
        ax.annotate(name, (x, ysd), xytext=(4, 3), textcoords="offset points", fontsize=9, fontweight="bold")
    ax.scatter([], [], s=40, label="pulsar", **PULSAR)
    ax.set_xlim(*ZOOM_X)
    ax.set_ylim(*ZOOM_Y)
    ax.set_xlabel("profile mean")
    ax.set_ylabel("profile standard deviation")
    ax.legend(loc="upper left", fontsize=7.5)
    plots["smote"] = outdir / "smote.pdf"
    save(fig, plots["smote"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
