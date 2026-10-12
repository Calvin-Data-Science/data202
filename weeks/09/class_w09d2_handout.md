<!--
Source for class_w09d2_handout.pdf, the printed activities for class_w09d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w09d2_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: noage or spike
                       (drawn by the script from datasets/titanic.csv, same passengers and split as the slides)
                       optional width, e.g. ![](plot:noage){width=46%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Part 1's survival table is the notebook's pivot table (all 1,309 passengers). Change it
together with the notebook.
This comment block is not printed.
-->

# DATA 202 — Missing Data · Week 9 Wednesday

Same passengers as Monday, but all 1,309 of them: 263 have no recorded age. Your professor will tell you when to do each part.

## 1 · Who lost their age?

![](plot:noage){width=46%}

Share who survived:

| class | age recorded | no age |
|:-:|:-:|:-:|
| 1st | 64% | 49% |
| 2nd | 44% | 25% |
| 3rd | 26% | 24% |

1. Which class lost the most ages? ________
2. Inside each class, who survived more often: passengers with an age, or without? ________
3. With a neighbor: one story that could explain **both** patterns:

______________________________________________________________

## 2 · Name the mechanism

**MCAR**: pure chance. **MAR**: explained by columns we *can* see. **MNAR**: depends on the missing value itself, or on something never recorded.

For each blank, write MCAR, MAR or MNAR, and why.

1. Two passengers have no port: a clerk smudged their line in the register.

   ______________________________________________________________

2. Age is blank for 29% of 3rd class but 6% of 2nd class; within a class, which ages are blank is luck.

   ______________________________________________________________

3. *(Suppose)* older passengers left their age blank on purpose.

   ______________________________________________________________

4. Cabin is blank for 98% of 3rd class: their tickets rarely listed one.

   ______________________________________________________________

\newpage

## 3 · The spike

![](plot:spike){width=100%}

The 981 training passengers' ages: as recorded (top), and after filling every blank with the mean age (bottom).

1. **Circle** what the imputer added.
2. How many passengers are now exactly 30.0 years old? ______
3. Standard deviation of age: before ______ years, after ______ years.
4. Median age is 39 in 1st class and 24 in 3rd. Who gets a worse guess from the mean: a missing 1st-class age or a missing 3rd-class age? Why? ______________________
