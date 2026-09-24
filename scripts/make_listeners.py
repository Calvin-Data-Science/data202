"""
Generate datasets/listeners.csv -- the two-feature teaching dataset for
Week 5 Monday (k-means clustering, weeks/05/class_w05d1.ipynb).

180 fake music listeners, two numbers each:
    hours_per_week    average hours of music streamed per week (last month)
    distinct_artists  number of different artists streamed (last month)

The two features are on comparable scales (0-40), so k-means needs no
rescaling (scaling is a Week 9 topic), and there are only two of them so
students can see every point -- PCA doesn't arrive until Wednesday.

Four loose groups generate the data, but the group labels are NOT saved:
in class we pretend nobody knows them. Two groups (light + everyday
listeners) deliberately overlap, so "3 or 4 clusters?" is a real question --
the elbow method leans toward 4, the silhouette score slightly toward 3.

Usage:  python scripts/make_listeners.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# (count, (mean, sd) of hours_per_week, (mean, sd) of distinct_artists)
GROUPS = [
    (55, (6, 2.4), (8, 3.2)),     # light listeners: a little music, a few artists
    (35, (29, 4.0), (6, 2.5)),    # superfans: lots of hours, very few artists
    (40, (18, 3.5), (33, 5.0)),   # explorers: many different artists
    (50, (13, 3.2), (16, 4.0)),   # everyday listeners: in between
]


def main():
    rng = np.random.default_rng(1)
    blocks = [
        np.c_[rng.normal(h_mean, h_sd, n), rng.normal(a_mean, a_sd, n)]
        for n, (h_mean, h_sd), (a_mean, a_sd) in GROUPS
    ]
    X = np.vstack(blocks)
    X[:, 0] = np.clip(X[:, 0], 0.5, None).round(1)
    X[:, 1] = np.clip(X[:, 1], 1, None).round()
    X = X[rng.permutation(len(X))]  # shuffle so row order doesn't reveal the groups

    listeners = pd.DataFrame({
        "listener_id": [f"L{i:03d}" for i in range(1, len(X) + 1)],
        "hours_per_week": X[:, 0],
        "distinct_artists": X[:, 1].astype(int),
    })
    out = ROOT / "datasets" / "listeners.csv"
    listeners.to_csv(out, index=False, lineterminator="\n")
    print(f"Wrote {out} ({len(listeners)} rows)")


if __name__ == "__main__":
    main()
