<!--
Source for class_w10d2_handout.pdf, the printed activities for class_w10d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w10d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: fit, slopes, alphas, ridgecurve
                       (drawn by the script from datasets/ames.csv: the same 25 houses,
                       X_train.sample(25, random_state=19), and 18 number columns as the slides)
                       optional width, e.g. ![](plot:ridgecurve){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Lasso (Part 5 of the slides), elastic net and the polynomial curve are on screen only.
This comment block is not printed.
-->

# DATA 202 — Ridge and Lasso · Week 10 Wednesday

Sale prices of houses in Ames, Iowa, from a line on 18 columns that learned from only 25 houses. Your professor will tell you when to do each part.

## 1 · Twenty-five houses

![](plot:fit){width=50%}

Each dot is a house: its actual price and the line's predicted price. On the dashed line, the prediction is perfect.

1. There are two kinds of dots: the **25 houses** the line learned from and **732 new houses**. **Label** each kind.
2. **Pair talk:** the line chose 19 numbers (18 slopes and an intercept) to fit 25 prices. Why does that make the 25 easy to fit? Why should we distrust the result?

## 2 · Slopes

![](plot:slopes){width=56%}

One slope per column, in dollars per typical step up in that column. Dark: learned from our 25 houses. Light: from all 2,193 training houses.

1. **Circle** three slopes that look too big or point the wrong way.
2. **Cross out** the columns that repeat another column.
3. **Pair talk:** `garage_cars` and `garage_area` got opposite slopes. Why might they cancel on the 25 houses but not on new ones?

\newpage

## 3 · Three alphas

![](plot:alphas){width=100%}

Ridge's slopes on the same 25 houses, for three values of alpha. At alpha = 1,000 the bars are there, just short: about \$1,000 each.

1. **Write** on each panel: *overfitting*, *about right* or *underfitting*.
2. **Pair talk:** with 25 *different* houses, which panel's slopes would change the most? Which would barely move? Is barely moving a good thing?

## 4 · Choose alpha

![](plot:ridgecurve){width=56%}

Ridge's typical miss in 5-fold cross-validation on the 25 houses.

1. **Circle** the best alpha.
2. **Label** the overfitting side and the underfitting side.
3. Here a *larger* alpha means a ____________ model. For trees, a *larger* `max_depth` meant a ____________ model.
