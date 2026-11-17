---
layout: week
title: "Week 12: Other Techniques — imbalanced and time-series data"
week_number: 12
---

# Snow Day?

## Twenty-Five Years at the Airport

Every day, at the weather station of Gerald R. Ford International Airport in Grand Rapids, a few numbers get written down: the day's highest and lowest temperature, how much rain fell (with any snow melted down to water), how much new snow fell, how deep the snow on the ground is, and how hard and from where the wind blew. The National Oceanic and Atmospheric Administration (NOAA) collects these records from stations all over the world, and anyone can download them.

Grand Rapids sits about 30 miles east of Lake Michigan. In winter, cold air blowing across the open lake picks up moisture and drops it as **lake-effect snow** on West Michigan: in a typical winter, the airport gets about 77 inches of snow, more than 6 feet, a little at a time and sometimes a lot at once.

This reading asks two questions every forecaster asks, with 25 years of those records:

1. **How warm will it be tomorrow?** A number, predicted from what happened before. Pages 2 to 4.
2. **Will tomorrow bring big snow?** A yes/no question where "yes" is rare. Pages 5 to 7.

Both questions need new tools. The rows of this dataset are in **time order**, and the second question has a class that almost never happens.

**📥 Download the dataset: [weather.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/weather.csv)**

```python
import pandas as pd

weather = pd.read_csv("weather.csv", parse_dates=["date"])
weather.shape          # (9131, 8): every day from January 1, 2001 to December 31, 2025
```

| column | what it holds |
|:---|:---|
| `date` | the day |
| `high_f`, `low_f` | the day's highest and lowest temperature, in °F |
| `precip_in` | rain plus melted snow, in inches |
| `snow_in` | new snow that fell that day, in inches |
| `snow_depth_in` | snow on the ground, in inches |
| `wind_mph` | average wind speed, in miles per hour |
| `wind_dir_deg` | where the day's strongest wind came from, in compass degrees: 90 = east, 180 = south, 270 = west, 360 = north |

`parse_dates=["date"]` tells pandas that `date` holds dates, not plain text, so it can do date arithmetic with them.

Some records from 25 years: the hottest day was **104 °F** (July 6, 2012); the coldest high was **2 °F** (January 30, 2019, during the "polar vortex"); the snowiest day brought **13.6 inches** (March 2, 2002); and the deepest snow on the ground was **24 inches** (February 18, 2014), at the end of the snowiest winter in the file, with 116 inches in all.

## Rows in Time Order

![Line chart of the daily high temperature at the Grand Rapids airport from July 2013 to June 2015, with big-snow days (2 or more inches of new snow) marked as orange triangles. The highs follow a yearly wave, from the 80s and 90s °F in summer (96 on July 19, 2013) to the teens and single digits in winter (7 on February 19, 2015), and jump up and down by 10 to 30 degrees within a few days. All 34 big-snow days fall between November and March, on days with highs from 9 to 33 °F: 22 in the winter of 2013–14 and 12 in the winter of 2014–15.](images/weather_two_years.png)

Two years of highs show three things:

- **A cycle:** warm summers, cold winters, every year.
- **Spells:** a cold day is usually followed by another cold day. Weather comes in stretches that last several days.
- **Rare days:** the orange triangles, days with at least 2 inches of new snow, are few, and they all sit in the cold part of the year.

That second point is what makes this **time-series data**: rows in time order, where each value depends on the ones before it. Having a date column isn't enough. A list of patients with their birthdays has dates too, but one patient's blood pressure doesn't depend on the patient before. Here, today's high depends a lot on yesterday's.

## Check the Clock First

In a time series, the order of the rows **is** information, so check it before anything else. Is every day there, once, in order?

```python
weather["date"].diff().value_counts()      # 1 day: 9,130 times
```

`diff()` subtracts each row's date from the next one. Every gap is exactly one day: no missing days, no repeats. (A day with no row would quietly break everything on the next pages, which count **rows** to go back in time.)

Then the blanks:

```python
weather.isna().sum()       # wind_mph: 7, every other column: 0
```

The average wind speed is missing on 7 days. Reading 7's tools work here, with one rule from time series: fill a gap only with what was known **at that time**. Carrying the last known value forward does that:

```python
weather["wind_mph"] = weather["wind_mph"].ffill()      # "forward fill": copy the day before
```

Filling with the column's mean would use days from years later. Here that changes almost nothing, but it is a habit worth keeping: in a time series, the future must never leak into the past.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What makes the airport data a time series?**

- [x] Its rows are in time order, and each day's weather depends on the days before it: cold and warm spells last several days.
- [ ] It has a column called `date`.
- [ ] It has more than 9,000 rows.
- [ ] It was recorded by a government agency.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Because `weather["date"].diff().value_counts()` shows a gap of exactly one day 9,130 times, no column of the dataset has blanks.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Why fill the 7 missing wind speeds with `ffill()` rather than with the column's mean?**

- [x] `ffill()` copies the day before, which was known at the time; the mean uses days from later years, the future.
- [ ] The mean can't be computed when there are blanks.
- [ ] `ffill()` always gives more accurate values than the mean.
- [ ] Wind speeds must be whole numbers.

<!-- END QUESTION -->

# Same as Yesterday

## Learn From the Past, Forecast the Future

> 🔁 **From Readings 6 and 8:** split before modeling, and keep the test set locked until the end. MAE (mean absolute error) is the average size of a miss, in the label's own units.

The first task: forecast **the day's high temperature**, in °F. How should we split? A forecaster in the evening of December 31, 2019 knows everything up to that day and nothing after. So the honest test is to do exactly that: learn from the past, forecast the future.

```python
weather["day_of_year"] = weather["date"].dt.dayofyear      # 1 = January 1 ... 365 (366 in leap years)
weather["month"] = weather["date"].dt.month
calendar = ["day_of_year", "month"]
y = weather["high_f"]

learn = weather["date"] < "2020-01-01"       # learn from 2001–2019...
test = ~learn                                # ...and forecast 2020–2025
```

That gives about 6,900 days to learn from and **2,192** days to forecast. A random split, as in earlier readings, would scatter 2023 days among the training rows, and the model would learn from the days right around the ones it forecasts. Page 4 shows how much that flatters a model.

Start with what the calendar alone can tell. A random forest (Reading 9), with the day of the year and the month:

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

