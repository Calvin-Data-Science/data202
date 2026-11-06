"""
Build weeks/11/class_w11d1_handout.pdf -- the printed in-class activities for
Week 11 Monday (logistic regression, on Kent County mortgage decisions) -- from
its editable source, weeks/11/class_w11d1_handout.md. Text and layout live in
the .md; the shared engine is scripts/handout.py. This script only draws the plots.

    logistic  the logistic function p = 1 / (1 + e^-z), z from -6 to 6 (students mark A, B, C and draw arrows)
    curves    four S-curves of P(denied) vs. DTI, numbered 1-4, from the scores in CURVES (students match them)

Parts 2 and 3 have no plot (a table of slope signs, and a threshold table typed into the .md from the notebook).

Usage:  python scripts/make_w11d1_handout.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "11" / "class_w11d1_handout.md"
OUT_PDF = ROOT / "weeks" / "11" / "class_w11d1_handout.pdf"
BLUE = "#2a78d6"
# curve number -> (b0, b1); same as the notebook's form cell. Answers: a -> 4, b -> 2, c -> 1, d -> 3
CURVES = {1: (-6, 0.2), 2: (-25, 0.5), 3: (10, -0.2), 4: (-10, 0.2)}
STYLES = {1: "-", 2: "--", 3: "-.", 4: ":"}

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def make_plots(outdir):
    plots = {}

    # logistic: the bare function
    z = np.linspace(-6, 6, 300)
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.plot(z, sigmoid(z), color=BLUE, lw=2)
    ax.set_xticks(range(-6, 7, 1)); ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlim(-6, 6); ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("score $z$"); ax.set_ylabel("probability $p$")
    plots["logistic"] = outdir / "logistic.pdf"
    save(fig, plots["logistic"])

    # curves: four numbered S-curves (line styles too, for black-and-white printing)
    dti = np.linspace(0, 80, 400)
    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    label_at = {1: (18, 0.07), 2: (46, 0.07), 3: (24, -0.11), 4: (58, -0.11)}     # x, vertical offset from the curve
    for number, (b0, b1) in CURVES.items():
        p = sigmoid(b0 + b1 * dti)
        ax.plot(dti, p, color="black", lw=1.6, ls=STYLES[number])
        x, dy = label_at[number]; y = sigmoid(b0 + b1 * x)
        ax.text(x, y + dy, str(number), fontsize=11, fontweight="bold",
                ha="center", va="center", bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec="black", lw=0.8))
    ax.axhline(0.5, color="#999999", lw=0.8, ls=":")
    ax.set_xticks(range(0, 81, 10)); ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlim(0, 80); ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("debt-to-income, DTI (%)"); ax.set_ylabel("P(denied)")
    plots["curves"] = outdir / "curves.pdf"
    save(fig, plots["curves"])

    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
