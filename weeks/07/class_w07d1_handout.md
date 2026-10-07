<!--
Source for class_w07d1_handout.pdf, the printed activities for class_w07d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w07d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: onecut, tree2, maps or depth
                       (drawn by the script from datasets/autism.csv, same data and split as the slides)
                       optional width, e.g. ![](plot:tree2){width=48%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
The three children in part 2 are test children 49, 84 and 40 from the notebook's split
(random_state=7); change them together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Decision Trees · Week 7 Monday

Same children as today's slides: the 111 training children, ASD (triangles) and NEU (circles). Your professor will tell you when to do each part.

## 1 · One line

![](plot:onecut){width=100%}

1. Draw **one** straight line, either **vertical** or **horizontal**, that best separates ASD from NEU.
2. Count the children on the wrong side of your line: ______

## 2 · Follow the tree

![](plot:tree2){width=100%}

In each box, value = [ASD, NEU]. Send each test child down the tree. Start at the top; *True* goes left.

| child | fGSH | GSSG | tree predicts | true group | right? |
|:--|--:|--:|:-:|:-:|:-:|
| 1 | 1.931 | 0.209 | ________ | ASD | ____ |
| 2 | 2.537 | 0.288 | ________ | NEU | ____ |
| 3 | 1.318 | 0.105 | ________ | ASD | ____ |

\newpage

## 3 · Three maps

![](plot:maps){width=100%}

1. The background shows what each tree predicts at every spot.
2. In the "no limit" map, **circle** a rectangle that exists for a single child.
3. Under each map, write *too simple*, *about right* or *too wiggly*.

## 4 · Which depth?

![](plot:depth){width=56%}

1. Each tree's accuracy on the training children and on the test children.
2. **Circle** the best depth for the test children.
3. **Label** the underfitting zone and the overfitting zone.
4. With no limit (depth 7): training ____ %, test ____ %.
