<!--
Source for class_w12d2_handout.pdf, the printed activities for class_w12d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w12d2_handout.py   (about 30 seconds)

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: week, forecast, horizon
                       (drawn by the script from datasets/bikes.csv, same hours and models as the slides)
                       optional width, e.g. ![](plot:horizon){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 3's rentals are the first five hours of datasets/bikes.csv (5:00 had 1 bike, for shift(-1) at 4:00).
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

## 2 · The forecast

![](plot:forecast){width=58%}

A random forest learned from the clock and the weather, January 2011 to June 2012. Then it forecast the next six months.

1. **Shade** the gap between the forecast and what happened.
2. **Pair talk:** why does the forest guess too low? Look at what it learned from.

\newpage

## 3 · Shift by hand

| time | rentals | `rentals.shift(1)` | `rentals.shift(-1)` |
|:--|:-:|:-:|:-:|
| Jan 1, 2011, 0:00 | 16 | ________ | ________ |
| 1:00 | 40 | ________ | ________ |
| 2:00 | 32 | ________ | ________ |
| 3:00 | 13 | ________ | ________ |
| 4:00 | 1 | ________ | ________ |

1. **Fill in** both columns. (At 5:00, 1 bike was rented.)
2. **Pair talk:** which column could a model really have when it makes its prediction?

## 4 · How far ahead?

![](plot:horizon){width=58%}

A forest with the clock, the weather, the newest rentals we'd know, and the same hour last week. Its typical miss on July–December 2012, by how far ahead it forecasts.

1. **Explain** the dip at 24 hours: what is the newest value we know a day ahead? ____________
2. **Pair talk:** the bike company asks for next week's forecast. What would you tell them along with the number?
