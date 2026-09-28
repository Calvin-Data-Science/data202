<!--
Source for class_w06d1_handout.pdf, the printed activities for class_w06d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w06d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: mystery, zoom, maps or accuracy
                       (drawn by the script from datasets/penguins.csv, same data as the slides)
                       optional width, e.g. ![](plot:zoom){width=48%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
This comment block is not printed.
-->

# DATA 202 — k-Nearest Neighbors · Week 6 Monday

Draw right on the plots. They show the same penguins as today's slides: the 223 measured in 2007–2008 (circles = Adelie, triangles = Chinstrap, squares = Gentoo) and three new ones from 2009 ($\star$). Your professor will tell you when to do each part.

## 1 · Which species?

![](plot:mystery){width=100%}

Your guess:   **A** ________   **B** ________   **C** ________

## 2 · Ask the neighbors

![](plot:zoom){width=40%}

1. Zoomed in on **B**. One grid square is 1 mm × 1 mm, so distances are true.
2. **Circle** B's nearest neighbor. With $k = 1$, B is a ________.
3. Draw **one circle** around B's 5 nearest neighbors. Votes:

   Adelie ____  Chinstrap ____  Gentoo ____

4. With $k = 5$, B is a ________.

\newpage

## 3 · Three maps

![](plot:maps){width=100%}

1. The background shows what kNN predicts at every spot.
2. **Circle** one "island" in the $k = 1$ map.
3. At $k = 100$, **circle** what is left of the Chinstrap region.
4. Under each map, write *too wiggly*, *about right* or *too simple*.

## 4 · Which k?

![](plot:accuracy){width=56%}

1. kNN's accuracy for every $k$: on the penguins it learned from, and on the new ones.
2. **Circle** the best $k$ for the new penguins.
3. **Label** the overfitting zone and the underfitting zone.
4. At $k = 1$: known ____ %, new ____ %.
