<!--
Source for class_w14d1_handout.pdf, the printed activities for class_w14d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w14d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: strips (Parts 2 and 3 have no plot)
                       (drawn by the script from datasets/mortgages.csv, same model, split and applicants as the slides)
                       optional width, e.g. ![](plot:strips){width=90%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
  - a table with 4+ dashes in a column of its |---| row (Part 3's) spans the page in small type;
    its columns are as wide as their dashes
  - symbols like ▲ ○ ≤ ≈ vanish in the PDF's font: write them out in words
The 24 applicants are TEST applications (WHITE12, BLACK12 in scripts/make_w14d1_handout.py), as in the notebook.
Answers. Part 1, at 0.2: White 3 of 12, wrongly denied 2 of 10, missed 1 of 2; Black 5 of 12, 3 of 8, 2 of 4.
Part 2: the line at about 0.30; Black: wrongly denied 1 of 8, missed 2 of 4. Part 3: 1 A, 2 E, 3 F, 4 C, 5 B (D has no situation).
This comment block is not printed.
-->

# DATA 202 — Fairness · Week 14 Monday

Week 11's model, on its locked test set: mortgage applications in Kent County, Michigan, decided in 2025. The model never sees race. It denies an application when its chance of denial is 0.2 or more. Your professor will tell you when to do each part.

## 1 · Same threshold, two groups

![](plot:strips){width=100%}

Twelve test applicants from each group, placed by the model's chance of denial. Orange triangles: the lender denied. Circles: the lender approved.

1. **Draw** the threshold, a vertical line at 0.2, across both strips. The model denies everyone to its right.
2. **Count** for each group.

| | White | Black |
|:--|:-:|:-:|
| the model denies | ____ of 12 | ____ of 12 |
| **wrongly denied:** of those the lender approved (circles), the model denies | ____ of 10 | ____ of 8 |
| **missed:** of those the lender denied (triangles), the model approves | ____ of 2 | ____ of 4 |

3. **Pair talk:** which row would a Black applicant point to? Which row would the lender point to?

## 2 · Move one line

1. On the **Black** strip, **draw** a second line so the model denies 3 of 12 Black applicants, as many as White applicants.
2. **Count** again, for Black applicants: wrongly denied ____ of 8; missed ____ of 4.
3. **Pair talk:** now both groups are denied equally often. What got better, and for whom? What got worse?

\newpage

## 3 · Pick the criterion

| | criterion | what is equal across groups | the harm it guards against | when to use it |
|:-:|------|---------|---------|---------|
| **A** | unawareness | the inputs: no protected column | deciding *by* race, sex or age | required in lending; then test for proxies |
| **B** | demographic parity | the share chosen (or denied) | outcomes that depend on the group | the broad view; a label you can't trust |
| **C** | equal opportunity | the share of qualified people turned away | the qualified losing out in one group | the middle view; when turning people away is the harm |
| **D** | equalized odds | both mistakes: wrongly denied and missed | either side carrying more risk in one group | when both mistakes matter; costs the most accuracy |
| **E** | calibration, predictive parity | what a score or a flag means | a "30%" that means different things in different groups | the narrow view; scores that people read |
| **F** | question the label | the answer key itself | a model that copies an unfair past | before modeling, when the label is a past human decision |

**Always:** audit every measure by group, on the test set. When the groups' base rates differ, B to E can't all hold at once. **Fixes:** before training (a better label, more data on small groups, test for proxies), while training (reweigh rows, add a fairness constraint), or after (a threshold per group, which is illegal by race in lending).

Write the letter that fits best.

1. ____ A state law says a parole model may not use a person's race or ZIP code.
2. ____ Doctors read a risk score of 30% as a 30% chance, so it must mean that for every group of patients.
3. ____ A hiring model learns from ten years of a firm's hiring, by managers who rarely hired women.
4. ____ A résumé screen turns away qualified older applicants more often than qualified younger ones.
5. ____ A city's housing lottery wants the share of winners from each neighborhood to match the share of applicants.

**Pair talk:** in 2016, reporters found that a pretrial risk tool had flagged Black defendants who were never re-arrested as high-risk about twice as often as white ones (45% against 23%). Its maker answered that each score meant the same chance of re-arrest in both groups. Who was right? Could the tool have had both?
