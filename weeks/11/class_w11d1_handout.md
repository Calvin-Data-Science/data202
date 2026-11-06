<!--
Source for class_w11d1_handout.pdf, the printed activities for class_w11d1.ipynb.
Rebuild the PDF after editing:   python scripts/make_w11d1_handout.py

How this file becomes the PDF:
  - "# ..."            the title line at the top of page 1
  - "## ..."           one handout part
  - ![](plot:NAME)     the part's plot: logistic, curves (drawn by the script).
                       A part has ONE plot, so Part 1's second plot is its own part (1b).
                       optional width, e.g. ![](plot:logistic){width=50%}; under 80% the plot
                       sits left and the text right, 80% or more it spans the page, text below
  - ____               4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  - \newpage           start a new page
  - $k = 5$, **bold**, *italic*, numbered lists, | tables |: normal markdown
Curves 1-4 in "curves" are, in order: z = -6 + 0.2 DTI, -25 + 0.5 DTI, 10 - 0.2 DTI, -10 + 0.2 DTI
(answers: a -> 4, b -> 2, c -> 1, d -> 3). Change them together with the notebook's form cell.
Part 3's ten applications are real training rows (index 15085, 3357, 15992, 956, 3746, 13129, 2383, 14253, 6724,
1311) with their 5-fold cross-validated P(denied) from the all-columns model, as shown in the notebook.
Answers: 50% -> TP 2, FP 1, FN 2, TN 5, precision 0.67, recall 0.50; 20% -> TP 3, FP 3, FN 1, TN 3, 0.50, 0.75.
This comment block is not printed.
-->

# DATA 202 — Logistic Regression · Week 11 Monday

How can a linear model classify? Applications to borrow against a home in Kent County, Michigan, decided in 2025: approved or denied. DTI = debt-to-income, the share of monthly income that would go to debt payments (%). Your professor will tell you when to do each part.

## 1a · From a score to a probability

![](plot:logistic){width=50%}

Step 1, the score: $z = -10 + 0.2 \times \text{DTI}$. Step 2, the probability: $p = 1 / (1 + e^{-z})$, the curve.

1. **Compute** each applicant's score.\
   A, DTI 30%: $z$ = ______\
   B, DTI 50%: $z$ = **0**\
   C, DTI 70%: $z$ = ______
2. **Mark** A, B and C on the curve.
3. Raise each score by 1. **Draw** an arrow along the curve for each applicant. Whose probability moves the most? ________
4. **Pair talk:** whose decision can a small change in the data flip: a clear case or a borderline one? Why might that matter to an applicant?

## 1b · Four S-curves

![](plot:curves){width=100%}

Four curves for the chance of denial. **Match** each score to its curve. (*Hint:* a curve crosses 50% where its score is 0.)

| score | curve | score | curve |
|:--|:--:|:--|:--:|
| (a) $z = -10 + 0.2 \times \text{DTI}$ | ______ | (b) $z = -25 + 0.5 \times \text{DTI}$ | ______ |
| (c) $z = -6 + 0.2 \times \text{DTI}$ | ______ | (d) $z = 10 - 0.2 \times \text{DTI}$ | ______ |

5. **Pair talk:** many lenders won't approve a DTI above 50%. Which curve looks most like that rule? What would a curve with an even bigger slope look like?

\newpage

## 2 · Many columns, one score

The model now uses DTI, loan-to-value, the loan amount, and the loan's purpose, lien and type. Before the slopes appear on screen, write **+** if you think the column raises the chance of denial, **−** if it lowers it.

| column | your guess | the model |
|:--|:--:|:--:|
| debt-to-income | ______ | ______ |
| loan amount | ______ | ______ |
| a home purchase (vs. a cash-out refinance) | ______ | ______ |
| a second lien (vs. a first mortgage) | ______ | ______ |
| a conventional loan (vs. an FHA loan) | ______ | ______ |

A **cash-out refinance** replaces a mortgage with a bigger one and pays the difference in cash. A **second lien** is a second loan on a home that already has a mortgage. An **FHA loan** is insured by the government, for borrowers with smaller down payments or lower credit scores.

**Pair talk:** the lender saw each applicant's credit score, but this file doesn't have it. Which of these columns might be standing in for it?

## 3 · Choose the threshold

Ten training applications: the model's chance of denial, and what the lender decided (D = denied, A = approved).

| application | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| chance of denial | 0.84 | 0.62 | 0.55 | 0.41 | 0.33 | 0.27 | 0.18 | 0.12 | 0.08 | 0.03 |
| lender's decision | D | D | A | D | A | A | D | A | A | A |

The model **flags** an application as *denied* when its chance is at or above the threshold. A positive is a denied application. **Precision** = TP ÷ (TP + FP); **recall** = TP ÷ (TP + FN).

1. **Fill in** the table, first for a threshold of 50%, then for 20%.

| threshold | TP | FP | FN | TN | precision | recall |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 50% | ____ | ____ | ____ | ____ | ______ | ______ |
| 20% | ____ | ____ | ____ | ____ | ______ | ______ |

2. **Pair talk:** a false positive turns away someone the lender would have approved; a false negative approves someone it would have denied. Which threshold would you choose, and who pays for each kind of mistake?