forest = RandomForestRegressor(random_state=1)
forest.fit(weather.loc[learn, calendar], y[learn])
mean_absolute_error(y[test], forest.predict(weather.loc[test, calendar]))      # 7.2 °F
```

The calendar forest misses by **7.2 °F** on a typical day. It has learned the yearly cycle: for each date, it predicts about the average high on that date in 2001–2019. Weather forecasters call that average the **climatology** of a date.

It also guesses **too cold**: 58.3 °F on average across 2020–2025, when the actual average was 59.5 °F. The years 2020–2025 were 1.2 degrees warmer than 2001–2019, and a tree can't predict outside what it has learned: each of its leaves is an average of training days. It will never forecast a level it hasn't seen.

## Lag Features

What the calendar forest is missing is what any person would use first: **what happened yesterday.** A cold spell in January 2024 is cold every day, whatever the average January is like.

A **lag feature** is a past value of the label, moved down into the current row. pandas does it with `shift`:

```python
weather["high_f"].shift(1)        # each row gets the value one row up: yesterday's high
```

| date | `high_f` | `shift(1)` | `shift(-1)` |
|:---|---:|---:|---:|
| Jan 1, 2001 | 24 | (blank) | 26 |
| Jan 2, 2001 | 26 | 24 | 27 |
| Jan 3, 2001 | 27 | 26 | 29 |
| Jan 4, 2001 | 29 | 27 | 36 |
| Jan 5, 2001 | 36 | 29 | 33 |

`shift(1)` moves each value **down** one row: on January 2, it holds January 1's high. January 1 has nothing before it, so pandas leaves a blank.

`shift(-1)` moves values **up**: it puts **tomorrow's** high into today's row. A model with that column would score almost perfectly, and be useless: when you make tomorrow's forecast, tomorrow hasn't happened. **A lag is always `shift(k)` with k of 1 or more, never negative.**

A **rolling feature** summarizes a recent window, such as the average high over the last 7 days. Shift first, so the window ends the day **before** the one being forecast:

```python
weather["high_f"].shift(1).rolling(7).mean()      # average of the 7 days before this one
```

Without the `shift(1)`, the window would include today's high: the answer, again.

Now build the features. Everything about yesterday, plus two more looks back:

```python
yesterday = []
for column in ["high_f", "low_f", "precip_in", "snow_in", "snow_depth_in", "wind_mph", "wind_dir_deg"]:
    weather[column + "_yesterday"] = weather[column].shift(1)
    yesterday.append(column + "_yesterday")
weather["high_f_2_days_ago"] = weather["high_f"].shift(2)
weather["high_mean_last_7"] = weather["high_f"].shift(1).rolling(7).mean()
lags = yesterday + ["high_f_2_days_ago", "high_mean_last_7"]

weather = weather.dropna().reset_index(drop=True)      # the first week has no 7-day average
y = weather["high_f"]
learn = weather["date"] < "2020-01-01"
test = ~learn
```

Dropping the blanks removes January 1 to 7, 2001: the days whose look back would fall before the data starts.

## The Score to Beat

Before any model, try **no model at all**: just copy the past. This is a **naive forecast**:

```python
for days in [1, 7, 365]:
    copy = weather["high_f"].shift(days)          # "the same as 1, 7 or 365 days ago"
    print(days, mean_absolute_error(y[test], copy[test]))
mean_absolute_error(y[test], weather.loc[test, "high_mean_last_7"])
```

| naive forecast | MAE on 2020–2025 |
|:---|---:|
| same as yesterday | 5.4 °F |
| average of the last 7 days | 7.0 °F |
| same as one year ago | 9.7 °F |
| same as one week ago | 9.8 °F |
| (calendar forest, for comparison) | 7.2 °F |

"Same as yesterday" beats the calendar forest by almost 2 degrees. Weather really does come in spells. A week ago, or a year ago, is too far back: the spell has changed.

**Always compute a naive forecast first.** It costs one line, and a model that can't beat it isn't worth running.

Now the forest with the calendar **and** the lags:

```python
forest.fit(weather.loc[learn, calendar + lags], y[learn])
mean_absolute_error(y[test], forest.predict(weather.loc[test, calendar + lags]))      # 4.7 °F
```

**4.7 °F**: better than copying yesterday (5.4) and much better than the calendar (7.2). It's right to within 5 degrees on 62% of the test days, against 43% for the calendar forest. And the "too cold" problem is gone: its average forecast for 2020–2025 is 59.5 °F, exactly the actual average. The lags carry the **level**: if the last few days were warm, the forecast is warm, whether or not the climate has shifted.

Yesterday's high does most of the work. In `forest.feature_importances_` it gets 0.88 of the total; the other columns share the rest. The temperatures alone (calendar, yesterday's high and low, two days ago, the 7-day average) reach 5.3 °F; yesterday's wind, rain and snow bring that down to 4.7.

![Line chart of daily highs in January and February 2024, from the test period. Black line with dots: what happened, including a cold snap down to 10 °F on January 15 and 11 on January 16, and a warm spell up to 73 °F on February 27. Blue dashed line: the forest that knows only the calendar, a slowly wiggling line mostly between 26 and 39 °F that misses both the cold snap and the warm days; for these two months it misses by 9.1 °F on average. Orange line: the forest that also knows yesterday's weather. It follows every swing about one day late, missing by 4.9 °F on average.](images/weather_forecast.png)

The orange line shows both the strength and the limit of lags. It follows every cold snap and warm spell, but **one day late**: it can't see a front coming until the day after it arrives. Its worst misses in 2020–2025, 20 degrees or more, all come on days when the high jumped or dropped 14 to 34 degrees from the day before.

> 🔁 **From Reading 6:** compare the days a model learned from with new days. The forest misses by **1.8 °F** on the days it learned from and by 4.7 °F on new days: it has memorized part of 2001–2019. Only the second number tells you how it forecasts.

> 📌 **One split:** these scores come from one stretch of time, 2020 to 2025. Another six years, with other cold snaps, would move every number.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

The highs on January 2, 3 and 4, 2001 were 26, 27 and 29 °F. In the row for January 3, `high_f.shift(1)` holds **[26]** and `high_f.shift(-1)` holds **[29]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Which of these columns would leak the answer into a forecast of the day's high?**

- [x] `weather["high_f"].shift(-1)`
- [ ] `weather["high_f"].shift(1)`
- [ ] `weather["high_f"].shift(7)`
- [ ] `weather["high_f"].shift(1).rolling(7).mean()`

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**The forest that knows only the calendar forecasts 2020–2025 about 1.2 °F too cold on average. Why?**

- [x] For each date it predicts about the average of 2001–2019 days on that date, and 2020–2025 were warmer; a tree can't forecast a level it has never learned from.
- [ ] Random forests always predict too low.
- [ ] It learned from the test years by mistake.
- [ ] The calendar columns were not scaled.

<!-- END QUESTION -->

# The Year on a Circle

## December 31 and January 1

As a number, `day_of_year` runs from 1 (January 1) to 365 (December 31). So the two days around New Year's midnight are **364 apart**, the farthest apart two days can be. On a calendar, they're neighbors, and so is their weather.

The fix: put the year on a **circle**, like a clock face, where a full turn is one year. Each day becomes an angle, and we keep two numbers for it, the angle's **sine** and **cosine**:

```python
import numpy as np

