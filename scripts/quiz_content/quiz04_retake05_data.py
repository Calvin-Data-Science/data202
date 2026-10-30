"""Simulated campus-library data behind the Week 5 retake quiz
(scripts/quiz_content/quiz04_retake05.py), which retakes SLOs 05A-05C next to Quiz 4.

There is no CSV on the course site -- the quiz only shows printed outputs.
This script exists so those outputs (elbow/silhouette table, PCA variance
shares) come from a real run instead of being made up, and to check the
by-hand k-means round of Question 1. Re-run it and paste the numbers into
quiz04_retake05.py if you change anything here:

    python scripts/quiz_content/quiz04_retake05_data.py

`readers`: one row per student who used the library this fall, with four
habits: loans_per_month, avg_pages (pages per borrowed book), hours_per_week
(spent in the library) and late_pct (% of loans returned late).
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

SEED = 5
N_READERS = 260
FEATURES = ["loans_per_month", "avg_pages", "hours_per_week", "late_pct"]

# Hidden habits: share, then (mean, sd) for each feature, in FEATURES order
GROUPS = {
    "bookworms":       (0.25, (8.0, 1.5), (380, 60), (3.0, 1.2), (10, 6)),
    "studiers":        (0.25, (2.0, 1.0), (250, 60), (12.0, 2.0), (5, 4)),
    "procrastinators": (0.20, (4.0, 1.2), (300, 60), (4.0, 1.5), (45, 10)),
    "casual":          (0.30, (1.5, 0.8), (180, 40), (1.5, 1.0), (15, 8)),
}

# Question 1: six students per version on a small integer grid
# (x = loans_per_month, y = hours_per_week); k = 2, starting centroids = two students.
Q1_POINTS = {
    "A": [("S31", 2, 6), ("S32", 6, 3), ("S33", 3, 4), ("S34", 5, 1), ("S35", 1, 5), ("S36", 7, 2)],
    "B": [("S41", 4, 6), ("S42", 1, 1), ("S43", 5, 7), ("S44", 2, 3), ("S45", 6, 5), ("S46", 3, 2)],
}
Q1_START = {"A": ("S35", "S34"), "B": ("S42", "S45")}


def make_readers(seed=SEED):
    rng = np.random.default_rng(seed)
    names = list(GROUPS)
    group = rng.choice(names, size=N_READERS, p=[GROUPS[g][0] for g in names])
    rows = []
    for i, g in enumerate(group, start=1):
        (loans, pages, hours, late) = GROUPS[g][1:]
        rows.append(dict(
            student_id=f"S{i:03d}", group=g,
            loans_per_month=round(float(np.clip(rng.normal(*loans), 0.5, 15)), 1),
            avg_pages=int(round(float(np.clip(rng.normal(*pages), 60, 900)), -1)),
            hours_per_week=round(float(np.clip(rng.normal(*hours), 0, 30)), 1),
            late_pct=int(round(float(np.clip(rng.normal(*late), 0, 100)))),
        ))
    return pd.DataFrame(rows)


def check_q1():
    for letter, points in Q1_POINTS.items():
        xy = {n: np.array([x, y]) for n, x, y in points}
        a, b = (xy[s] for s in Q1_START[letter])
        assign = {}
        for n, p in xy.items():
            da, db = np.sum((p - a) ** 2), np.sum((p - b) ** 2)
            assert da != db, f"tie for {n}"
            assign[n] = "A" if da < db else "B"
        new_a = np.mean([xy[n] for n in xy if assign[n] == "A"], axis=0)
        new_b = np.mean([xy[n] for n in xy if assign[n] == "B"], axis=0)
        print(f"Q1 version {letter}: {assign} -> new A {new_a}, new B {new_b}")


def report(readers):
    X_scaled = StandardScaler().fit_transform(readers[FEATURES])
    print("readers:", len(readers))
    print(readers.groupby("group")[FEATURES].mean().round(1))
    print("\nk | inertia | silhouette")
    for k in range(1, 9):
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
        sil = silhouette_score(X_scaled, km.labels_) if k > 1 else float("nan")
        print(f"{k} | {km.inertia_:.0f} | {sil:.2f}")
    km4 = KMeans(n_clusters=4, random_state=42, n_init=10).fit(X_scaled)
    print("\nk=4 clusters vs hidden groups:\n", pd.crosstab(km4.labels_, readers["group"]))
    print("\nPCA scaled shares:", PCA().fit(X_scaled).explained_variance_ratio_.round(3))


if __name__ == "__main__":
    check_q1()
    report(make_readers())
