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
random_state=1); the standard deviations 14.5 and 50.2 are the training set's. Change them
together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Scaling, Encoding and Pipelines · Week 9 Monday

Same passengers as today's slides: the 1,043 *Titanic* passengers with age, fare and port recorded. Your professor will tell you when to do each part.

## 1 · Who is closest?

![](plot:closest){width=100%}

| passenger | class | age | fare |
|:--|:-:|--:|--:|
| A — Colley, Mr. Edward | 1st | 47 | £25.59 |
| B — Davies, Mr. John | 3rd | 21 | £24.15 |
| C — Chaffee, Mr. Herbert | 1st | 46 | £61.18 |

1. **In years and pounds** (left plot): draw the lines A–B and A–C. Closer to A: ________
2. **In standard deviations** (age ÷ 14.5, fare ÷ 50.2): A–B differ by ______ in age and ______ in fare; A–C by ______ and ______. Closer to A: ________

## 2 · Encode four passengers

The three port columns are `embarked_Cherbourg`, `embarked_Queenstown` and `embarked_Southampton`.

| sex | embarked | sex_male | Cherbourg | Queenstown | Southampton |
|:--|:--|:-:|:-:|:-:|:-:|
| male | Southampton | ____ | ____ | ____ | ____ |
| female | Cherbourg | ____ | ____ | ____ | ____ |
| male | Queenstown | ____ | ____ | ____ | ____ |
| female | Southampton | ____ | ____ | ____ | ____ |

Why is there no `sex_female` column? ______________________________

\newpage

## 3 · Follow the pipe

![](plot:pipe){width=100%}

1. In each branch, write the columns that go in.
2. How many columns come out of `prep` and into kNN? ______

## 4 · Choose k

![](plot:kcurve){width=56%}

1. Accuracy of the whole pipeline for each k: on the folds it learned from, and on the held-out fold.
2. **Circle** the best k.
3. **Label** the overfitting side and the underfitting side.
4. k = 1: learned-from folds ______ %, held-out fold ______ %.