weather["day_sin"] = np.sin(2 * np.pi * weather["day_of_year"] / 365.25)     # 2π is one full turn
weather["day_cos"] = np.cos(2 * np.pi * weather["day_of_year"] / 365.25)
```

(365.25 is the average length of a year, leap years included.) On the circle, December 31 and January 1 sit side by side.

Why two numbers? With the sine alone, two different days would share almost the same number: February 1 and May 31 both have a sine of about 0.52. The pair (sine, cosine) is different for every day of the year, like the two coordinates of a point on the clock face.

## A Line That Can Bend

Which models care? Take linear regression (Reading 8), with nothing but the date:

```python
from sklearn.linear_model import LinearRegression

for columns in [["day_of_year"], ["day_sin", "day_cos"]]:
    line = LinearRegression().fit(weather.loc[learn, columns], y[learn])
    print(columns, mean_absolute_error(y[test], line.predict(weather.loc[test, columns])))
```

| linear regression on | MAE on 2020–2025 |
|:---|---:|
| `day_of_year`, a number | 17.3 °F |
| `day_sin` and `day_cos`, a circle | 7.1 °F |

![Line chart from July 1 to June 30, with New Year in the middle. Gray: the average high on each date in 2001–2019, a wave from about 85 °F in late July down to the high 20s and low 30s in January and back up. Orange: linear regression on the day of the year on a circle, a smooth wave that follows the gray line closely, from 85.0 °F in late July down to 31.6 in mid-January. Blue: linear regression on the day of the year as a plain number, two pieces of one straight, slowly rising line: from 58 °F on July 1 up to 66.8 on December 31, then a drop to 49.8 on January 1, and up again to 58 by June 30. It is far from the gray wave almost everywhere.](images/weather_circle.png)

With the day as a plain number, a straight line can only rise all year (or fall all year). Here it rises 0.047 °F a day, from 49.8 °F on January 1 to 66.8 °F on December 31, and then **jumps down 17 degrees at midnight on New Year**, where 365 turns into 1. It misses summer and winter alike: 17.3 °F on a typical day.

On the circle, the same linear regression draws a **wave**: 85.0 °F in late July, 31.6 °F in mid-January, passing smoothly through New Year. Its 7.1 °F is as good as the calendar forest's 7.2. Two columns turned a straight line into the shape of the year.

## Which Models Care?

The circle helps models that measure **distance** (kNN, Reading 5) or draw **straight lines** (linear and logistic regression). A tree splits a column into ranges, like "day of year above 330", and never measures how far 365 is from 1.

There is a second cycle in the data: the **compass**. A wind from 350° and a wind from 10° both come from the north, only 20° apart, but as plain numbers they are 340 apart. Same recipe, with degrees turned into a fraction of a turn:

```python
weather["wind_sin"] = np.sin(np.deg2rad(weather["wind_dir_deg_yesterday"]))     # 360 degrees = one turn
weather["wind_cos"] = np.cos(np.deg2rad(weather["wind_dir_deg_yesterday"]))
```

Now give kNN and a forest the day of the year, yesterday's high and low, and yesterday's wind direction, once as plain numbers and once on circles:

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

numbers = ["day_of_year", "high_f_yesterday", "low_f_yesterday", "wind_dir_deg_yesterday"]
circles = ["day_sin", "day_cos", "high_f_yesterday", "low_f_yesterday", "wind_sin", "wind_cos"]
knn = make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=10))
for model in [knn, RandomForestRegressor(random_state=1)]:
    for columns in [numbers, circles]:
        model.fit(weather.loc[learn, columns], y[learn])
        print(mean_absolute_error(y[test], model.predict(weather.loc[test, columns])))
```

| model | plain numbers | circles |
|:---|---:|---:|
| kNN, k = 10 | 5.10 °F | 5.09 °F |
| random forest | 5.05 °F | 5.05 °F |

Barely any change, for two reasons. The forest never measures distances, as expected. And for kNN, yesterday's high already says what season it is, and every day of the year has 19 copies from other years at exactly the same number, so its nearest neighbors rarely need to reach across New Year. **The circle matters most for linear models**, and for kNN when the neighbors are far apart. For trees, plain numbers are fine.

Should every cycle go on a circle? The circle says that neighbors on the cycle **behave alike**. That's true for days of the year (December 31 is like January 1) and for compass directions. Ask it before you use it: for people, Sunday is not much like Monday, even though they are neighbors in the week.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Linear regression on `day_of_year` as a plain number misses by 17.3 °F; on `day_sin` and `day_cos`, by 7.1 °F. Why?**

- [x] A straight line in the day number can only rise (or fall) all year and jumps at New Year; on the circle, the same linear model can draw a wave that rises to summer and falls back to winter.
- [ ] Sine and cosine are measured in °F.
- [ ] Two columns always give a better linear regression than one.
- [ ] The circle adds information about yesterday's weather.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A wind from 340° and a wind from 20° are **[40]** degrees apart on a compass, but **[320]** apart as plain numbers.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

A random forest needs the day of the year on a circle to forecast well, because a tree measures how far apart December 31 and January 1 are.

<!-- END QUESTION -->

# Replay the Past

## Cross-Validation in Time Order

> 🔁 **From Reading 6:** to choose features and knobs, use cross-validation on the training data, never the test set.

Page 2 scored each model once, on 2020–2025 📌. To compare features or knobs, we need cross-validation, and it must stay inside 2001–2019.

`KFold(shuffle=True)` from Reading 6 deals the days into 5 folds at random. For a time series, there is a better way: **replay the past**. `TimeSeriesSplit` cuts the days into blocks in time order. Fold 1 learns from the first block and forecasts the next one. Fold 2 learns from the first two blocks and forecasts the third. And so on: the learning stretch grows, and the forecast is always of the stretch right after it. This is called a **rolling window** (or "walk-forward") cross-validation.

```python
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score

weather["year"] = weather["date"].dt.year
X_dev, y_dev = weather.loc[learn], y[learn]          # 2001–2019 only: 2020–2025 stays locked
for fold, (learn_rows, check_rows) in enumerate(TimeSeriesSplit(n_splits=5).split(X_dev)):
    print(fold + 1, X_dev["date"].iloc[learn_rows[-1]], X_dev["date"].iloc[check_rows[0]], X_dev["date"].iloc[check_rows[-1]])
```

![Diagram of five rolling-window folds over the 2001–2019 learning years, one lane per fold. In each lane a blue bar (the days the forest learns from) starts in January 2001 and grows: to March 2004, May 2007, July 2010, September 2013 and November 2016. Right after it comes an orange bar (the next 1,155 days, a little over 3 years, which the forest forecasts) and then gray (not used). The error at the right: fold 1 5.0 °F, fold 2 4.6, fold 3 5.0, fold 4 5.0, fold 5 5.0. A last lane, the real test, learns from 2001–2019 and forecasts 2020–2025: 4.7 °F.](images/weather_rolling.png)

Each fold is a forecast someone could really have made on that date, knowing only what they knew then. The real test on page 2 is the same idea, one step further: learn from everything before 2020, forecast after.

