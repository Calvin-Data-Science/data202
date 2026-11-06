<!--
Source for class_w11d2_handout.pdf, the printed activities for class_w11d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w11d2_handout.py   (about 30 seconds)

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: treeforest, adaboost
                       (drawn by the script from datasets/pumpkin.csv, same seeds and split as the slides;
                       adaboost = the notebook's 20 seeds, X_train.sample(20, random_state=73))
                       optional width, e.g. ![](plot:treeforest){width=56%}; under 80% the plot
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

Pumpkin seeds of two varieties, measured from photos. Ç = Çerçevelik, Ü = Ürgüp Sivrisi. Your professor will tell you when to do each part.

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

## 3 · AdaBoost by hand

![](plot:adaboost){width=100%}

Twenty training seeds, two columns. **Left:** stump 1 asks one question, "aspect ratio $\le$ 2.12?": left of the line it says Ç, right of it Ü. **Right:** the same seeds after reweighting, each drawn by its new weight.

1. **Left: circle** the seeds stump 1 gets wrong.
2. **Right: draw** the single cut (one vertical or one horizontal line) that stump 2 should make.
3. **Pair talk:** each stump alone misses several seeds, yet the weighted vote of three stumps gets all 20 right. How?
