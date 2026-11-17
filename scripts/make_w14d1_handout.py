"""
Build weeks/14/class_w14d1_handout.pdf -- the printed in-class activities for
Week 14 Monday (fairness, on Week 11's mortgage model) -- from its editable
source, weeks/14/class_w14d1_handout.md. Text and layout live in the .md; the
shared engine is scripts/handout.py. This script only draws the plot, with the
SAME model, split and applicants as the notebook.

    strips   twelve White and twelve Black TEST applicants (WHITE12, BLACK12), placed by Week 11's model's
             P(denied); orange triangles = the lender denied, gray circles = approved. Students draw the
             threshold at 0.2 (Part 1) and a second line for Black applicants (Part 2, about 0.30).

Usage:  python scripts/make_w14d1_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "14" / "class_w14d1_handout.md"
OUT_PDF = ROOT / "weeks" / "14" / "class_w14d1_handout.pdf"
# test applications (row labels of datasets/mortgages.csv), the same as the notebook's Handout 1 cell
WHITE12 = [1166, 2793, 6044, 12130, 8471, 9831, 9654, 14343, 18503, 17154, 3224, 1416]
BLACK12 = [8059, 9852, 15346, 1126, 3041, 2636, 6, 12204, 14654, 2525, 2393, 14674]

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    mortgages = pd.read_csv(ROOT / "datasets" / "mortgages.csv")
    numeric = ["debt_to_income", "loan_to_value", "loan_amount"]
    words = ["loan_purpose", "lien", "loan_type"]
    complete = mortgages.dropna(subset=numeric)
    X, y = complete[numeric + words], complete["decision"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)
    model = Pipeline([("prep", ColumnTransformer([("num", StandardScaler(), numeric),
                                                  ("words", OneHotEncoder(drop="first"), words)])),
                      ("logit", LogisticRegression(max_iter=5000))]).fit(X_train, y_train)
    test = complete.loc[X_test.index].copy()
    test["chance"] = model.predict_proba(X_test)[:, 1]

    fig, ax = plt.subplots(figsize=(7.4, 2.1))
    for level, rows in [(1, WHITE12), (0, BLACK12)]:
        strip = test.loc[rows].sort_values("chance")
        offsets = np.where(np.arange(len(strip)) % 2 == 0, 0.11, -0.11)          # stagger close neighbors
        for (_, row), dy in zip(strip.iterrows(), offsets):
            if row["decision"] == "denied":
                ax.scatter(row["chance"], level + dy, marker="^", s=70, color="#eb6834", zorder=3)
            else:
                ax.scatter(row["chance"], level + dy, marker="o", s=55, facecolors="white",
                           edgecolors="#555555", linewidths=1.3, zorder=3)
    ax.scatter([], [], marker="^", s=55, color="#eb6834", label="the lender denied")
    ax.scatter([], [], marker="o", s=45, facecolors="white", edgecolors="#555555", linewidths=1.3,
               label="the lender approved")
    ax.set_yticks([1, 0])
    ax.set_yticklabels(["White\napplicants", "Black\napplicants"])
    ax.set_ylim(-0.45, 1.45)
    ax.set_xlim(0, 0.8)
    ax.set_xticks(np.arange(0, 0.81, 0.1))
    ax.set_xticks(np.arange(0, 0.81, 0.05), minor=True)
    ax.grid(axis="x", which="minor", color="#eeeeee", linewidth=0.5)
    ax.grid(axis="y", visible=False)
    ax.axhline(0.5, color="#bbbbbb", linewidth=0.8)
    ax.set_xlabel("the model's chance of denial")
    ax.legend(loc="upper right", fontsize=7.5, ncol=2, bbox_to_anchor=(1, 1.22), frameon=False)
    plots = {"strips": outdir / "strips.pdf"}
    save(fig, plots["strips"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
