<!--
Source for class_w10d1_handout.pdf, the printed activities for class_w10d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w10d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: scatter or overunder
                       (drawn by the script from datasets/ames.csv, same houses and split as the slides)
                       optional width, e.g. ![](plot:overunder){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 2's five houses are test houses 1117, 192, 45, 674 and 1770 (random_state=1), priced by the
one-line model; part 3's coefficients come from the notebook. Change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Linear Regression · Week 10 Monday

Same houses as today's slides: 2,925 home sales in Ames, Iowa, 2006–2010. Your professor will tell you when to do each part.

## 1 · Draw the line

![](plot:scatter){width=100%}

1. With a ruler, draw the straight line that best follows the 2,193 training houses.
2. Your line's price for a 2,000 sq ft house: $ ________
3. Your line's slope: about $ ________ per square foot.

## 2 · Five test houses

The computer's line: price = $9,194 + $114.97 × living area. Prices in **thousands of dollars**.

| house | living area | actual | predicted | residual (actual − predicted) | residual² |
|:--|--:|--:|--:|:-:|:-:|
| Somerset | 1,861 | 257 | 223 | ______ | ______ |
| Brookside | 2,068 | 210 | 247 | ______ | ______ |
| Northridge Heights | 1,358 | 224 | 165 | ______ | ______ |
| North Ames | 1,142 | 114 | 140 | ______ | ______ |
| Northridge | 2,202 | 263 | 262 | ______ | ______ |

1. **MAE** = mean of the |residuals| = ______ thousand dollars
2. **RMSE** = √(mean of the residuals²) = ______ thousand dollars
3. Why is the RMSE bigger than the MAE? ______________________________

\newpage

## 3 · Same size, one more bedroom

| model | coefficient of `bedrooms` |
|:--|--:|
| price ~ bedrooms | +$14,077 per bedroom |
| price ~ living area + bedrooms | −$31,152 per bedroom |

How can the same column add $14,077 in one model and take away $31,152 in the other?

______________________________________________________________

______________________________________________________________

## 4 · Over or under?

![](plot:overunder){width=100%}

Average percentage error for the test houses, from the cheapest fifth to the priciest fifth. Above 0 = the model values the house **higher** than it sold for.

1. **Circle** the group the one-line model overvalues most, and the group it undervalues.
2. If these values set property taxes, who would pay too much? ______________________
