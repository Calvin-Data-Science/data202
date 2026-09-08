# DATA 202 --- Quiz 2

Week 4 --- Covering Week 3: Cleaning, Grouping & Plots

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 2`, which
generates `quiz02_A.pdf` and `quiz02_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: People Experiencing Homelessness

`homeless` contains 100 simulated records of people experiencing
homelessness, cleaned the same way as in Monday's class: standardized city
names, shelter status, and education levels.

**Columns:** `id`, `years_homeless`, `family_size`, `monthly_support_usd`
(numerical) \textperiodcentered\ `name`, `city`, `shelter_status`,
`education_level` (categorical/text)

**First few rows (already cleaned):**

**Version A sample rows:**

| id | name | city | shelter_status | years_homeless | family_size | monthly_support_usd | education_level |
|---|---|---|---|---|---|---|---|
| 1 | Peter | New York | shelter | 6 | 1 | 186 | None |
| 5 | Joseph | San Francisco | shelter | 2 | 5 | 37 | Higher |
| 11 | Miguel | Chicago | unsheltered | 9 | 5 | 195 | Higher |
| 17 | Joseph | Los Angeles | unsheltered | 12 | 1 | 273 | Higher |
| 27 | John | San Francisco | shelter | 9 | 2 | 464 | None |

**Version B sample rows:**

| id | name | city | shelter_status | years_homeless | family_size | monthly_support_usd | education_level |
|---|---|---|---|---|---|---|---|
| 2 | Joseph | Boston | street | 10 | 2 | 366 | None |
| 8 | Lucas | San Francisco | shelter temporary | 8 | 2 | 25 | Primary |
| 21 | Lucas | Boston | unsheltered | 9 | 5 | 84 | None |
| 39 | Anna | Los Angeles | shelter | 12 | 5 | 556 | Primary |
| 59 | David | San Francisco | shelter | 11 | 2 | 264 | Secondary |

## Question 1 (SLO 03A)

**Version A:**

Answer:
```python
homeless["shelter_status"] = (
    homeless["shelter_status"]
    .str.strip()
    .str.lower()
    .str.replace(r"^sheltered$", "shelter", regex=True)
)
```

**Version B:**

Answer:
```python
homeless["shelter_status"] = (
    homeless["shelter_status"]
    .str.strip()
    .str.lower()
    .str.replace(r"shelter\s*,\s*pending", "shelter pending", regex=True)
)
```

## Question 2 (SLO 03B)

**Version A:**

Answer:
```python
result = (
    homeless.groupby("city")["monthly_support_usd"]
    .mean()
    .reset_index()
    .sort_values("monthly_support_usd", ascending=False)
)
```

With `ascending=True`, cities would be sorted from LOWEST average to HIGHEST instead of highest to lowest.

**Version B:**

Answer:
```python
result = homeless.groupby("education_level").agg(
    n_people=("id", "count"),
    avg_years=("years_homeless", "mean"),
)
```

Median would be LESS sensitive to the outlier (it resists extreme values); mean would be pulled toward the outlier.

## Question 3 (SLO 03C)

**Version A:**

| Question | Answer |
|---|---|
| What's the distribution of `monthly_support_usd` across all people? | Histogram -- x=monthly_support_usd |
| How do `years_homeless` and `monthly_support_usd` relate to each other? | Scatter -- x=years_homeless, y=monthly_support_usd |
| How does average `monthly_support_usd` change as `years_homeless` increases? | Line -- x=years_homeless, y=avg(monthly_support_usd) |
| How does average `monthly_support_usd` compare across `city` values? | Bar -- x=city, y=avg(monthly_support_usd) |

**Version B:**

| Question | Answer |
|---|---|
| What's the distribution of `years_homeless` across all people? | Histogram -- x=years_homeless |
| How do `family_size` and `monthly_support_usd` relate to each other? | Scatter -- x=family_size, y=monthly_support_usd |
| How does average `family_size` change as `years_homeless` increases? | Line -- x=years_homeless, y=avg(family_size) |
| How does average `years_homeless` compare across `shelter_status` values? | Bar -- x=shelter_status, y=avg(years_homeless) |

## Question 4 (SLO 02A) --- Review from Quiz 1

**Version A:**

| # | Command | Answer |
|---|---|---|
| 1 | `homeless["monthly_support_usd"]` | Access -- Column |
| 2 | `homeless["high_support"] = homeless["monthly_support_usd"] > 400` | Add -- Column |
| 3 | `homeless = pd.concat([homeless, pd.DataFrame([new_row])], ignore_index=True)` | Add -- Row |
| 4 | `homeless = homeless[homeless["shelter_status"] != "street"]` | Delete -- Row(s) |
| 5 | `homeless = homeless.drop(columns=["notes"])` | Delete -- Column |

**Version B:**

| # | Command | Answer |
|---|---|---|
| 1 | `homeless["years_homeless"]` | Access -- Column |
| 2 | `homeless["long_term"] = homeless["years_homeless"] > 10` | Add -- Column |
| 3 | `homeless = pd.concat([homeless, pd.DataFrame([new_row])], ignore_index=True)` | Add -- Row |
| 4 | `homeless = homeless[homeless["city"] != "Boston"]` | Delete -- Row(s) |
| 5 | `homeless = homeless.drop(columns=["family_size"])` | Delete -- Column |

## Question 5 (SLO 02B) --- Review from Quiz 1

**Version A:**

Answer:
```python
result = homeless[(homeless["shelter_status"] == "street") & (homeless["years_homeless"] > 10)]
result = result.sort_values("years_homeless", ascending=False)
```

**Version B:**

Answer:
```python
result = homeless[(homeless["city"] == "San Francisco") & (homeless["monthly_support_usd"] < 100)]
result = result.sort_values("monthly_support_usd", ascending=True)
```

## Question 6 (SLO 02C) --- Review from Quiz 1

**Version A:**

```python
px.scatter(homeless, x="years_homeless", y="monthly_support_usd",
           symbol="shelter_status", size="family_size",
           title="Years Homeless vs. Monthly Support")
```

| Channel | Answer |
|---|---|
| x-axis | years_homeless -- Numerical |
| y-axis | monthly_support_usd -- Numerical |
| symbol | shelter_status -- Categorical |
| size | family_size -- Numerical |

Plus a blank sketch box for the student to draw their prediction of the chart.

**Version B:**

```python
px.scatter(homeless, x="family_size", y="monthly_support_usd",
           symbol="education_level", size="years_homeless",
           title="Family Size vs. Monthly Support")
```

| Channel | Answer |
|---|---|
| x-axis | family_size -- Numerical |
| y-axis | monthly_support_usd -- Numerical |
| symbol | education_level -- Categorical |
| size | years_homeless -- Numerical |

Plus a blank sketch box for the student to draw their prediction of the chart.