Notice the difference from `KFold`: the first block (January 2001 to March 2004) is only ever learned from, never checked, because nothing comes before it.

## A Model That Knows Only the Date

Why not just shuffle? Try a model that knows nothing about the weather, only the **date**: the year and the day of the year.

```python
date_only = ["year", "day_of_year"]
forest = RandomForestRegressor(random_state=1)
for cv in [KFold(n_splits=5, shuffle=True, random_state=1), TimeSeriesSplit(n_splits=5)]:
    errors = -cross_val_score(forest, X_dev[date_only], y_dev, cv=cv, scoring="neg_mean_absolute_error")
    print(errors.round(1), errors.mean())
```

| folds | MAE in each fold | mean |
|:---|:---|---:|
| shuffled (`KFold`) | 5.1, 5.2, 5.5, 5.2, 5.4 | 5.3 °F |
| rolling (`TimeSeriesSplit`) | 9.4, 9.6, 9.0, 9.5, 10.0 | 9.5 °F |

The shuffled folds say that a model knowing only the date forecasts the high to within 5.3 °F: better than "same as yesterday" (5.4), with no weather at all. That's impossible, and the rolling folds say so: 9.5 °F, worse even than the calendar forest. On the real test, 2020–2025, this model misses by **9.1 °F**. The rolling folds told the truth; the shuffled ones did not.

What happened? With shuffled folds, every checked day has its **yesterday and its tomorrow** among the days the forest learned from. With the year and the day of the year, the forest finds them, and averages their highs. It isn't forecasting; it's peeking at the days around the answer. The future leaks in, just as when a model is scored on the rows it learned from (Reading 6). This model misses by only 1.8 °F on the days it learned from: it has memorized each year's weather, day by day. That is **overfitting**, and shuffled folds hide it, because each checked day sits right next to a memorized one.

Rolling folds can't be fooled this way. The checked days come **after** every day the forest learned from, as in real use.

## What Rolling Folds Say About the Forecast

Now page 2's forecast model, calendar and lags:

| folds | MAE in each fold | mean |
|:---|:---|---:|
| shuffled (`KFold`) | 4.7, 4.7, 4.9, 4.9, 4.9 | 4.84 °F |
| rolling, growing window | 5.0, 4.6, 5.0, 5.0, 5.0 | 4.93 °F |
| rolling, last 3 years only | 5.1, 4.8, 5.2, 5.2, 5.2 | 5.09 °F |
| rolling, last 6 years only | 5.0, 4.7, 5.1, 5.1, 5.0 | 4.98 °F |

With the lags, shuffling flatters the model only a little (4.84 against 4.93): yesterday's high is already in each row, so the days around the answer add little. But you can't know in advance which case you're in, and the date-only model shows how wrong shuffled folds can be. **For a time series, use rolling folds, always.** The real test (4.7 °F) landed inside the folds' range, 4.6 to 5.0.

The last two rows add `max_train_size` (in days) to `TimeSeriesSplit`. Each fold then learns only from the most recent stretch, a **fixed window**, instead of everything before it:

```python
TimeSeriesSplit(n_splits=5, max_train_size=365 * 3)       # learn from the last 3 years only
```

Here the fixed windows do worse: 5.09 with 3 years, 4.98 with 6, against 4.93 for everything. Old winters still teach about this winter. A fixed window wins when the old data **stops looking like today**: a station moved to a new spot, a new instrument, a system that changed its rules. Like any knob, the window size is chosen with the rolling folds.

To choose features or knobs with `GridSearchCV`, pass the same folds: `cv=TimeSeriesSplit(n_splits=5)`.

> 📌 **One split, five times:** rolling folds give a **range** (here 4.6 to 5.0 °F), not just a mean. Report the range: it says how much the error moves from one stretch of years to the next.

## A Toolbox for Time Series

| option | when to use it | how, in code |
|:---|:---|:---|
| check the clock | before any lag: lags count rows, not days, so a missing day shifts everything after it | `df["date"].diff().value_counts()`; fill gaps with `ffill()` |
| lag features | when recent values predict the next one; pick lags at the cycles (1 day, 1 week, 1 year) | `y.shift(k)`, with k of 1 or more, never negative |
| rolling features | a steadier summary of the recent past than any one lag | `y.shift(1).rolling(7).mean()`, also `.min()`, `.max()`, `.sum()` |
| calendar features | any date; trees take them as plain numbers | `.dt.dayofyear`, `.dt.month`, `.dt.dayofweek`, `.dt.hour` |
| cycles on a circle | linear models and kNN, when neighbors on the cycle behave alike (days of the year, hours, compass directions) | `np.sin(2 * np.pi * day / 365.25)` and `np.cos(...)` |
| naive forecast | always, first: the score any model must beat | `y.shift(1)` as the prediction |
| time split | always: learn from the past, test on the future, never a random split | a date cutoff, as on page 2 |
| rolling-window CV | choosing features and knobs; report the folds' range | `cv=TimeSeriesSplit(n_splits=5)` |
| fixed window | when old data stops looking like today | `TimeSeriesSplit(n_splits=5, max_train_size=...)` |

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**A forest that knows only the year and the day of the year scores 5.3 °F with shuffled folds and 9.5 °F with rolling folds. Which number should you believe, and why?**

- [x] 9.5 °F. With shuffled folds, each checked day's yesterday and tomorrow are among the learned days, and the forest copies their highs; rolling folds only check days after everything the forest learned from, as in real use.
- [ ] 5.3 °F, because shuffled folds mix all the years fairly.
- [ ] 5.3 °F, because it is lower.
- [ ] Neither: cross-validation doesn't work on time series.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Like `KFold`, `TimeSeriesSplit` checks every training day exactly once.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**When would a fixed window (`max_train_size`) be a better choice than learning from all the past?**

- [x] When old data stops looking like today, for example after the weather station moved to a new spot or got a new instrument.
- [ ] Always: recent data is always better.
- [ ] When the dataset has no missing days.
- [ ] Never: more data always wins.

<!-- END QUESTION -->

# A Rare Kind of Day

## Big Snow

The second question: **will today bring big snow?** Call a day a **big-snow day** when at least 2 inches of new snow fall: enough to shovel, plow and salt.

```python
weather["big_snow"] = (weather["snow_in"] >= 2).astype(int)      # 1 = at least 2 inches of new snow
weather["big_snow"].value_counts()       # 0: 8,799   1: 325
```

**325** of 9,124 days: **3.6%**, about 13 a winter, from 6 (2023–24) to 22 (2013–14). All but one fall between November and April.

> 🔁 **From Reading 5:** a lazy model that always predicts the most common class is the first score to beat. **Recall** = of the real positives, the share the model catches. **Precision** = of the days the model flags, the share that really are positive.

A lazy model that always says "no big snow" is right **96.4%** of the time, and catches **none** of the big-snow days.

