# DATA 202 --- Quiz 2

Week 4 --- Covering Week 3: Cleaning, Grouping & Plots

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 2`, which
generates `quiz02_A.pdf` and `quiz02_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: Esports Players

`players` contains simulated records of competitive video game players, one
row per player. The rows below are the **raw** data, exactly as loaded from
the CSV. Question 1 works with this raw data; Questions 2--6 assume `players`
has already been cleaned (standardized city names, ladder status, and skill
levels).

**Columns:** `id`, `years_playing`, `sponsors`, `monthly_earnings_usd`
(numerical) \textperiodcentered\ `handle`, `city`, `ladder_status`,
`skill_level` (categorical/text)

**First few rows (raw --- before any cleaning):**

**Version A sample rows:**

| id | handle | city | ladder_status | years_playing | sponsors | monthly_earnings_usd | skill_level |
|---|---|---|---|---|---|---|---|
| 3 | NOVA | toronto | unranked | 10 | 4 | 422 | ADVANCED |
| 4 | blaze | SEOUL. | CASUAL | 14 | 3 | 37 | novice |
| 6 | viper | L.A. | ranked , pending | 9 | 5 | 552 | ADVANCED |
| 9 | pixel. | berlin | Ranked | 13 | 1 | 74 | expert |
| 44 | ghost | NEW-YORK | RANK | 13 | 1 | 171 | amateur |

**Version B sample rows:**

| id | handle | city | ladder_status | years_playing | sponsors | monthly_earnings_usd | skill_level |
|---|---|---|---|---|---|---|---|
| 15 | kiRA | NEW-YORK | Ranked | 14 | 4 | 579 | ADVANCED |
| 16 | ZEPHYR | SEOUL. | ranked , pending | 10 | 4 | 286 | AMATEUR |
| 35 | echo | berlin | unranked | 9 | 4 | 375 | EXPERT |
| 45 | mochi. | los Angeles | RANK | 5 | 2 | 90 | novice |
| 49 | NEO | toronto | CASUAL | 10 | 1 | 399 | ADVANCED |

## Question 1 (SLO 03A)

**Version A:**

```python
players["ladder_status"] = (
    players["ladder_status"]
    .str.strip()
    .str.lower()
    .str.replace(r"^rank$", "ranked", regex=True)
)
```

- `.str.strip()` removes leading/trailing whitespace.
- `.str.lower()` lowercases everything (`"Ranked"` → `"ranked"`, `"CASUAL"` → `"casual"`, `"RANK"` → `"rank"`).
- `.str.replace(r"^rank$", "ranked", regex=True)` rewrites values that are *exactly* `"rank"` to `"ranked"`. The `^` and `$` anchors matter: `"ranked"` and `"unranked"` both contain `"rank"`, so without them they would be mangled into `"rankeded"` and `"unrankeded"`.
- The result is assigned back to the column.

| id | ladder_status (raw) | ladder_status (after) |
|---|---|---|
| 3 | `unranked` | `unranked` |
| 4 | `CASUAL` | `casual` |
| 6 | `ranked , pending` | `ranked , pending` |
| 9 | `Ranked` | `ranked` |
| 44 | `RANK` | `ranked` |

**Version B:**

```python
players["ladder_status"] = (
    players["ladder_status"]
    .str.strip()
    .str.lower()
    .str.replace(r"ranked\s*,\s*pending", "ranked pending", regex=True)
)
```

- `.str.strip()` removes leading/trailing whitespace.
- `.str.lower()` lowercases everything (`"Ranked"` → `"ranked"`, `"CASUAL"` → `"casual"`, `"RANK"` → `"rank"`).
- `.str.replace(r"ranked\s*,\s*pending", "ranked pending", regex=True)` matches `"ranked"`, then any spaces, a comma, any spaces, then `"pending"`, and rewrites it as `"ranked pending"` (so `"ranked , pending"` → `"ranked pending"`).
- Nothing here turns `"rank"` into `"ranked"`, so `"RANK"` ends up as `"rank"`; `"unranked"` is untouched.

| id | ladder_status (raw) | ladder_status (after) |
|---|---|---|
| 15 | `Ranked` | `ranked` |
| 16 | `ranked , pending` | `ranked pending` |
| 35 | `unranked` | `unranked` |
| 45 | `RANK` | `rank` |
| 49 | `CASUAL` | `casual` |

