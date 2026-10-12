<!--
Source for class_w10d2_handout.pdf, the printed activities for class_w10d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w10d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: ridgecurve
                       (drawn by the script from datasets/ames.csv, same houses and split as the slides)
                       optional width, e.g. ![](plot:ridgecurve){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 1's and part 3's tables are typed in from the notebook's output (5-fold CV on the 2,193
training houses, random_state=1). Change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Ridge and Lasso · Week 10 Wednesday

Same houses as Monday: 2,193 training houses in Ames, Iowa, and 5-fold cross-validation. Your professor will tell you when to do each part.

## 1 · More freedom

RMSE (typical miss, in dollars) of plain least squares, with and without the product columns.

| model | columns | folds it learned from | held-out fold | gap |
|:--|--:|--:|--:|:-:|
| Monday | 47 | $27,069 | $27,876 | ________ |
| with products | 237 | $19,548 | $28,958 | ________ |

1. Which model is overfitting? ________ How can you tell? ______________________
2. The products made the misses on *known* houses ________ and on *new* houses ________.

## 2 · Choose alpha

![](plot:ridgecurve){width=58%}

1. Ridge's typical miss for each alpha.
2. **Circle** the best alpha.
3. **Label** the overfitting side and the underfitting side.
4. Here a *larger* knob means a ________ model. For kNN, a *larger* k meant a ________ model.

\newpage

## 3 · What Lasso keeps

| alpha | columns kept (of 237) | CV RMSE |
|--:|--:|--:|
| 10 | 212 | $26,365 |
| 30 | 195 | $25,775 |
| 100 | 155 | $24,644 |
| 300 | 105 | $24,222 |
| 1,000 | 58 | $24,510 |
| 3,000 | 31 | $26,079 |
| 10,000 | 18 | $31,393 |

1. **Circle** the alpha with the lowest CV RMSE.
2. Find the **simplest** model within $500 of the best. alpha = ________, with ______ columns.
3. Lasso dropped `second_floor_area` but kept `living_area`. Why might that cost almost nothing? ______________________

______________________________________________________________