This is **imbalanced data**: one class, the **majority** (ordinary days), far outnumbers the other, the **minority** (big-snow days). Here, 27 to 1. Accuracy rewards guessing the majority, so from now on we report **recall** and **precision** for the rare class.

## The Same Split

The forecast is made the evening before, so the features are page 2's "yesterday" columns, with the day of the year and yesterday's wind direction on circles (page 3):

```python
snow_features = ["high_f_yesterday", "low_f_yesterday", "precip_in_yesterday", "snow_in_yesterday",
                 "snow_depth_in_yesterday", "wind_mph_yesterday", "wind_sin", "wind_cos", "day_sin", "day_cos"]
X_train, y_train = weather.loc[learn, snow_features], weather.loc[learn, "big_snow"]
X_test, y_test = weather.loc[test, snow_features], weather.loc[test, "big_snow"]
```

The same time split: **260** big-snow days among the 6,932 training days (3.8%), and **65** among the 2,192 test days (3.0%).

The shares differ: the last six winters had fewer big snows. With rows that are **not** in time order (patients, songs, squares of forest), `train_test_split(X, y, stratify=y)` keeps the share of the rare class the same in both sets, so that a small minority isn't split unevenly by luck. With a time series, the split is by date, and the test winters are what they are: that difference is part of what the test measures.

## 97% Accurate, 3 Big Snows Caught

First, the naive forecast: "big snow yesterday, so big snow today." On the test days it flags 66 days and is right on 18: **recall 0.28, precision 0.27**. Storms that last two days are common enough to make that work some of the time.

Then logistic regression (Reading 9), scaled, on all 10 features:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy_score(y_test, y_pred), recall_score(y_test, y_pred), precision_score(y_test, y_pred)
```

| model | accuracy | recall | precision | days flagged |
|:---|---:|---:|---:|---:|
| lazy: "never big snow" | 97.0% | 0.00 | — | 0 |
| naive: "big snow yesterday" | 95.7% | 0.28 | 0.27 | 66 |
| logistic regression | 97.0% | 0.05 | 0.50 | 6 |

The model is **97.0% accurate, exactly as accurate as the lazy model.** In six years, it says "big snow" on 6 days. It's right on 3 of them, and misses the other **62** big snows. By recall, the naive forecast beats it six times over.

The slopes show what it learned: cold yesterday (slope −0.98 for yesterday's high, per standard deviation) and winter (+1.44 for `day_cos`, which is highest in January) push toward big snow; snow and rain yesterday push a little (+0.21, +0.16); the wind direction, almost nothing.

## Why the Model Leans Toward "No"

Logistic regression learns by making its mistakes on the training days as small as it can, and it counts every mistake the same way. With 27 ordinary days for every big snow, what is the cheapest way to make few mistakes?

Look at the winter days of 2001–2019, grouped by yesterday's high:

![Bar chart of the November-to-March days of 2001–2019, grouped by yesterday's high temperature, showing the percent of days with big snow. 10 °F or less: 1 of 12 (8%); 11 to 15: 10 of 55 (18%); 16 to 20: 30 of 125 (24%), the highest bar; 21 to 25: 43 of 218 (20%); 26 to 30: 51 of 361 (14%); 31 to 35: 51 of 494 (10%); 36 to 40: 30 of 460 (7%); 41 to 45: 17 of 370 (5%); 46 to 50: 13 of 296 (4%); 51 to 60: 7 of 333 (2%); over 60: 2 of 142 (1%). A dashed line at 50% is far above every bar.](images/weather_snow_share.png)

Even after the coldest days, big snow comes at most **one time in four**. Suppose a rule could use only yesterday's high. After a day of 16 to 20 °F, saying "big snow" would be right 30 times and wrong 95; saying "no" would be wrong only 30 times. In **every** group, "no" makes fewer mistakes. So the rule with the fewest mistakes says "no" everywhere.

The real model, with ten columns, finds a few corners where big snow is more likely, but the logic is the same. On its own training days, it calls **248 of the 260** big-snow days "no", and only 15 of the 6,672 ordinary days "big snow". Nothing about the snow days is hidden; they're just outnumbered. A model that minimizes mistakes overall gives up the rare days that sit among the common ones.

## A Storm It Saw Only After It Arrived

The Christmas blizzard of 2022 brought Grand Rapids four days of snow in a row. Here are the model's probabilities, each computed the evening before:

| day | new snow | probability of big snow |
|:---|---:|---:|
| Dec 22, 2022 | 3.8 in | 0.12 |
| Dec 23 | 7.5 in | 0.22 |
| Dec 24 | 10.5 in | 0.74 |
| Dec 25 | 2.7 in | 0.80 |

The model missed the first two days and caught the last two. It sees only yesterday's numbers from one airport: no radar, no weather maps, nothing about the storm on its way. So it can't see a storm before it arrives, only one that's already here. That's a real limit of these features, and no threshold or rebalancing will fix it. Still, the model ranks days: some evenings deserve a higher probability than others, and page 6 uses that.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Logistic regression is 97.0% accurate on the test days, exactly as accurate as the lazy model that never predicts big snow. What does that tell you?**

- [x] Accuracy hides the rare class: the model catches only 3 of the 65 big-snow days, and recall and precision show it.
- [ ] The model is as good as it can be.
- [ ] The test set has no big-snow days.
- [ ] The model and the lazy model make the same predictions on every day.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**After winter days with a high of 16 to 20 °F, big snow followed 30 times out of 125. Why would a rule that minimizes mistakes still say "no big snow" after such days?**

- [x] Saying "big snow" would be wrong 95 times; saying "no" is wrong only 30 times. In every group the big-snow days are the minority, so "no" always makes fewer mistakes.
- [ ] 16 to 20 °F is too cold for snow.
- [ ] The rule can't use temperatures below 20 °F.
- [ ] 30 big snows out of 125 days is more than half.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

With rows that are not in time order, `train_test_split(X, y, stratify=y)` keeps the **[share/proportion/percentage]** of the rare class the same in the training and the test set.

<!-- END QUESTION -->

# Where to Draw the Line

## Probabilities, Then a Threshold

> 🔁 **From Reading 9:** `predict` says "yes" when the probability is at least **0.5**. That 0.5 is the **threshold**, and choosing it means choosing which mistakes to make.

Moving the threshold is a knob, so we choose it with cross-validation on the training days, and with **rolling** folds, since this is a time series. Each training day gets a probability from a model that learned only from the days before it:

```python
chance = pd.Series(np.nan, index=y_train.index)         # each training day's probability of big snow
for learn_rows, check_rows in TimeSeriesSplit(n_splits=5).split(X_train):
    model.fit(X_train.iloc[learn_rows], y_train.iloc[learn_rows])
    chance.iloc[check_rows] = model.predict_proba(X_train.iloc[check_rows])[:, 1]
