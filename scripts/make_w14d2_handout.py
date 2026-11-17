"""
Build weeks/14/class_w14d2_handout.pdf -- the printed in-class activities for
Week 14 Wednesday (interpretability: a random forest on the mortgage data) --
from its editable source, weeks/14/class_w14d2_handout.md. Text and layout live
in the .md; the shared engine is scripts/handout.py. This script only draws the
plots, with the SAME forest, split and applicants as the notebook.

    importance  impurity importance (training) next to permutation importance (test accuracy lost), 8 columns;
                income is the big disagreement (0.12 vs 0.0001)
    ice         the forest's chance of denial for 100 test applicants with their debt-to-income set to each
                value (ICE lines), and their average (partial dependence)
    grids       applicants A (row 3389, denied for debt-to-income) and B (row 17464, denied for collateral):
                the forest's chance if only debt-to-income and loan-to-value changed; students shade >= 0.5

Usage:  python scripts/make_w14d2_handout.py   (about 30 seconds)
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "14" / "class_w14d2_handout.md"
OUT_PDF = ROOT / "weeks" / "14" / "class_w14d2_handout.pdf"
NUMBERS = ["debt_to_income", "loan_to_value", "loan_amount", "income", "property_value"]
WORDS = ["loan_purpose", "lien", "loan_type"]
APPLICANTS = {"A": 3389, "B": 17464}
DTI_ROWS = {33: "30–36", 40: "40", 45: "45", 49: "49", 55: "50–60", 65: "over 60"}
LTV_COLUMNS = [60, 70, 80, 90, 95, 101]
LABELS = {"debt_to_income": "debt-to-income", "loan_to_value": "loan-to-value", "loan_amount": "loan amount",
          "income": "income", "property_value": "property value", "loan_purpose": "loan purpose",
          "lien": "lien", "loan_type": "loan type"}

plt.rcParams.update(handout.PLOT_STYLE)


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_plots(outdir):
    mortgages = pd.read_csv(ROOT / "datasets" / "mortgages.csv")
    complete = mortgages.dropna(subset=["debt_to_income", "loan_to_value", "loan_amount"])
    X, y = complete[NUMBERS + WORDS], complete["decision"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)
    forest = Pipeline([
        ("prep", ColumnTransformer([("words", OneHotEncoder(handle_unknown="ignore"), WORDS)],
                                   remainder="passthrough", verbose_feature_names_out=False)),
        ("forest", RandomForestClassifier(min_samples_leaf=5, random_state=1, n_jobs=-1)),
    ]).fit(X_train, y_train)
    plots = {}

    # importance: two panels, each on its own scale
    impurity = pd.Series(forest[-1].feature_importances_, index=forest[0].get_feature_names_out())
    for column in WORDS:
        impurity[column] = impurity[impurity.index.str.startswith(column + "_")].sum()
    shuffled = permutation_importance(forest, X_test, y_test, n_repeats=10, random_state=1)
    table = pd.DataFrame({"impurity": impurity[NUMBERS + WORDS], "permutation": shuffled.importances_mean},
                         index=NUMBERS + WORDS).sort_values("impurity")
    print(table.round(4))
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.3), sharey=True)
    names = [LABELS[c] for c in table.index]
    axes[0].barh(names, table["impurity"], color="#2a78d6")
    axes[0].set_title("impurity (training)", fontsize=9.5)
    axes[0].set_xlabel("share of the splits' cleanup")
    axes[1].barh(names, table["permutation"], color="#eb6834")
    axes[1].set_title("permutation (test)", fontsize=9.5)
    axes[1].set_xlabel("accuracy lost when shuffled")
    for ax in axes:
        ax.grid(axis="y", visible=False)
    plots["importance"] = outdir / "importance.pdf"
    save(fig, plots["importance"])

    # ice: one line per applicant, and the average
    dti_values = [15, 25, 33] + list(range(36, 50)) + [55, 65]
    sample = X_test.sample(100, random_state=1)
    ice = pd.DataFrame({d: forest.predict_proba(sample.assign(debt_to_income=d))[:, 1] for d in dti_values},
                       index=sample.index)
    print("average:", ice.mean().round(2).to_dict())
    fig, ax = plt.subplots(figsize=(4.2, 2.9))
    for _, row in ice.iterrows():
        ax.plot(dti_values, row.values, color="#9a9a9a", lw=0.6, alpha=0.7)
    ax.plot(dti_values, ice.mean().values, color="#1f4e99", lw=2.6, label="average (partial dependence)")
    ax.plot([], [], color="#9a9a9a", lw=0.8, label="one applicant (ICE)")
    ax.set_xlim(12, 68)
    ax.set_ylim(0, 1)
    ax.set_xticks([15, 25, 33, 40, 45, 49, 55, 65])
    ax.set_xticklabels(["<20", "20–30", "30–36", "40", "45", "49", "50–60", ">60"], fontsize=7.5)
    ax.set_xlabel("debt-to-income (%), set for every applicant")
    ax.set_ylabel("forest's chance of denial")
    ax.legend(loc="upper left", fontsize=7)
    plots["ice"] = outdir / "ice.pdf"
    save(fig, plots["ice"])

    # grids: what-ifs around A and B, numbers only (students shade the denials)
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.5))
    for ax, (name, row) in zip(axes, APPLICANTS.items()):
        base = complete.loc[[row], NUMBERS + WORDS]
        what_if = pd.DataFrame([{"debt_to_income": d, "loan_to_value": v} for d in DTI_ROWS for v in LTV_COLUMNS])
        changed = base.loc[[row] * len(what_if)].reset_index(drop=True)
        changed[["debt_to_income", "loan_to_value"]] = what_if
        chance = forest.predict_proba(changed)[:, 1].reshape(len(DTI_ROWS), len(LTV_COLUMNS))
        print(name, "\n", np.round(chance, 2))
        for i in range(len(DTI_ROWS)):
            for j in range(len(LTV_COLUMNS)):
                ax.text(j, i, f"{chance[i, j]:.2f}", ha="center", va="center", fontsize=8.5)
        ax.set_xticks(range(len(LTV_COLUMNS)))
        ax.set_xticklabels([f"{v}%" for v in LTV_COLUMNS], fontsize=8)
        ax.set_yticks(range(len(DTI_ROWS)))
        ax.set_yticklabels(DTI_ROWS.values(), fontsize=8)
        ax.set_xlim(-0.5, len(LTV_COLUMNS) - 0.5)
        ax.set_ylim(len(DTI_ROWS) - 0.5, -0.5)
        ax.set_xticks(np.arange(-0.5, len(LTV_COLUMNS)), minor=True)
        ax.set_yticks(np.arange(-0.5, len(DTI_ROWS)), minor=True)
        ax.grid(which="minor", color="#999999", linewidth=0.6)
        ax.grid(which="major", visible=False)
        ax.tick_params(which="minor", length=0)
        ax.set_xlabel("loan-to-value")
        ax.set_ylabel("debt-to-income (%)")
        ax.set_title(f"applicant {name}", fontsize=10)
        for side in ["top", "right"]:
            ax.spines[side].set_visible(True)
    fig.tight_layout(w_pad=2.5)
    plots["grids"] = outdir / "grids.pdf"
    save(fig, plots["grids"])
    return plots


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
