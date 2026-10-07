<!--
Source for class_w07d2_handout.pdf, the printed activities for class_w07d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w07d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: folds or cvcurve
                       (drawn by the script from datasets/autism.csv, same data and split as the slides)
                       optional width, e.g. ![](plot:cvcurve){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 1's table comes from the notebook's five-split loop; part 4's from its grid search
(both on fGSH and GSSG). Change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Cross-Validation and Grid Search · Week 7 Wednesday

Same children as today's slides: ASD vs. NEU by two blood measurements, 111 training children and 48 test children. Your professor will tell you when to do each part.

## 1 · Five splits

Test accuracy of a tree at each `max_depth`, for five different random splits.

| random_state | depth 1 | depth 2 | depth 3 | depth 4 | depth 5 |
|:--|--:|--:|--:|--:|--:|
| 1 | 0.750 | 0.938 | 0.938 | 0.896 | 0.833 |
| 7 (Monday's) | 0.792 | 0.875 | 0.875 | 0.771 | 0.729 |
| 13 | 0.812 | 0.896 | 0.896 | 0.875 | 0.875 |
| 21 | 0.583 | 0.771 | 0.729 | 0.708 | 0.688 |
| 30 | 0.750 | 0.875 | 0.875 | 0.896 | 0.854 |

1. In each row, **circle** the best score.
2. Depth 2: lowest ________, highest ________.

## 2 · Five folds

![](plot:folds){width=100%}

1. The 111 training children are cut into 5 folds. In each round, **shade** the fold that gets scored.
2. Cross-validation score = mean of the 5 rounds = ________ ÷ 5 = ________

\newpage

## 3 · Pick the depth

![](plot:cvcurve){width=56%}

1. Mean accuracy over the 5 rounds, for each depth. The bars show how much the rounds disagreed.
2. **Circle** the best depth.
3. **Label** the underfitting side and the overfitting side.

## 4 · The grid

5-fold cross-validation accuracy for every combination of `max_depth` and `min_samples_leaf`.

| min_samples_leaf | depth 1 | depth 2 | depth 3 | depth 4 | depth 5 | depth 6 | no limit |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 1 | 0.702 | 0.847 | 0.838 | 0.829 | 0.820 | 0.829 | 0.784 |
| 2 | 0.702 | 0.847 | 0.828 | 0.820 | 0.829 | 0.829 | 0.829 |
| 5 | 0.702 | 0.847 | 0.856 | 0.847 | 0.847 | 0.856 | 0.856 |
| 10 | 0.702 | 0.828 | 0.828 | 0.828 | 0.828 | 0.828 | 0.828 |
| 20 | 0.702 | 0.774 | 0.774 | 0.774 | 0.774 | 0.774 | 0.774 |

1. **Circle** the best score.
2. **Box** every cell within 0.01 of the best. (One child out of 111 is about 0.009.)
3. Trees fitted: ______ combinations × ______ folds = ______
4. Which boxed cell would you choose, and why?