checked = chance.notna()          # 5,775 days, from March 10, 2004 on
```

The first block (2001 to early 2004) is only learned from, so it gets no probability. (With rows that aren't in time order, Reading 9's `cross_val_predict(model, X, y, cv=5, method="predict_proba")` does this loop in one line.)

Now count, at each threshold, how many days get flagged and how many of those really bring big snow:

```python
for threshold in [0.5, 0.3, 0.2, 0.15, 0.1, 0.07, 0.05, 0.04, 0.03]:
    flagged = chance[checked] >= threshold
    print(threshold, flagged.sum(), precision_score(y_train[checked], flagged), recall_score(y_train[checked], flagged))
```

| threshold | days flagged | precision | recall | accuracy |
|---:|---:|---:|---:|---:|
| 0.5 | 19 | 0.32 | 0.03 | 96.2% |
| 0.3 | 67 | 0.30 | 0.09 | 95.9% |
| 0.2 | 169 | 0.31 | 0.25 | 95.2% |
| 0.15 | 307 | 0.26 | 0.38 | 93.8% |
| 0.1 | 659 | 0.19 | 0.58 | 89.2% |
| 0.07 | 1,051 | 0.14 | 0.69 | 83.2% |
| 0.05 | 1,371 | 0.13 | 0.81 | 78.6% |
| 0.04 | 1,539 | 0.12 | 0.88 | 76.1% |
| 0.03 | 1,749 | 0.11 | 0.93 | 72.9% |

These 5,775 days hold 212 big snows. Read down the table:

- **At 0.5**, the model flags 19 days in 16 years and catches 3% of the big snows. Its accuracy, 96.2%, is a bit **below** the lazy model's 96.3% on the same days.
- **Lower the threshold**, and recall climbs: 25% at 0.2, 58% at 0.1, 81% at 0.05. Precision falls, from about 3 in 10 flagged days to about 1 in 8.
- **Accuracy falls** the whole way down, because every lower threshold trades a few missed big snows for many false alarms. Accuracy counts them the same. They are not.

## Who Pays for Each Mistake?

Picture two people using this forecast in the evening:

- **The road crew.** If big snow is coming, they spray brine on the main roads the night before. Brine is cheap; a missed storm means ice under the morning rush hour. They want **recall**, and can live with false alarms: a threshold of 0.05 sends them out on about 87 evenings a year and catches 81% of the big snows, though 7 of every 8 nights out are a false alarm.
- **A school principal**, deciding whether to text parents "a snow day is possible tomorrow". Too many false alarms, and parents stop reading the texts. They want **precision**: at 0.2, they send about 11 texts a year, about 3 in 10 are followed by big snow, and they warn about a quarter of the big snows. (At 0.5 they'd barely ever text, and wouldn't be right any more often.)

There is no right threshold in the data. It comes from what each mistake costs, and **who pays** for it: a tank of brine, an icy commute, a family's trust in the school's texts. The data scientist's job is to show the trade-off; the people who pay for the mistakes should help choose.

## On the Test Winters

With the threshold chosen, the test set opens once:

```python
model.fit(X_train, y_train)
p_test = model.predict_proba(X_test)[:, 1]
```

| threshold | big snows caught (of 65) | days flagged | precision |
|---:|---:|---:|---:|
| 0.5 | 3 | 6 | 0.50 |
| 0.2 | 16 | 52 | 0.31 |
| 0.1 | 33 | 233 | 0.14 |
| 0.05 | 55 | 513 | 0.11 |

The test winters tell the same story as the rolling folds: the road crew's 0.05 catches 55 of the 65 big snows (85%), with 513 nights out; the principal's 0.2 catches 16, and 3 texts in 10 are right.

> 📌 **One split:** 65 test big snows. One big snow is 1.5 points of recall.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

Six evenings get these probabilities of big snow: 0.30, 0.12, 0.08, 0.06, 0.03 and 0.02. Big snow came only after the evenings at 0.30 and 0.06. At a threshold of 0.05, the model flags **[4]** evenings. Its precision is **[0.5/.5/0.50/50%]** and its recall is **[1/1.0/100%]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**The road crew can spray brine cheaply, and a missed storm means icy roads at rush hour. Which threshold fits, and what is the price?**

- [x] A low one, like 0.05: it catches about 4 in 5 big snows, but most nights the crew goes out, no big snow comes.
- [ ] 0.5, because it has the highest accuracy.
- [ ] 0.5, because the model is right on half of the days it flags.
- [ ] Any threshold: recall and precision don't depend on it.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

The threshold should be chosen on the test winters, 2020–2025, because they are the most recent.

<!-- END QUESTION -->

# Rebalancing the Days

## Change What the Model Learns From

Moving the threshold changes how we read the model's probabilities, after training. The other family of fixes changes what the model **learns from**:

| method | what it does |
|:---|:---|
| class weights | each big-snow day counts about 26 times as much in the model's mistakes (6,672 ordinary days ÷ 260 big snows) |
| random oversampling | copies random big-snow days until there are as many as ordinary days |
| random undersampling | throws away random ordinary days until there are as few as big-snow days |
| SMOTE | makes new, synthetic big-snow days between real big-snow days that are close to each other |

Class weights are an option of the model itself: `LogisticRegression(class_weight="balanced")`. The other three come from **imbalanced-learn** (`import imblearn`), a library built on scikit-learn just for imbalanced data. (Colab has it; elsewhere, `pip install imbalanced-learn`.) Each method is a **sampler** with one job, `fit_resample(X, y)`, which returns a rebalanced `X` and `y`:

```python
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

X_smote, y_smote = SMOTE(random_state=1).fit_resample(X_train, y_train)
y_train.value_counts(), y_smote.value_counts()      # 6,672 and 260  ->  6,672 and 6,672
```

SMOTE made 6,412 synthetic big-snow days. How? Take two real big-snow days that are close to each other, shown here with two of the columns:

| big-snow day | yesterday's high | yesterday's snow |
|:---|---:|---:|
| A: Dec 16, 2005 | 34 °F | 0.5 in |
| B: Jan 7, 2009 | 31 °F | 0.8 in |

SMOTE picks a random spot on the line between them. One third of the way from A to B: 34 + (31 − 34) ÷ 3 = **33 °F**, and 0.5 + (0.8 − 0.5) ÷ 3 = **0.6 in**. That new day never happened, but it sits among big-snow days. (SMOTE does this with all 10 columns at once, choosing each day's partner among its 5 nearest big-snow neighbors.) The risk: the space between two big-snow days isn't always big-snow territory, and some synthetic days land among ordinary ones.

## Rebalance Only the Days It Learns From

imbalanced-learn has its own `make_pipeline`, which works like scikit-learn's with one difference: **a sampler runs only when the pipeline learns** (`fit`), never when it predicts. So in cross-validation, only the folds the model learns from get rebalanced, and each checked fold keeps the real mix of days.

```python
from imblearn.pipeline import make_pipeline as make_imb_pipeline
from sklearn.model_selection import cross_validate

