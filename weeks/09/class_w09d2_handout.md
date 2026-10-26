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

**Talk with your neighbor:** 3rd class lost the most ages, and in every class the passengers with no age survived less often. What story could explain **both** patterns?

## 2 · Name the mechanism

**MCAR**: pure chance. **MAR**: explained by columns we *can* see. **MNAR**: depends on the missing value itself, or on something never recorded.

Write MCAR, MAR or MNAR in each blank.

1. ________ A lab freezer breaks overnight and spoils a random rack of blood samples.
2. ________ To keep an online survey short, a randomly chosen half of the people never see the income question.
3. ________ Two *Titanic* passengers have no port: a clerk smudged their line in the register.
4. ________ A weather station's thermometer stops working below −30 °C.
5. ________ In a salary survey, the people with the highest salaries skip the salary question.
6. ________ A fitness watch records no steps on the days its owner leaves it at home: mostly lazy days.
7. ________ A clinic measures cholesterol only for patients over 40. Every patient's age is in the data.
8. ________ Men skip the "hours of sleep" question more often than women, however much they sleep. Sex is in the data.
9. ________ Cabin is blank for 98% of *Titanic* 3rd class: their tickets rarely listed one.
10. ________ Students who were failing a course dropped it, so their final grade is blank. Their midterm grades are in the data.
11. ________ The real missing *Titanic* ages from Part 1.

**Talk with your neighbor:** compare answers, then defend 10 and 11. For 10: what if the midterm column were missing? For 11: could the data ever settle it?

## 3 · The spike

![](plot:spike){width=100%}

The 981 training passengers' ages: as recorded (top), and after filling every blank with the mean age (bottom).

1. **Circle** what the imputer added.
2. **Talk with your neighbor:** median age is 39 in 1st class and 24 in 3rd. Whose blanks does one mean of 30 fit worse? What would you fill them with instead?

## 4 · Pick the fix

| | fix | what it assumes about the blank rows |
|:-:|---|---|
| **A** | drop the rows with blanks | they are like everyone else |
| **B** | fill with one mean or median | they are like everyone else |
| **C** | fill from similar rows | other columns explain who is blank |
| **D** | C, plus a missing-indicator column | the blank itself says something |

Write the best letter for each situation from Part 2.

1. ________ The freezer spoiled a random rack of blood samples (#1).
2. ________ Men skip the sleep question; sex is in the data (#8).
3. ________ Failing students dropped the course; their midterms are in the data (#10).
4. ________ The highest earners skip the salary question (#5).
5. ________ The real missing *Titanic* ages (#11).

**Talk with your neighbor:** for the salaries, does any letter bring the missing salaries back? What else could you do?
