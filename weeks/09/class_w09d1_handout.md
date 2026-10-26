<!--
Source for class_w09d1_handout.pdf, the printed activities for class_w09d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w09d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: closest, pipe or kcurve
                       (drawn by the script from datasets/titanic.csv, same passengers and split as the slides)
                       optional width, e.g. ![](plot:kcurve){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 1's passengers A, B, C and part 2's four passengers are the notebook's (training set,
random_state=1); the standard deviations 14.5 and 50.3 are the training set's. Change them
together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Scaling, Encoding and Pipelines · Week 9 Monday

Same passengers as today's slides: the 1,043 *Titanic* passengers with age, fare and port recorded. Your professor will tell you when to do each part.

## 1 · Who is closest?

![](plot:closest){width=90%}

| passenger | class | age | fare |
|:--|:-:|--:|--:|
| A — Colley, Mr. Edward | 1st | 47 | £25.59 |
| B — Davies, Mr. John | 3rd | 21 | £24.15 |
| C — Chaffee, Mr. Herbert | 1st | 46 | £61.18 |

1. On **both** plots, draw the lines A–B and A–C, and circle the passenger closer to A.
2. **Talk with your neighbor:** the two plots disagree. Using the table too, which answer would you trust to find a passenger like A, and why?

## 2 · One-hot encode four passengers

**One-hot:** one 0/1 column per category, with a 1 only in the row's own category.

| # | sex | embarked | sex_male | Cherbourg | Queenstown | Southampton |
|:-:|:--|:--|:-:|:-:|:-:|:-:|
| 1 | male | Southampton | ____ | ____ | ____ | ____ |
| 2 | female | Cherbourg | ____ | ____ | ____ | ____ |
| 3 | male | Queenstown | ____ | ____ | ____ | ____ |
| 4 | female | Southampton | ____ | ____ | ____ | ____ |

**Talk with your neighbor:** one-hot makes every port *equally far* from every other. Is that fair to Southampton, Cherbourg and Queenstown? What would you want to know about them?

\newpage

## 3 · Follow the pipe

![](plot:pipe){width=100%}

In each branch, write the columns that go in. In the right box, write how many columns come out into kNN.

## 4 · Choose k

![](plot:kcurve){width=56%}

Accuracy of the whole pipeline for each k, averaged over 5 folds of the training passengers: on the folds it trained on, and on the fold it was scored on (cross-validated). The test passengers were not used.

1. **Circle** the best k.
2. **Label** the overfitting side and the underfitting side.
