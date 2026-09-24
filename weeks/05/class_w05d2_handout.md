<!--
Source for class_w05d2_handout.pdf, the printed activities for class_w05d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w05d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: clusters, views or cumulative
                       (drawn by the script from the same digits as the slides)
                       optional width, e.g. ![](plot:views){width=100%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 4$, **bold**, *italic*, numbered lists, | tables |: normal markdown
                       (keep table rows under 72 characters, or pandoc stretches the table to full width)
This comment block is not printed.
-->

# DATA 202 — PCA · Week 5 Wednesday

Draw right on the plots. They show the same data as today's slides: 1,797 handwritten digits (8×8 pixels = **64 numbers** each). Your professor will tell you when to do each part.

## 1 · What's in each cluster?

![](plot:clusters){width=52%}

1. k-means split the digits into 10 clusters. Each row: the cluster's **average image**, then 8 of its members.
2. In the empty box, write the **digit** each row mostly holds.
3. **Circle** every image that doesn't belong in its row.
4. Which clusters are the most mixed?

## 2 · One ruler for every column

Pixel 42 of the first image, measured two ways: the usual darkness scale (0–16), and a scanner that stores that pixel ×100 (0–1,600). Compute its z-score in both units: **z = (value − column mean) ÷ column standard deviation**.

| | 0–16 scale | 0–1,600 scale |
|:--|--:|--:|
| column mean | 6.9 | 690 |
| column standard deviation | 6.5 | 650 |
| pixel 42, first image | 11 | 1,100 |
| **z-score** | ____ | ____ |

What do you notice?

\newpage

## 3 · Two views of the same digits

![](plot:views){width=100%}

1. Each character is one image (300 of the 1,797), drawn as its **true digit**.
2. **Circle the 0s** in both views. In which view do they form one group?
3. In the PCA view, name two digits that still **overlap**: ____ and ____

## 4 · How many components?

![](plot:cumulative)

1. The share of the variance kept by the first $n$ of the 64 components.
2. Mark where the curve reaches **80%**: ____ components.
3. Mark where it reaches **90%**: ____ components.
