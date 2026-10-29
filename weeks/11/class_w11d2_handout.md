<!--
Source for class_w11d2_handout.pdf, the printed activities for class_w11d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w11d2_handout.py   (about 1 minute)

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: treeforest, moretrees
                       (drawn by the script from datasets/pumpkin.csv, same seeds and split as the slides)
                       optional width, e.g. ![](plot:moretrees){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 1's votes are typed in from the notebook's output: RandomForestClassifier(n_estimators=5,
random_state=1) on the 1,875 training seeds; seeds A-F are test rows 2368, 1276, 297, 679, 1561, 655.
Change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Ensembles · Week 11 Wednesday

Same pumpkin seeds as Monday. Ç = Çerçevelik, Ü = Ürgüp Sivrisi. Your professor will tell you when to do each part.

## 1 · Five trees vote

A random forest of five deep trees, each grown on its own bootstrap sample of the training seeds. Their votes on six new seeds:

| seed | tree 1 | tree 2 | tree 3 | tree 4 | tree 5 | forest | actual | right? |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | Ü | Ü | Ü | Ü | Ü | ______ | Ü | ______ |
| B | Ü | Ç | Ç | Ç | Ç | ______ | Ç | ______ |
| C | Ç | Ç | Ç | Ü | Ü | ______ | Ç | ______ |
| D | Ç | Ç | Ü | Ç | Ç | ______ | Ç | ______ |
| E | Ü | Ç | Ü | Ü | Ç | ______ | Ü | ______ |
| F | Ü | Ü | Ü | Ü | Ü | ______ | Ç | ______ |

1. **Fill in** the forest's answer (the majority vote), then mark it right or wrong.
2. **Circle** every wrong vote of a single tree. Is there a tree with no circles? ________
3. **Pair talk:** which single tree would you trust alone? Would 100 more trees fix seed F?

## 2 · Tree vs. forest

![](plot:treeforest){width=58%}

Five-fold cross-validation on the training seeds, as the trees grow deeper.

1. **Label** the side where the single tree overfits.
2. **Pair talk:** both reach 100% on the seeds they learned from. Why doesn't the forest's held-out accuracy fall?

\newpage

## 3 · More trees

![](plot:moretrees){width=58%}

Five-fold cross-validation on the training seeds, as we add trees. Boosting: small trees in a row, each learning from the mistakes left by the ones before it.

1. **Circle** where boosting starts to overfit.
2. **Pair talk:** why can more trees hurt boosting but not the forest?
