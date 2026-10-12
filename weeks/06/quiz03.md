# DATA 202 --- Quiz 3

Week 6 --- Covering Weeks 4--5: Joins, Tidy Data, Clustering & PCA

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 3`, which
generates `quiz03_A.pdf` and `quiz03_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: Campus Gym

The campus gym keeps three related tables (simulated data). Every question
on this quiz uses them.

- `members` --- one row per gym member: `member_id`, the `plan` they signed
  up for (typed by hand at the front desk, so the **raw** text is messy), and
  their habits per visit: `avg_minutes` (minutes per visit), `cardio_pct`
  (\% of that time on cardio machines) and `calories` (calories burned per
  visit).
- `checkins` --- how many times a member came to the gym in each week
  (`week_1`--`week_4`) of a `month`.
- `plans` --- the gym's membership plans and their `monthly_fee` (dollars).

Question 7 works with the raw `plan` text. All other questions assume `plan`
has already been cleaned to `"basic"`, `"premium"` or `"student-monthly"`.

**First few rows of `members` (raw):**

**Version A sample rows:**

| member_id | plan | avg_minutes | cardio_pct | calories |
|---|---|---|---|---|
| M001 | Basic | 44 | 70 | 390 |
| M002 | BASIC | 51 | 71 | 420 |
| M003 | Prem | 34 | 43 | 290 |
| M004 | basic | 82 | 12 | 440 |
| M005 | Student - Monthly | 45 | 98 | 440 |

**Version A** -- **First few rows of `checkins`:**

| member_id | month | week_1 | week_2 | week_3 | week_4 |
|---|---|---|---|---|---|
| M002 | Sep | 6 | 5 | 6 | 2 |
| M002 | Oct | 6 | 1 | 2 | 4 |
| M003 | Sep | 2 | 1 | 0 | 0 |
| M003 | Oct | 0 | 0 | 0 | 1 |
| M004 | Sep | 5 | 2 | 1 | 4 |
| M006 | Sep | 4 | 3 | 3 | 4 |

**Version A** -- **All of `plans`:**

| plan | monthly_fee |
|---|---|
| basic | 25 |
| premium | 45 |
| student-monthly | 15 |

**Version B sample rows:**

| member_id | plan | avg_minutes | cardio_pct | calories |
|---|---|---|---|---|
| M006 | PREMIUM | 81 | 24 | 500 |
| M007 | Student-Monthly | 103 | 16 | 610 |
| M008 | prem | 46 | 85 | 400 |
| M009 | Basic | 49 | 49 | 370 |
| M010 | student - monthly | 38 | 74 | 340 |

**Version B** -- **First few rows of `checkins`:**

| member_id | month | week_1 | week_2 | week_3 | week_4 |
|---|---|---|---|---|---|
| M006 | Sep | 4 | 3 | 3 | 4 |
| M006 | Oct | 5 | 0 | 4 | 5 |
| M008 | Sep | 7 | 2 | 3 | 4 |
| M008 | Oct | 5 | 3 | 1 | 3 |
| M010 | Sep | 1 | 4 | 3 | 2 |
| M011 | Sep | 5 | 3 | 4 | 4 |
| M011 | Oct | 3 | 5 | 4 | 4 |

**Version B** -- **All of `plans`:**

| plan | monthly_fee |
|---|---|
| basic | 25 |
| premium | 45 |
| student-monthly | 15 |

## Question 1 (SLO 04A)

**Version A:**

| Table | Column | Answer |
|---|---|---|
| `members` | `member_id` | Primary key |
| `members` | `plan` | Foreign key -> plans |
| `plans` | `plan` | Primary key |
| `checkins` | `member_id` | Foreign key -> members (it repeats: one row per member per month) |
| `checkins` | `week_1` | Neither (a measurement, not an identifier) |

**Version B:**

| Table | Column | Answer |
|---|---|---|
| `checkins` | `member_id` | Foreign key -> members (it repeats: one row per member per month) |
| `plans` | `plan` | Primary key |
| `members` | `calories` | Neither (a measurement, not an identifier) |
| `members` | `plan` | Foreign key -> plans |
| `members` | `member_id` | Primary key |

