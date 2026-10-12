"""
Build weeks/09/class_w09d2_handout.pdf -- the printed in-class activities for
Week 9 Wednesday (missing data) -- from its editable source,
weeks/09/class_w09d2_handout.md. Text and layout live in the .md; the shared
engine is scripts/handout.py. This script only draws the plots, on the SAME
passengers and split as the notebook (datasets/titanic.csv, all 1,309 passengers,
train_test_split(test_size=0.25, stratify=y, random_state=1)).

    noage    share of passengers with no recorded age, by ticket class
    spike    the training passengers' ages as recorded, and after filling the
             blanks with the training mean (SimpleImputer(strategy="mean"))

Usage:  python scripts/make_w09d2_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "09" / "class_w09d2_handout.md"
OUT_PDF = ROOT / "weeks" / "09" / "class_w09d2_handout.pdf"

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    titanic = pd.read_csv(ROOT / "datasets" / "titanic.csv")
    X = titanic[["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]]
    y = titanic["survived"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1)
    plots = {}

    # noage -- share with no age, by class
    share = titanic["age"].isna().groupby(titanic["pclass"]).mean() * 100
    fig, ax = plt.subplots(figsize=(3.3, 2.6))
    bars = ax.bar(["1st", "2nd", "3rd"], share.values, color="#2a78d6", width=0.6)
    for bar, value in zip(bars, share.values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.8, f"{value:.0f}%", ha="center", fontsize=9)
    ax.set_ylim(0, 35)
    ax.set_xlabel("ticket class"); ax.set_ylabel("no recorded age (%)")
    ax.grid(axis="x", visible=False)
    plots["noage"] = outdir / "noage.pdf"; save(fig, plots["noage"])

    # spike -- ages before and after mean imputation
    filled = SimpleImputer(strategy="mean").fit_transform(X_train[["age"]])[:, 0]
    bins = np.arange(0, 82, 2)
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 3.6), sharex=True, sharey=True)
    axes[0].hist(X_train["age"].dropna(), bins=bins, color="#2a78d6", edgecolor="white", linewidth=0.4)
    axes[0].set_title("as recorded", loc="left", fontsize=9)
    axes[1].hist(filled, bins=bins, color="#2a78d6", edgecolor="white", linewidth=0.4)
    axes[1].set_title("blanks filled with the mean", loc="left", fontsize=9)
    axes[1].set_xlabel("age (years)")
    for ax in axes:
        ax.set_ylabel("passengers")
        ax.set_xticks(range(0, 81, 10))
    plots["spike"] = outdir / "spike.pdf"; save(fig, plots["spike"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
