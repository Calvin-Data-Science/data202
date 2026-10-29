<!--
Source for class_w10d2_handout.pdf, the printed activities for class_w10d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w10d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: thirty, alphas, ridgecurve
                       (drawn by the script from datasets/ames.csv: the same 30 houses,
                       X_train.sample(30, random_state=29), as the slides)
                       optional width, e.g. ![](plot:ridgecurve){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 4's table is typed in from the notebook's output (Lasso on Monday's 47 columns, 5-fold CV
on the 2,193 training houses, random_state=1). Change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Ridge and Lasso · Week 10 Wednesday

Sale price vs. living area for houses in Ames, Iowa. Your professor will tell you when to do each part.

## 1 · Thirty houses

![](plot:thirty){width=56%}

Thirty sales, a straight line and a degree-10 curve.

1. **Predict:** which model has the smaller RMSE on these 30 houses? ________ On *other* houses of the same sizes? ________
2. **Circle** two places where the curve follows a single house instead of the trend.
3. Which model is overfitting? ________________

## 2 · Three alphas

![](plot:alphas){width=100%}

Ridge's curve on the same 30 houses, for three values of alpha.

1. **Write** on each panel: *overfitting*, *about right* or *underfitting*.
2. **Pair talk:** with 30 different houses, which curve would change the most? Which would barely move? Is barely moving a good thing?

\newpage

## 3 · Choose alpha

![](plot:ridgecurve){width=56%}

Ridge's typical miss in 5-fold cross-validation on the 30 houses.

1. **Circle** the best alpha.
2. **Label** the overfitting side and the underfitting side.
3. Here a *larger* alpha means a ____________ model. For trees, a *larger* `max_depth` meant a ____________ model.

## 4 · What Lasso keeps

Back to all 2,193 training houses and Monday's 47 columns. Monday's line, with no penalty: CV RMSE **\$27,876**.

| alpha | columns kept (of 47) | CV RMSE |
|--:|--:|--:|
| 10 | 44 | \$27,857 |
| 100 | 32 | \$28,043 |
| 300 | 25 | \$28,563 |
| 1,000 | 15 | \$29,653 |
| 3,000 | 13 | \$31,310 |
| 10,000 | 9 | \$35,343 |
| 30,000 | 4 | \$51,003 |

1. Find the **simplest** model within \$1,000 of Monday's. alpha = ________, with ______ columns.
2. **Mark** the row that is underfitting.
3. **Pair talk:** Lasso dropped `second_floor_area` but kept `living_area`. Why might that cost almost nothing?
