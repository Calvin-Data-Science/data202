# DATA 202 --- Quiz 4 Retake: Week 5

Retaking SLOs 05A--05C: Clustering & PCA

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 4 --variant retake05`, which
generates `quiz04_retake05_A.pdf` and `quiz04_retake05_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: Campus Library Readers

The campus library (simulated data, as in Quiz 4) built `readers`: one row
per student who used the library this fall (260 students), with four habits:

- `loans_per_month` --- how many books they borrow per month
- `avg_pages` --- the average length of the books they borrow (pages)
- `hours_per_week` --- hours they spend in the library per week
- `late_pct` --- the \% of their loans returned late

**A few rows of `readers`:**

**Version A sample rows:**

| student_id | loans_per_month | avg_pages | hours_per_week | late_pct |
|---|---|---|---|---|
| S001 | 2.3 | 220 | 2.8 | 21 |
| S002 | 1.2 | 180 | 2.0 | 13 |
| S003 | 4.7 | 370 | 2.8 | 27 |
| S004 | 3.2 | 250 | 13.4 | 0 |

**Version B sample rows:**

| student_id | loans_per_month | avg_pages | hours_per_week | late_pct |
|---|---|---|---|---|
| S005 | 10.6 | 420 | 2.8 | 8 |
| S006 | 2.1 | 240 | 11.4 | 1 |
| S007 | 3.3 | 250 | 12.1 | 5 |
| S008 | 4.5 | 410 | 2.6 | 8 |

## Question 1 (SLO 05A) --- Retake from Quiz 3

**Version A:**

| student | loans_per_month | hours_per_week | closest |
|---|---|---|---|
| S31 | 2 | 6 | A |
| S32 | 6 | 3 | B |
| S33 | 3 | 4 | A |
| S34 | 5 | 1 | B |
| S35 | 1 | 5 | A |
| S36 | 7 | 2 | B |

New centroid A = (2, 5), new centroid B = (6, 2) -- the mean loans_per_month and mean hours_per_week of each centroid's students.

Assign: each student goes to the centroid at the smallest straight-line distance. Update: each centroid moves to the average of its students.

**Version B:**

| student | loans_per_month | hours_per_week | closest |
|---|---|---|---|
| S41 | 4 | 6 | B |
| S42 | 1 | 1 | A |
| S43 | 5 | 7 | B |
| S44 | 2 | 3 | A |
| S45 | 6 | 5 | B |
| S46 | 3 | 2 | A |

New centroid A = (2, 2), new centroid B = (5, 6) -- the mean loans_per_month and mean hours_per_week of each centroid's students.

Assign: each student goes to the centroid at the smallest straight-line distance. Update: each centroid moves to the average of its students.

## Question 2 (SLO 05B) --- Retake from Quiz 3

**Version A:**

**k = 4.** Inertia: the elbow is at 4 -- it falls steeply from k = 1 to 4 (1040 → 658 → 379 → 185), then only slowly (164, 151, 139, 126). Silhouette: highest at k = 4 (0.59). Both agree. (Choosing k = 8 just because its inertia is lowest is wrong: inertia always drops as k grows.)

**Version B:**

**k = 4.** Inertia: the elbow is at 4 -- it falls steeply from k = 1 to 4 (1040 → 658 → 379 → 185), then only slowly (164, 151, 139, 126). Silhouette: highest at k = 4 (0.59). Both agree. (Choosing k = 8 just because its inertia is lowest is wrong: inertia always drops as k grows.)

## Question 3 (SLO 05C) --- Retake from Quiz 3

**Version A:**

```python
PCA().fit(X_scaled).explained_variance_ratio_.round(3)
# [0.456  0.306  0.195  0.043]
```

**2 components**: 0.456 + 0.306 = 0.762, so they keep **76.2%** (PC1 alone is only 45.6%).

**Version B:**

```python
PCA().fit(X_scaled).explained_variance_ratio_.round(3)
# [0.456  0.306  0.195  0.043]
```

**3 components**: two keep 0.456 + 0.306 = 76.2% (< 90%); three keep 0.456 + 0.306 + 0.195 = **95.7%**.