options = {
    "nothing": make_pipeline(StandardScaler(), LogisticRegression()),
    "class weights": make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced")),
    "oversample": make_imb_pipeline(StandardScaler(), RandomOverSampler(random_state=1), LogisticRegression()),
    "undersample": make_imb_pipeline(StandardScaler(), RandomUnderSampler(random_state=1), LogisticRegression()),
    "SMOTE": make_imb_pipeline(StandardScaler(), SMOTE(random_state=1), LogisticRegression()),
}
for name, option in options.items():
    scores = cross_validate(option, X_train, y_train, cv=TimeSeriesSplit(n_splits=5), scoring=["recall", "precision"])
    print(name, scores["test_recall"].mean(), scores["test_precision"].mean())
```

| rebalancing | recall | precision |
|:---|---:|---:|
| nothing | 0.03 | 0.28 |
| class weights | 0.86 | 0.12 |
| oversample (copy big-snow days) | 0.86 | 0.12 |
| undersample (drop ordinary days) | 0.86 | 0.12 |
| SMOTE | 0.84 | 0.13 |

All four rebalancing methods land in the same spot, and you've seen that spot before: on the threshold table, **0.04** gives recall 0.88 and precision 0.12. For logistic regression, rebalancing mostly does what lowering the threshold does: it slides the line toward the ordinary days. (Not by chance, 0.04 is close to the share of big-snow days in the training data, 3.8%.)

So why rebalance at all? Undersampling reached the same spot while keeping only 1 ordinary day in 26, which makes training much faster on big data (and throws information away on small data). And rebalancing earns its keep with models that have no threshold to move, with very rare classes, and with grid searches: tune with `scoring="recall"` (or `"f1"`, which is high only when precision and recall both are), never with the default accuracy.

One warning: a rebalanced model learned from a world where half the days bring big snow. Its probabilities run far too high. Read them as scores for ranking days, not as real chances.

## SMOTE First, Then Split: a Leak

A common mistake: SMOTE the **whole** dataset, then split. SMOTE's synthetic days have no date, so after SMOTE-ing everything, people split at random:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Wrong order: synthetic big-snow days from ALL days, then a random split
X_all, y_all = SMOTE(random_state=1).fit_resample(weather[snow_features], weather["big_snow"])
X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=0.25, random_state=1, stratify=y_all)
y_hat = RandomForestClassifier(random_state=1).fit(X_tr, y_tr).predict(X_te)
recall_score(y_te, y_hat), precision_score(y_te, y_hat)      # 0.97, 0.97

# Right order: split by date; the pipeline makes synthetic days from the training days only
smote_forest = make_imb_pipeline(SMOTE(random_state=1), RandomForestClassifier(random_state=1))
y_hat = smote_forest.fit(X_train, y_train).predict(X_test)
recall_score(y_test, y_hat), precision_score(y_test, y_hat)      # 0.20, 0.19
```

The wrong order reports **recall 0.97 and precision 0.97**: a forecaster's dream. The right order: **0.20 and 0.19**. What happened?

- Most of the big-snow days in the wrong test set are **synthetic**, made from real days that are now in the training set: points on the line between two days the forest has seen. The forest has nearly seen them already. The score measures **memory**, not forecasting: overfitting, hidden by a leak.
- That test set is **50% big-snow days**. Grand Rapids is 3.6%. Its precision says nothing about a real winter, where 27 ordinary days surround every big snow.

**Rule: rebalance only the training data, after the split.** The `imblearn` pipeline does it for you, in cross-validation and in the final fit.

## Does Every Fix Work for Every Model?

Reading 9's random forest, four ways, scored once on the test winters. The last one is from imbalanced-learn too: `BalancedRandomForestClassifier` is a forest where each tree learns from its own **balanced** sample, the big-snow days and an equal number of ordinary days, both drawn with replacement.

```python
from imblearn.ensemble import BalancedRandomForestClassifier

forests = {
    "nothing": RandomForestClassifier(random_state=1),
    "class weights": RandomForestClassifier(class_weight="balanced", random_state=1),
    "SMOTE": make_imb_pipeline(SMOTE(random_state=1), RandomForestClassifier(random_state=1)),
    "balanced forest": BalancedRandomForestClassifier(sampling_strategy="all", replacement=True,
                                                      bootstrap=False, random_state=1),
}
for name, forest in forests.items():
    y_hat = forest.fit(X_train, y_train).predict(X_test)
    print(name, recall_score(y_test, y_hat), precision_score(y_test, y_hat), y_hat.sum())
```

| forest | recall | precision | days flagged |
|:---|---:|---:|---:|
| nothing | 0.05 | 0.75 | 4 |
| class weights | 0.00 | 0.00 | 2 |
| SMOTE | 0.20 | 0.19 | 69 |
| balanced forest | 0.68 | 0.11 | 385 |

