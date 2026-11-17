<!--
Source for class_w14d2_handout.pdf, the printed activities for class_w14d2.ipynb.
Rebuild the PDF after editing:   python scripts/make_w14d2_handout.py   (about 30 seconds)

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: importance, ice, grids (Part 4 has no plot)
                       (drawn by the script from datasets/mortgages.csv, same forest, split and applicants as the slides)
                       optional width, e.g. ![](plot:ice){width=56%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
  - a table with 4+ dashes in a column of its |---| row (Part 4's) spans the page in small type;
    its columns are as wide as their dashes
  - symbols like ≤ ≈ vanish in the PDF's font: write them out in words
Applicants A and B are test rows 3389 and 17464 of datasets/mortgages.csv (APPLICANTS in the script).
Answers. Part 1: income (impurity 0.12, permutation 0.0001). Part 2: cliffs at 50% and 60%; odd lines: three start
high, one VA purchase stays low. Part 3: A approved at any DTI of 49 or less; B approved at LTV 90 or less (at its
own DTI). Part 4: 1 E, 2 A, 3 B, 4 C, 5 D, 6 F.
This comment block is not printed.
-->

# DATA 202 — Interpretability · Week 14 Wednesday

A random forest learned from Kent County's 2025 mortgage decisions: 90.5% right on the test set, against 88.2% for Week 11's line. Can it say why it denies someone? Your professor will tell you when to do each part.

## 1 · Two importances

![](plot:importance){width=100%}

**Impurity:** how much each column's splits cleaned up the leaves while the forest learned, on the training data. **Permutation:** how much accuracy the forest loses on the test set when one column is shuffled.

1. **Circle** the column the two disagree about most.
2. **Pair talk:** the forest split on that column a lot, yet shuffling it costs almost nothing on new applicants. What was the forest doing with it?

## 2 · One line per applicant

![](plot:ice){width=58%}

100 test applicants. Each gray line: one applicant's chance of denial, with their debt-to-income set to each value and everything else kept. Blue: the average of the lines.

1. **Label** the cliffs on the average.
2. **Circle** a line that doesn't follow the average.
3. **Pair talk:** the average says 50–60% means a chance of about one half. Whose chance is that?

\newpage

## 3 · Around A and B

![](plot:grids){width=100%}

Both were denied. **A** is buying a home, with a debt-to-income of 50–60% and 90% of the price borrowed. The lender's reason: *debt-to-income*. **B** wants a home-improvement loan, with a debt-to-income of 30–36%; the loans would add up to 101% of the home's value. The lender's reason: *collateral*. Each cell: the forest's chance of denial if only those two columns changed.

1. **Shade** every cell where the forest denies (0.5 or more).
2. **Circle** each applicant's own cell, and **draw** an arrow to the nearest cell where the forest approves.
3. **Pair talk:** the lender must tell each applicant why. What would you write to A, and to B? Can they act on it?

## 4 · Pick the method

| | method | the question it answers | global or local | when to use it |
|:-:|------|----------|------|----------|
| **A** | permutation importance | which columns does the model rely on? | global | on held-out data; prefer it to impurity importance |
| **B** | partial dependence, with ICE lines | how does the prediction change with one column? | global, with a line per person | the shape of an effect; the lines show who differs from the average |
| **C** | global surrogate | which simple rules imitate the model? | global | a readable summary; report how often it agrees |
| **D** | LIME or SHAP | which columns pushed this one prediction? | local | explaining one decision of any model; check it's stable |
| **E** | counterfactual | what is the smallest change that flips the decision? | local | a reason a person can act on |
| **F** | a readable model | slopes or a small tree explain themselves | both | when it's nearly as accurate as the black box |

Write the letter that fits best.

1. ____ A bank must tell a denied applicant what they could change to be approved.
2. ____ A hospital wants to know which of 40 lab results its model relies on most, for new patients.
3. ____ A city wants to see how its predicted bus delays change with the temperature.
4. ____ Auditors want one page of rules that behaves like a 500-tree model.
5. ____ A doctor asks why the model flagged this one patient.
6. ____ A parole board's black box is only one point more accurate than a logistic regression.

**Pair talk:** an explanation says "loan-to-value". Could it hide a proxy, like Monday's neighborhood? How would you check?
