<!--
Source for class_w11d1_handout.pdf, the printed activities for class_w11d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w11d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: scurve, lengthwidth, ccurve
                       (drawn by the script from datasets/pumpkin.csv, same seeds and split as the slides)
                       optional width, e.g. ![](plot:ccurve){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
This comment block is not printed.
-->

# DATA 202 — Logistic Regression · Week 11 Monday

Pumpkin seeds of two varieties, Çerçevelik and Ürgüp Sivrisi, measured from photos. Your professor will tell you when to do each part.

## 1 · The S-curve

![](plot:scurve){width=56%}

Each dot is a training seed: Ürgüp Sivrisi on top, Çerçevelik at the bottom. The curve is the model's probability that a seed is Ürgüp Sivrisi.

1. **Mark** the 50/50 point on the curve.
2. **Shade** the aspect ratios where the model predicts Ürgüp Sivrisi.
3. Predicted variety of seed\
   A: ________________\
   B: ________________\
   C: ________________
4. **Circle** the seed the model is least sure about.

## 2 · Draw the boundary

![](plot:lengthwidth){width=60%}

Training seeds by length and width.

1. **Draw** the straight line you would use to separate the two varieties.
2. **Circle** a region where no straight line could get every seed right.
3. Your line says "long for its width." Which column of the data measures that? ______________

\newpage

## 3 · Choose C

![](plot:ccurve){width=56%}

Logistic regression on all 12 columns (scaled), 5-fold cross-validation on the training seeds.

1. **Circle** the best C.
2. **Label** the underfitting side.
3. Is there an overfitting side? ________ **Pair talk:** why not?
4. Here a *larger* C means a ____________ model. For Ridge, a *larger* alpha meant a ____________ model.