## Question 2 (SLO 04B)

**Version A:**

| how= | rows |
|---|---|
| `"inner"` | 5 |
| `"left"` | 6 |
| `"right"` | 7 |
| `"outer"` | 8 |

M002 and M003 have 2 check-in rows each and M004 has 1, all matching a member, so inner = 5. Left (keep all check-ins) adds M006 (no member row) -> 6. Right (keep all members) adds M001 and M005 (no check-ins) -> 7. Outer adds all three -> 8.

**Version B:**

| how= | rows |
|---|---|
| `"inner"` | 5 |
| `"left"` | 7 |
| `"right"` | 7 |
| `"outer"` | 9 |

M006 and M008 have 2 check-in rows each and M010 has 1, all matching a member, so inner = 5. Left (keep all check-ins) adds M011's two rows (no member row) -> 7. Right (keep all members) adds M007 and M009 (no check-ins) -> 7. Outer adds all four -> 9.

## Question 3 (SLO 04C)

**Version A:**

```python
checkins_long = pd.melt(
    checkins,
    id_vars=["member_id", "month"],
    value_vars=["week_1", "week_2", "week_3", "week_4"],
    var_name="week",
    value_name="visits",
)
```

| member_id | month | week | visits |
|---|---|---|---|
| M002 | Sep | week_1 | 6 |
| M002 | Sep | week_2 | 5 |
| M002 | Sep | week_3 | 6 |
| M002 | Sep | week_4 | 2 |
| M002 | Oct | week_1 | 6 |
| M002 | Oct | week_2 | 1 |
| M002 | Oct | week_3 | 2 |
| M002 | Oct | week_4 | 4 |

8 rows: 2 wide rows x 4 week columns. Row order may differ (pd.melt actually lists all week_1 rows first, then week_2, ...); any order is fine.

**Version B:**

```python
checkins_long = pd.melt(
    checkins,
    id_vars=["member_id", "month"],
    value_vars=["week_1", "week_2", "week_3", "week_4"],
    var_name="week",
    value_name="visits",
)
```

| member_id | month | week | visits |
|---|---|---|---|
| M008 | Sep | week_1 | 7 |
| M008 | Sep | week_2 | 2 |
| M008 | Sep | week_3 | 3 |
| M008 | Sep | week_4 | 4 |
| M008 | Oct | week_1 | 5 |
| M008 | Oct | week_2 | 3 |
| M008 | Oct | week_3 | 1 |
| M008 | Oct | week_4 | 3 |

8 rows: 2 wide rows x 4 week columns. Row order may differ (pd.melt actually lists all week_1 rows first, then week_2, ...); any order is fine.

## Question 4 (SLO 05A)

**Version A:**

| member | visits_per_week | calories (hundreds) | closest |
|---|---|---|---|
| M11 | 1 | 1 | A |
| M12 | 1 | 3 | A |
| M13 | 1 | 2 | A |
| M14 | 4 | 3 | B |
| M15 | 5 | 4 | B |
| M16 | 6 | 2 | B |

New centroid A = (1, 2), new centroid B = (5, 3) -- the mean visits_per_week and mean calories of each centroid's members.

Assign: each member goes to the centroid at the smallest straight-line distance. Update: each centroid moves to the average of its members.

**Version B:**

| member | visits_per_week | calories (hundreds) | closest |
|---|---|---|---|
| M21 | 1 | 4 | A |
| M22 | 2 | 5 | A |
| M23 | 3 | 6 | A |
| M24 | 4 | 1 | B |
| M25 | 5 | 2 | B |
| M26 | 6 | 3 | B |

New centroid A = (2, 5), new centroid B = (5, 2) -- the mean visits_per_week and mean calories of each centroid's members.

Assign: each member goes to the centroid at the smallest straight-line distance. Update: each centroid moves to the average of its members.

## Question 5 (SLO 05B)

**Version A:**

