<!--
Source for class_w05d1_handout.pdf, the printed activities for class_w05d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w05d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part; its plot goes on the left, its text on the right
  - ![](plot:NAME)     which plot the part shows: unlabeled, start, clusters or elbow
                       (drawn by the script from datasets/listeners.csv, same data as the slides)
                       optional width, e.g. ![](plot:clusters){width=42%}  (default 46%)
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 4$, **bold**, *italic*, numbered lists: normal markdown
This comment block is not printed.
-->

# DATA 202 — Clustering · Week 5 Monday

Draw right on the plots. Every plot shows the **same 180 listeners** as today's slides (one dot per listener). Your professor will tell you when to do each part.

## 1 · How many groups?

![](plot:unlabeled)

1. **Circle** every group of listeners you see.
2. How many groups did you circle? ____
3. Compare with a neighbor: where do your circles **disagree**?

## 2 · k-means by hand: one round

![](plot:start)

1. The four X's (**A**–**D**) are the **starting centroids**: listeners 38, 71, 129 and 158.
2. **Assign.** Draw lines that split the plot so every listener goes with its **nearest** X. *Tip: a boundary runs halfway between two X's.*
3. **Update.** In each of your groups, draw a **new X** at the middle of its points.
4. Compare with the *Round 1* panels on screen. Which X moved the most? Which listeners changed group?

\newpage

## 3 · Name the groups

![](plot:clusters)

1. This is where k-means ($k = 4$) ended up. The cluster numbers mean nothing.
2. Next to each group, write a **short name** for the kind of listener it holds.
3. Put a $\star$ next to one listener who could belong to **two** groups.
4. Compare names with a neighbor. Same names? Why did you choose yours?

## 4 · How many groups?

![](plot:elbow)

1. This is the inertia for $k = 1$ to $10$. **Circle the elbow.**
2. From the screen: elbow says $k =$ ____ and silhouette says $k =$ ____.
3. I'd choose $k =$ ____ because

   ____________