(The extra settings of `BalancedRandomForestClassifier` just write out the newer versions' defaults, so every version builds the same forest.)

- **Class weights did nothing**, worse than nothing: 2 days flagged, both wrong. A fully grown tree keeps splitting until each leaf holds days of one class only; weighting a leaf that holds only ordinary days doesn't change its vote. For logistic regression, weights worked as well as SMOTE. **A fix that helps one model can do nothing for another: compare them with cross-validation.**
- **SMOTE** moved the forest a little: 13 big snows caught instead of 3.
- **The balanced forest** caught 44 of the 65, with 385 days flagged. It was also the fastest of the four: each tree learns from about 520 days (260 of each kind) instead of 6,932. Each tree throws most of the ordinary days away, but every tree throws away a different part.

And the plain logistic regression with its threshold moved to 0.05? It caught 55 big snows with 513 days flagged: more recall than the balanced forest, at about the same precision. On these features, **the simplest fix did as well as any.** Try the threshold first.

> 📌 **One split:** 65 test big snows. The forests' order could change with other winters; the lesson about class weights on full-grown trees wouldn't.

## A Toolbox for Imbalanced Data

| option | when to use it | how, in code |
|:---|:---|:---|
| look, and keep the share | first: count the rare class; stratify when rows are not in time order | `y.value_counts(normalize=True)`; `train_test_split(..., stratify=y)` |
| measure the rare class | always: recall and precision next to the lazy model, and as the scoring in CV | `recall_score`, `precision_score`, `f1_score`; `scoring="f1"` |
| move the threshold | the first fix for any model with probabilities; choose it with CV and the cost of each mistake | `model.predict_proba(X)[:, 1]`, then compare with a threshold |
| class weights | models that have the option, like logistic regression; barely moves full-grown trees | `class_weight="balanced"` |
| random oversampling | small data, where no row can be spared; not with deep trees, which memorize the copies | `RandomOverSampler` |
| random undersampling | a huge majority and slow training; not with few rows | `RandomUnderSampler` |
| SMOTE | few rare rows; models with no class weights, like kNN | `SMOTE` (`SMOTENC` when some columns are words) |
| balanced ensembles | forests, especially on big data: fast, and each tree sees a different part of the majority | `BalancedRandomForestClassifier` |
| rebalance after the split | every time you use a sampler: in CV, in grid search and in the final fit | `make_pipeline` from `imblearn.pipeline` |
| question the label | before any of it | page 8 |

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**For logistic regression, class weights, oversampling, undersampling and SMOTE all land near recall 0.86 and precision 0.12, about the same spot as the threshold 0.04. What does that suggest?**

- [x] For logistic regression, rebalancing mostly slides the line toward the ordinary days, much like lowering the threshold.
- [ ] The four methods are the same algorithm.
- [ ] Rebalancing is always useless.
- [ ] The threshold 0.04 rebalances the training data.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

SMOTE makes a synthetic day exactly halfway between big-snow day A (yesterday's high 34 °F, yesterday's snow 0.5 in) and big-snow day B (31 °F, 0.8 in). The synthetic day has yesterday's high **[32.5]** °F and yesterday's snow **[0.65/.65]** in.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**SMOTE on all the days and then a random split gives recall 0.97 and precision 0.97. Splitting by date first, with SMOTE inside the pipeline, gives 0.20 and 0.19. Which should you believe, and why?**

- [x] 0.20 and 0.19. In the wrong order, most test big-snow days are synthetic, made from days the forest learned from, and the test set is 50% big snow instead of 3.6%.
- [ ] 0.97 and 0.97, because SMOTE gives the model more big-snow days to learn from.
- [ ] 0.97 and 0.97, because a random split is fairer than a split by date.
- [ ] Both: they measure the same thing.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**`class_weight="balanced"` worked well for logistic regression but did nothing for a random forest of fully grown trees. Why?**

- [x] A fully grown tree splits until each leaf holds one class only, so weighting the days barely changes any leaf's vote.
- [ ] Random forests ignore all their options.
- [ ] Class weights only work with SMOTE.
- [ ] The forest had no big-snow days to learn from.

<!-- END QUESTION -->

# Counting Snow

## Rocks, Telephone Poles and Snowflakes

This week's chapter of Deborah Stone's *Counting* opens with a step counter:

> "You can't fiddle with your Fitbit . . . but your Fitbit can fiddle with you. Unlike rocks or telephone poles, people think and feel."

Stone calls it the **Fitbit Effect**: "the process of measuring people changes the way they behave." Count your steps and you take more of them.

Snow is like the rocks and the telephone poles. A forecast of 6 inches won't make one more flake fall. That's part of what makes weather a good place to learn forecasting: the thing being predicted holds still while we predict it.

But a forecast is always read by people, and they change. The road crew goes out, the school sends its text, and the grocery store runs out of bread and milk. And when the forecast is about **people** (how many bikes they'll rent, which customers will leave, where crimes will happen), the forecast can change the very thing it predicts. Whether a forecast "came true" then depends on what people did because of it.

## How Often Do You Measure Snow?

Even counting snow takes rules. On January 11–12, 1997, a lake-effect storm buried the Tug Hill Plateau, east of Lake Ontario. A volunteer snow spotter in Montague, New York measured the new snow on a white board, cleared the board, and measured again: six times in 24 hours. The six measurements added up to **77 inches**, more than the national 24-hour record. TV and the local weather office announced a new record.

The National Weather Service formed a committee to check. Its 1997 report found each of the six measurements valid, but not their sum:

> "NWS standards for climatological observations of snowfall require that no more than four observations, taken with a maximum frequency of once every six hours, be summed within any 24-hour period to compute the total snowfall for that period. More frequent measurements taken by clearing the snow board tend to increase totals."

Fresh snow settles under its own weight. Clear the board more often, and you measure more of it before it settles. So 77 inches never became the record. The record stayed at Silver Lake, Colorado: 76 inches, April 14–15, 1921. Except, the committee noted, that one wasn't a 24-hour measurement either:

> "It was an estimate derived by prorating a measured 87 inches in 27.5 hours to a 24-hour period."

Our label, "at least 2 inches of new snow", rests on the same kind of rules: a white board at the airport, a ruler, a schedule for clearing it. And the 2 inches is our choice. A 3-inch cutoff would give a rarer class and a different model. Lake-effect snow falls in narrow bands, too: the airport can get a dusting while a town 20 miles away gets buried. Before rebalancing anything, ask what the rare class **is**, who measured it, and by what rule.

## What Counts as Normal

When a forecaster says a day was "5 degrees above normal", the normal is a number NOAA computes: the average for that date over the last **30 years**. Every ten years, NOAA moves the window forward; today's normals are the averages of 1991 to 2020. That is page 4's **fixed window**, chosen on purpose: the climate changes, so old decades eventually stop describing today.

Our calendar forest learned the normals of 2001–2019 and guessed 1.2 °F too cold for 2020–2025. The forest with lags didn't, because yesterday's weather carries the present level. A model that knows only the average past assumes the future will look like it.

## Forecasts Are for Decisions

Adrian Mackenzie's *Machine Learners* describes what machine learning is for, most of the time:

> "It works to mediate future-oriented decisions (although all too often near-future decisions such as ad-click prediction)."

Tomorrow's weather is about as near-future as decisions get. The model in this reading never decides anything: it gives the evening a probability. The decision is the threshold, which turns a 0.06 into "send the brine trucks" or "don't text the parents". Choosing it means choosing whose mistakes count more. That isn't a fact in the data; it belongs to the people who pay for each mistake.

## Questions Worth Asking About Any Forecast

- **What did the model know when it made the forecast?** Lags of 1 or more, never a column from the future.
- **Does it beat a naive forecast?** "Same as yesterday" missed by 5.4 °F; "big snow yesterday" caught 28% of the big snows.
- **Were the folds in time order?** Shuffled folds promised 5.3 °F for a model that really missed by 9.1.
- **How much does the error move from fold to fold?** Report the range, not just one number.
- **How rare is the class, and what does the lazy model score?** 97% accuracy can mean 3 big snows caught out of 65.
- **Who chose the threshold, and who pays for each kind of mistake?**
- **What does the label measure, and by what rule?** A ruler, a board and a cutoff we picked.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What does the story of the Montague 77 inches show about labels?**

- [x] How a quantity is measured changes the count: clearing the board more often gives a bigger total, so a label like "big snow" depends on measurement rules as well as on the weather.
- [ ] Volunteer observers can't measure snow correctly.
- [ ] Lake-effect snow can't be measured.
- [ ] The national record is wrong and should be 77 inches.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Stone writes that "unlike rocks or telephone poles, people think and feel." How does that make a weather forecast different from a forecast of how many bikes people will rent?**

- [x] Snow doesn't react to the forecast, but people can: a bike forecast may change how many bikes people rent, while a snow forecast changes only what people do about the snow.
- [ ] Weather forecasts are always more accurate.
- [ ] Bike rentals are not a time series.
- [ ] There is no difference: both forecasts change the thing they predict.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

NOAA's "normal" high for a date is the average over every year since the station's records began.

<!-- END QUESTION -->