**k = 3.** Inertia: the elbow is at 3 -- it falls steeply from k = 1 to 3 (852 → 436 → 165), then only slowly (139, 116, 96, ...). Silhouette: highest at k = 3 (0.61). Both agree. (Choosing k = 8 just because its inertia is lowest is wrong: inertia always drops as k grows.)

**Version B:**

**k = 3.** Inertia: the elbow is at 3 -- it falls steeply from k = 1 to 3 (852 → 436 → 165), then only slowly (139, 116, 96, ...). Silhouette: highest at k = 3 (0.61). Both agree. (Choosing k = 8 just because its inertia is lowest is wrong: inertia always drops as k grows.)

## Question 6 (SLO 05C)

**Version A:**

```python
PCA().fit(X_scaled).explained_variance_ratio_.round(3)
# [0.617  0.307  0.070  0.006]
```

**2 components**: 0.617 + 0.307 = 0.924, so they keep **92.4%** (PC1 alone is only 61.7%).

**Version B:**

```python
PCA().fit(X_scaled).explained_variance_ratio_.round(3)
# [0.617  0.307  0.070  0.006]
```

**3 components**: two keep 0.617 + 0.307 = 92.4% (< 95%); three keep 0.617 + 0.307 + 0.070 = **99.4%**.

## Question 7 (SLO 03A) --- Retake from Quiz 2

**Version A:**

```python
members["plan"] = (
    members["plan"]
    .str.strip()
    .str.lower()
    .str.replace(r"^prem$", "premium", regex=True)
)
```

| member_id | plan (raw) | plan (after) |
|---|---|---|
| M001 | `Basic` | `basic` |
| M002 | `BASIC` | `basic` |
| M003 | `Prem` | `premium` |
| M004 | `basic` | `basic` |
| M005 | `Student - Monthly` | `student - monthly` |

The `^...$` anchors mean only an *exact* `"prem"` is replaced. Nothing fixes the spaces in `"student - monthly"`, so M005 would still not match `plans`.

**Version B:**

```python
members["plan"] = (
    members["plan"]
    .str.strip()
    .str.lower()
    .str.replace(r"\s*-\s*", "-", regex=True)
)
```

| member_id | plan (raw) | plan (after) |
|---|---|---|
| M006 | `PREMIUM` | `premium` |
| M007 | `Student-Monthly` | `student-monthly` |
| M008 | `prem` | `prem` |
| M009 | `Basic` | `basic` |
| M010 | `student - monthly` | `student-monthly` |

`\s*-\s*` replaces a hyphen and any spaces around it with a bare hyphen. Nothing turns `"prem"` into `"premium"`, so M008 would still not match `plans`.

## Question 8 (SLO 03B) --- Retake from Quiz 2

**Version A:**

Answer:
```python
result = (
    members.groupby("plan")["calories"]
    .mean()
    .reset_index()
    .sort_values("calories", ascending=False)
)
```

**Version B:**

Answer:
```python
result = members.groupby("plan").agg(
    n_members=("member_id", "count"),
    median_cardio=("cardio_pct", "median"),
)
```

## Question 9 (SLO 03C) --- Retake from Quiz 2

**Version A:**

| Question | Answer |
|---|---|
| What's the distribution of `calories` across all members? | Histogram -- x=calories |
| How do `avg_minutes` and `calories` relate to each other? | Scatter -- x=avg_minutes, y=calories |
| How does the total number of `visits` change from `week_1` to `week_4` (using `checkins_long`)? | Line -- x=week, y=sum(visits) |
| How does average `cardio_pct` compare across `plan` values? | Bar -- x=plan, y=avg(cardio_pct) |

**Version B:**

| Question | Answer |
|---|---|
| What's the distribution of `avg_minutes` across all members? | Histogram -- x=avg_minutes |
| How do `cardio_pct` and `calories` relate to each other? | Scatter -- x=cardio_pct, y=calories |
| How does the average number of `visits` change from `week_1` to `week_4` (using `checkins_long`)? | Line -- x=week, y=avg(visits) |
| How many members are in each `cluster` (after running k-means)? | Bar -- x=cluster, y=count of members |

