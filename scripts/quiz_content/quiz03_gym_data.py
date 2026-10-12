"""Simulated campus-gym data behind Quiz 3 (scripts/quiz_content/quiz03.py).

There is no CSV on the course site -- the quiz only shows sample rows and
printed outputs. This script exists so those printed outputs (k-means
cluster summary, elbow/silhouette table, PCA variance shares) come from a
real run instead of being made up. Re-run it and paste the numbers into
quiz03.py if you change anything here:

    python scripts/quiz_content/quiz03_gym_data.py

Tables (all keyed the way the quiz describes):
    plans     -- plan (PK), monthly_fee
    members   -- member_id (PK), plan (FK -> plans, raw messy text),
                 avg_minutes, cardio_pct, calories
    checkins  -- member_id + month (PK), week_1..week_4 (wide)
    profile   -- one row per member WITH check-ins: visits_per_week (mean of
                 their week_ columns) joined to the members' numeric columns;
                 this is what k-means / PCA run on.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

SEED = 3
N_MEMBERS = 240
FEATURES = ["visits_per_week", "avg_minutes", "cardio_pct", "calories"]

# Hidden habits: (share, weekly-visit rate, minutes mean/sd, cardio % mean/sd)
GROUPS = {
    "cardio regulars": (0.35, 4.5, 45, 8, 80, 8),
    "lifters":         (0.30, 3.5, 80, 10, 20, 8),
    "occasional":      (0.35, 1.0, 35, 8, 50, 12),
}


def make_tables(seed=SEED):
    rng = np.random.default_rng(seed)
    names = list(GROUPS)
    shares = [GROUPS[g][0] for g in names]
    group = rng.choice(names, size=N_MEMBERS, p=shares)

    rows = []
    for i, g in enumerate(group, start=1):
        _, rate, m_mu, m_sd, c_mu, c_sd = GROUPS[g]
        minutes = float(np.clip(rng.normal(m_mu, m_sd), 15, 130))
        cardio = float(np.clip(rng.normal(c_mu, c_sd), 0, 100))
        # Cardio burns more per minute than lifting; calories inherit minutes' spread.
        calories = minutes * (5 + 5 * cardio / 100) + rng.normal(0, 25)
        rows.append(dict(member_id=f"M{i:03d}", group=g, rate=rate,
                         avg_minutes=round(minutes), cardio_pct=round(cardio),
                         calories=int(round(calories, -1))))
    members = pd.DataFrame(rows)

    plan_clean = rng.choice(["basic", "premium", "student-monthly"], size=N_MEMBERS, p=[0.3, 0.3, 0.4])
    members["plan_clean"] = plan_clean

    # Two months of check-ins; ~10% of members (new sign-ups) have none.
    chk = []
    has_checkins = rng.random(N_MEMBERS) > 0.10
    for (_, m), keep in zip(members.iterrows(), has_checkins):
        if not keep:
            continue
        for month in ["Sep", "Oct"]:
            weeks = rng.poisson(m["rate"], size=4).clip(0, 7)
            chk.append(dict(member_id=m["member_id"], month=month,
                            **{f"week_{w}": int(v) for w, v in enumerate(weeks, start=1)}))
    checkins = pd.DataFrame(chk)

    week_cols = ["week_1", "week_2", "week_3", "week_4"]
    long = checkins.melt(id_vars=["member_id", "month"], value_vars=week_cols,
                         var_name="week", value_name="visits")
    visits = long.groupby("member_id")["visits"].mean().rename("visits_per_week").reset_index()
    profile = pd.merge(visits, members, on="member_id", how="inner")
    profile["visits_per_week"] = profile["visits_per_week"].round(2)

    plans = pd.DataFrame({"plan": ["basic", "premium", "student-monthly"],
                          "monthly_fee": [25, 45, 15]})
    return plans, members, checkins, profile


def report(profile):
    X = profile[FEATURES].to_numpy()
    X_scaled = StandardScaler().fit_transform(X)
    print("profile rows:", len(profile))
    print("column std:", profile[FEATURES].std().round(1).to_dict())

    print("\nk | inertia | silhouette")
    for k in range(1, 9):
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
        sil = silhouette_score(X_scaled, km.labels_) if k > 1 else float("nan")
        print(f"{k} | {km.inertia_:.0f} | {sil:.2f}")

    km3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_scaled)
    profile = profile.assign(cluster=km3.labels_)
    summary = profile.groupby("cluster").agg(
        n_members=("member_id", "count"),
        visits_per_week=("visits_per_week", "mean"),
        avg_minutes=("avg_minutes", "mean"),
        cardio_pct=("cardio_pct", "mean"),
        calories=("calories", "mean"),
    ).round(1)
    print("\nk=3 cluster summary (original units):\n", summary)
    print("\ncluster vs hidden group:\n", pd.crosstab(profile["cluster"], profile["group"]))

    print("\nPCA unscaled shares:", PCA().fit(X).explained_variance_ratio_.round(3))
    print("PCA scaled shares:  ", PCA().fit(X_scaled).explained_variance_ratio_.round(3))
    print("PCA scaled PC1 loadings:", PCA().fit(X_scaled).components_[0].round(2))
    return profile


if __name__ == "__main__":
    plans, members, checkins, profile = make_tables()
    print("members:", members.shape, "checkins:", checkins.shape)
    print("members without check-ins:", (~members["member_id"].isin(checkins["member_id"])).sum())
    profile = report(profile)
    print(members.head(12))
    print(checkins.head(12))
