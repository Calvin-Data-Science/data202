<!--
Source for class_w06d2_handout.pdf, the printed activities for class_w06d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w06d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 1's scores come from the notebook's five-split loop (k = 5). The numbers in parts 2
and 3 come from the notebook's split (random_state=24, k = 5);
change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Testing a Model · Week 6 Wednesday

Same penguins as today's slides: 342 penguins, split at random into 239 for training and 103 for testing. Your professor will tell you when to do each part.

## 1 · Five splits, five scores

Same model ($k = 5$), same penguins; only `random_state` changes.

| split | random_state | test accuracy |
|:--|--:|--:|
| **ours** | 24 | 95.1% |
| another | 15 | 92.2% |
| another | 1 | 93.2% |
| another | 7 | 97.1% |
| another | 19 | 100.0% |

1. Lowest score: ____ %

   Highest score: ____ %

2. **Circle** the split you'd be tempted to report.

## 2 · Build the confusion matrix

Our split, $k = 5$. The model got **46** Adelies, **18** Chinstraps and **34** Gentoos right. Its 5 mistakes:

| bill length (mm) | bill depth (mm) | true species | predicted |
|--:|--:|:--|:--|
| 44.4 | 17.3 | Gentoo | Chinstrap |
| 45.8 | 18.9 | Adelie | Chinstrap |
| 48.1 | 16.4 | Chinstrap | Gentoo |
| 40.9 | 16.6 | Chinstrap | Adelie |
| 42.9 | 17.6 | Adelie | Chinstrap |

1. Fill in all nine cells. Rows = **true** species, columns = **predicted**.

| | **Adelie** | **Chinstrap** | **Gentoo** |
|:--|:-:|:-:|:-:|
| **Adelie** | ______ | ______ | ______ |
| **Chinstrap** | ______ | ______ | ______ |
| **Gentoo** | ______ | ______ | ______ |

2. Accuracy = right ÷ all = ______ ÷ 103 = ______

## 3 · Finding the Chinstraps

1. In your matrix, **circle** the Chinstrap row and **box** the Chinstrap column.
2. **Recall** — of the real Chinstraps, how many did we find?

   recall = ______ ÷ ______ = ______

3. **Precision** — of the penguins we called Chinstrap, how many really are?

   precision = ______ ÷ ______ = ______

4. A lazy model answers *not Chinstrap* for every penguin. On "Chinstrap or not?":

   accuracy = ______ ÷ 103 = ______  ·  recall = ______

5. In your matrix, write **FP** in each false-positive cell and **FN** in each false-negative cell for Chinstrap.
