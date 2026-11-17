<!--
Source for class_w12d2_handout.pdf, the printed activities for class_w12d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w12d2_handout.py   (about 30 seconds)

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: week, forecast, circle, rolling
                       (drawn by the script from datasets/bikes.csv, same hours and models as the slides)
                       optional width, e.g. ![](plot:forecast){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
  - a table with 4+ dashes in a column of its |---| row (the last one) spans the page in small type;
    its columns are as wide as their dashes
  - symbols like ≤ ≈ vanish in the PDF's font: write them out in words
Part 2's rentals are the first five hours of datasets/bikes.csv (5:00 had 1 bike, for shift(-1) at 4:00).
Answers. Part 3: line A = the circle, line B = the hour as a number (11 pm 276, midnight 59: the jump; test MAE 155 vs 125); Sunday
and Monday are neighbors on the clock but not alike for bikes (a weekend column fits better).
Part 4: fold k learns from Jan 2011 up to its check stretch, then checks the next 90 days; fold 1 learned from
winter only (no warm days, no spring crowds). Fold MAEs 55, 30, 23, 31, 42; shuffled folds 22 each.
This comment block is not printed.
-->

# DATA 202 — Time-Series Data · Week 12 Wednesday

Capital Bikeshare in Washington, D.C.: bikes rented each hour, 2011–2012. Your professor will tell you when to do each part.

## 1 · One week

![](plot:week){width=96%}

Bikes rented each hour, Monday, September 10, to Sunday, September 16, 2012.

1. **Label** the morning and the evening commute on one weekday.
2. **Circle** the weekend.
3. Your prediction for Monday, September 17, at 8 am: ________ bikes. **Pair talk:** what are you basing it on?

## 2 · What the forest is missing

![](plot:forecast){width=100%}

A random forest learned from the clock and the weather, January 2011 to June 2012. Then it forecast the next six months, July to December 2012.

1. **Shade** the gap between the forecast and what happened.
2. **Pair talk:** why does the forest guess too low? Look at what it learned from.

| Jan 1, 2011 | 0:00 | 1:00 | 2:00 | 3:00 | 4:00 |
|:--|:-:|:-:|:-:|:-:|:-:|
| `rentals` | 16 | 40 | 32 | 13 | 1 |
| `rentals.shift(1)` | _____ | _____ | _____ | _____ | _____ |
| `rentals.shift(-1)` | _____ | _____ | _____ | _____ | _____ |

3. **Fill in** both rows. (At 5:00, 1 bike was rented.)
4. **Pair talk:** which row could the forest really have when it makes its prediction?

\newpage

## 3 · The clock on a circle

![](plot:circle){width=100%}

Left: each hour as two numbers, `hour_sin` and `hour_cos`. Right, noon to noon: linear regression (Week 10) on the hour alone, with the hour as a number or on the circle.

1. **Label** lines A and B: which one had `hour` as a number?
2. **Circle** where that line jumps. Why there? ______________
3. **Pair talk:** on a circle, Sunday sits next to Monday. Should the day of the week go on a circle too?

## 4 · Replay the past

![](plot:rolling){width=100%}

Each fold learns from everything before a date, then checks the next 90 days. Right: each fold's typical miss (MAE, bikes per hour), for a forest with clock, weather and lags.

1. **Draw** folds 2 to 5 like fold 1: shade what each fold learns from, and box what it checks.
2. Fold 1 misses most. In the line on top, what had its forest never seen? ______________
3. **Pair talk:** shuffled folds (Week 7) promise 22 in every fold. In June 2012, what do you tell the company?

## Today's options

| option | why it helps | when to use it | in code |
|-----|--------|---------|----------|
| check the clock | lags count rows, not hours | before any lag | `time.diff().value_counts()` |
| lags, rolling means | carry the recent level | recent values predict the next | `y.shift(24)`, `.shift(1).rolling(24).mean()` |
| clock features | daily, weekly, yearly cycles | any timestamp; fine for trees | `.dt.hour`, `.dt.dayofweek`, `.dt.month` |
| clock on a circle | 11 pm next to midnight | kNN, linear models | `np.sin(2*np.pi*h/24)`, `np.cos(...)` |
| clock as categories | any shape over the day | linear models, plenty of data | `OneHotEncoder()` on `hour` |
| naive forecast | the score to beat | always, first | `y.shift(168)` as the forecast |
| time split | test on the future | always; never shuffle | `train = time < cutoff` |
| rolling window CV | replays the past, fold by fold | choosing features and knobs | `cv=TimeSeriesSplit(5)` |
| fixed window | learns from recent data only | old data no longer fits today | `max_train_size=...` |