## Question 2 (SLO 03B)

**Version A:**

Answer:
```python
result = (
    players.groupby("city")["monthly_earnings_usd"]
    .mean()
    .reset_index()
    .sort_values("monthly_earnings_usd", ascending=False)
)
```

**Version B:**

Answer:
```python
result = players.groupby("skill_level").agg(
    n_players=("id", "count"),
    avg_years=("years_playing", "mean"),
)
```

Median would be LESS sensitive to the outlier (it resists extreme values); mean would be pulled toward the outlier.

## Question 3 (SLO 03C)

**Version A:**

| Question | Answer |
|---|---|
| What's the distribution of `monthly_earnings_usd` across all players? | Histogram -- x=monthly_earnings_usd |
| How do `years_playing` and `monthly_earnings_usd` relate to each other? | Scatter -- x=years_playing, y=monthly_earnings_usd |
| How does average `monthly_earnings_usd` change as `years_playing` increases? | Line -- x=years_playing, y=avg(monthly_earnings_usd) |
| How does average `monthly_earnings_usd` compare across `city` values? | Bar -- x=city, y=avg(monthly_earnings_usd) |

**Version B:**

| Question | Answer |
|---|---|
| What's the distribution of `years_playing` across all players? | Histogram -- x=years_playing |
| How do `sponsors` and `monthly_earnings_usd` relate to each other? | Scatter -- x=sponsors, y=monthly_earnings_usd |
| How does average `sponsors` change as `years_playing` increases? | Line -- x=years_playing, y=avg(sponsors) |
| How does average `years_playing` compare across `ladder_status` values? | Bar -- x=ladder_status, y=avg(years_playing) |

## Question 4 (SLO 02A) --- Review from Quiz 1

**Version A:**

| # | Command | Answer |
|---|---|---|
| 1 | `players["monthly_earnings_usd"]` | Access -- Column |
| 2 | `players["high_earner"] = players["monthly_earnings_usd"] > 400` | Add -- Column |
| 3 | `players = pd.concat([players, pd.DataFrame([new_row])], ignore_index=True)` | Add -- Row |
| 4 | `players = players[players["ladder_status"] != "casual"]` | Delete -- Row(s) |
| 5 | `players = players.drop(columns=["skill_level"])` | Delete -- Column |

**Version B:**

| # | Command | Answer |
|---|---|---|
| 1 | `players["years_playing"]` | Access -- Column |
| 2 | `players["veteran"] = players["years_playing"] > 10` | Add -- Column |
| 3 | `players = pd.concat([players, pd.DataFrame([new_row])], ignore_index=True)` | Add -- Row |
| 4 | `players = players[players["city"] != "Berlin"]` | Delete -- Row(s) |
| 5 | `players = players.drop(columns=["sponsors"])` | Delete -- Column |

## Question 5 (SLO 02B) --- Review from Quiz 1

**Version A:**

Answer:
```python
result = players[(players["ladder_status"] == "casual") & (players["years_playing"] > 10)]
result = result.sort_values("years_playing", ascending=False)
```

**Version B:**

Answer:
```python
result = players[(players["city"] == "Seoul") & (players["monthly_earnings_usd"] < 100)]
result = result.sort_values("monthly_earnings_usd", ascending=True)
```

## Question 6 (SLO 02C) --- Review from Quiz 1

**Version A:**

```python
px.scatter(players, x="years_playing", y="monthly_earnings_usd",
           symbol="ladder_status", size="sponsors",
           title="Years Playing vs. Monthly Earnings")
```

| Channel | Answer |
|---|---|
| x-axis | years_playing -- Numerical |
| y-axis | monthly_earnings_usd -- Numerical |
| symbol | ladder_status -- Categorical |
| size | sponsors -- Numerical |

Plus a blank sketch box for the student to draw their prediction of the chart.

**Version B:**

```python
px.scatter(players, x="sponsors", y="monthly_earnings_usd",
           symbol="skill_level", size="years_playing",
           title="Sponsors vs. Monthly Earnings")
```

| Channel | Answer |
|---|---|
| x-axis | sponsors -- Numerical |
| y-axis | monthly_earnings_usd -- Numerical |
| symbol | skill_level -- Categorical |
| size | years_playing -- Numerical |

Plus a blank sketch box for the student to draw their prediction of the chart.

