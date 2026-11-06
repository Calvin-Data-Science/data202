---
layout: week
title: "Week 10: Linear Regression"
week_number: 10
---

# Predicting a Number

## How Old Is This Abalone?

An **abalone** is a sea snail with a single ear-shaped shell, lined with iridescent mother-of-pearl. It is also a prized seafood, and fisheries need to know how old the abalone in a population are: how fast they grow, how long they live, and whether enough of them get old enough to breed.

The trouble is finding out. A biologist cuts the shell through its cone, stains it, and counts the **growth rings** under a microscope. The dataset's own documentation calls this "a boring and time-consuming task." Weighing and measuring an abalone takes a minute. So: **can a few quick measurements predict an abalone's age?**

Every reading since Reading 5 has predicted a **class**: heart disease or not, high income or not. Age is a **number**. Predicting a number is called **regression**, and the question changes from "right or wrong?" to "**how far off?**" Guessing 11 years for an abalone that is 12 isn't wrong the way "no" is wrong when the answer was "yes"; it's off by one year.

The data comes from a 1994 study of blacklip abalone along the north coast of Tasmania, Australia. Researchers measured, weighed and aged **4,177** of them.

**📥 Download the dataset: [abalone.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/abalone.csv)**

```python
import pandas as pd

abalone = pd.read_csv("abalone.csv")
abalone.shape          # (4177, 10): 4,177 abalone, 10 columns
```

| Column | What it holds |
|:---|:---|
| `sex` | male, female or infant (too young to tell) |
| `length_mm` | the longest shell measurement, in mm |
| `diameter_mm` | the width, across the length, in mm |
| `height_mm` | the height, with the meat in the shell, in mm |
| `whole_g` | the whole abalone, in grams |
| `meat_g` | the meat alone, in grams |
| `gut_g` | the gut, in grams |
| `shell_g` | the shell, dried, in grams |
| `rings` | rings counted under the microscope |
| `age_years` | the label: rings + 1.5, the age in years |

The last two columns say the same thing: the documentation says to add 1.5 to the ring count to get the age. We'll predict `age_years`.

## Look Before You Fit

> 🔁 **From Reading 7:** before choosing what to do with a column, look at its values, and at **whose** values look odd.

```python
abalone["height_mm"].describe()      # min 0.0, max 226.0
```

A typical abalone here is about 28 mm tall. Two have a height of **0 mm**, which is impossible for a snail with meat in its shell. Two more are **103 mm** and **226 mm** tall, on shells only 141 mm and 91 mm long: an abalone 226 mm tall would be more than twice as tall as it is long. These four rows are almost certainly typing mistakes. With only four out of 4,177, and a clear reason, we drop them:

```python
clean = abalone[(abalone["height_mm"] > 0) & (abalone["height_mm"] < 60)]     # 4,173 abalone
```

This is not a formality. At the end of page 5 we'll glance at models with **products** of columns, where a single 226 mm height, multiplied by other columns, can send a prediction off by hundreds of years.

## A Small Lab

Remember why we want a model: counting rings is slow. A lab that has to count them doesn't get 4,000 aged abalone; it gets a few hundred. So we play that lab. We take **400** abalone at random as the ones whose rings were counted, and split them as always:

```python
from sklearn.model_selection import train_test_split

lab = clean.sample(400, random_state=1)
X = lab.drop(columns=["rings", "age_years"])
y = lab["age_years"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
```

That gives **300 training abalone** and **100 test abalone**. The test set stays locked until the end. The training abalone range from 4.5 to 24.5 years old, 11.6 on average.

## One Line

Start with one column. Of the seven measurements, `shell_g` goes along with age most closely. Here are the 300 training abalone:

![Scatter plot of the 300 training abalone, shell weight in grams on the horizontal axis (0 to 185) and age in years on the vertical axis (2 to 26). The points rise from about 5 years at the lightest shells to 10 to 20 years at the heaviest, fanning out as they go. An orange least-squares line runs through the cloud, labeled "age ≈ 8.24 + 0.0716 × shell weight". One abalone, with a 67 g shell and age 17.5, is circled; a dashed vertical segment from the line up to it is labeled "residual = 17.5 − 13.0 = +4.5".](images/abalone_line.png)

Heavier shells go with older abalone, but loosely: at 50 g, ages run from about 9 to 18 years. A **straight line** through the cloud turns any shell weight into a prediction:

```
predicted age = b0 + b1 × shell weight
```

`b1` is the **slope**: how much the prediction rises for each extra gram of shell. `b0` is the **intercept**: where the line crosses zero grams. Together they are the model's **coefficients**, and training means choosing them.

Which line is best? Look at the circled abalone: its shell weighs 67 g and it is 17.5 years old. The line predicts 13.0, so it misses by 17.5 − 13.0 = 4.5 years. That vertical miss is the abalone's **residual**:

```
residual = actual − predicted
```

A positive residual means the abalone is **older** than predicted; a negative one, younger. **Least squares** picks the line that makes the **sum of the squared residuals** over all training abalone as small as possible. Squaring keeps positive and negative misses from canceling out, and it makes a big miss count much more than a small one (one miss of 4 adds 16; four misses of 1 add only 4).

scikit-learn fits it with `LinearRegression`, using the same `fit` and `predict` as every model so far:

```python
from sklearn.linear_model import LinearRegression

line = LinearRegression().fit(X_train[["shell_g"]], y_train)
line.intercept_, line.coef_        # 8.24 and [0.0716]
```

So the best line is:

```
predicted age = 8.24 + 0.0716 × shell weight (g)
```

- **Slope 0.0716:** each extra gram of shell goes with about 0.07 more years, or about **0.7 years per 10 grams**.
- **Intercept 8.24:** the prediction for a shell weighing 0 g. No abalone has a weightless shell, and no 8-year-old does either; the intercept just positions the line.

A 50 g shell predicts 8.24 + 0.0716 × 50 = 11.8 years; a 100 g shell, 15.4 years.

Notice in the plot what a straight line can't do. The young abalone hug the line closely, while the old ones scatter far above it. Abalone grow fast when young and slowly when old, so the oldest shells aren't much heavier than middle-aged ones. Page 6 comes back to what that does to old abalone.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Which of these is a regression problem?**

- [x] Predicting an abalone's age in years from its measurements.
- [ ] Predicting whether an abalone is male, female or infant.
- [ ] Predicting whether an abalone is older than 10 years: yes or no.
- [ ] Grouping abalone into clusters without any label.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

The line is: predicted age = 8.24 + 0.0716 × shell weight. An abalone with a 25 g shell is predicted to be about **[10.0]** years old (one decimal). If it is really 8.5, its residual is 8.5 − 10.0 = **[-1.5]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Why did we drop the four abalone with heights of 0, 103 and 226 mm?**

- [x] Those heights are impossible for their shells, so they are almost certainly typing mistakes, and extreme values can distort a model badly.
- [ ] LinearRegression can't handle the value 0.
- [ ] Any abalone taller than 60 mm is too old to be useful.
- [ ] Dropping rows always makes a model more accurate.

<!-- END QUESTION -->

# How Far Off? MAE, RMSE and R²

## Five Test Abalone

Accuracy, precision and recall count right and wrong answers. For numbers we measure **how far off** the predictions are. Here is the line on five test abalone (predictions rounded to one decimal):

| abalone | shell (g) | actual age | predicted | residual |
|:---|---:|---:|---:|---:|
| A | 34.0 | 13.5 | 10.7 | +2.8 |
| B | 65.6 | 12.5 | 12.9 | −0.4 |
| C | 64.5 | 10.5 | 12.9 | −2.4 |
| D | 11.0 | 8.5 | 9.0 | −0.5 |
| E | 78.0 | 19.5 | 13.8 | +5.7 |

## MAE: the Typical Miss

The **mean absolute error (MAE)** drops the signs and averages the misses:

```
MAE = (2.8 + 0.4 + 2.4 + 0.5 + 5.7) ÷ 5 = 11.8 ÷ 5 = 2.36
```

On these five abalone, the line is typically about 2.4 years off. MAE is in the label's own units (years), so it's easy to explain to a biologist.

## RMSE: Big Misses Count More

The **root mean squared error (RMSE)** squares each residual, averages the squares, and takes the square root to get back to years:

```
RMSE = √((2.8² + 0.4² + 2.4² + 0.5² + 5.7²) ÷ 5)
     = √((7.84 + 0.16 + 5.76 + 0.25 + 32.49) ÷ 5)
     = √(46.5 ÷ 5) = √9.3 ≈ 3.05
```

RMSE is larger than MAE (3.05 against 2.36) because squaring blows up the big misses: abalone E's 5.7 years contributes 32.49 of the 46.5, about 70%. RMSE is always at least as large as MAE; the more uneven the misses, the bigger the gap. RMSE is also the natural score for least squares, since it's built from the same squared residuals that least squares minimizes.

## Scored on All 100 Test Abalone

```python
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

predicted = line.predict(X_test[["shell_g"]])
mean_absolute_error(y_test, predicted)         # 2.01
root_mean_squared_error(y_test, predicted)     # 2.62
```

On all test abalone: MAE **2.01** years, RMSE **2.62** years.

The single worst miss is a 19.5-year-old with a 33.8 g shell, a light shell for its age. The line predicts 10.7 and misses by 8.8 years. That one abalone holds **11%** of all the squared error on 100 abalone. Leave it out, and MAE barely moves (2.01 → 1.94), while RMSE drops from 2.62 to 2.48. **MAE describes the typical abalone; RMSE is pulled toward the worst misses.** Which matters more depends on the cost of a big miss.

## Is 2 Years Good? The Lazy Model and R²

> 🔁 **From Reading 5:** before praising a score, compare it with a **lazy model**. For classification, the lazy model always predicted the most common class.

For regression, the lazy model always predicts the **training average**, 11.6 years, for every abalone. On the test abalone it misses by MAE **2.69** and RMSE **3.41**. The line does better, but not by a landslide.

**R²** ("R squared") turns that comparison into one number:

```
R² = 1 − (the model's sum of squared residuals ÷ the lazy model's sum of squared residuals)
```

- **R² = 1:** perfect predictions, no squared error left.
- **R² = 0:** no better than always guessing the average.
- **R² below 0:** worse than the average. It can happen on test data.

```python
r2_score(y_test, predicted)                    # 0.39
```

R² = 0.39: the line removes about 39% of the lazy model's squared error. Shell weight helps, but most of what makes one abalone older than another is still unexplained. Unlike MAE and RMSE, R² has **no units**, so it can compare models across different labels, but it hides how many years the misses are.

| metric | answers | units | perfect |
|:---|:---|:---|:---|
| MAE | how far off is a typical prediction? | the label's (years) | 0 |
| RMSE | the same, with big misses counting more | the label's (years) | 0 |
| R² | what share of the lazy model's squared error is gone? | none | 1 |

📌 **One split:** these are 100 test abalone. Another random lab of 400 would give somewhat different numbers.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

Three abalone have residuals of +2, −2 and 0 years. Their MAE is **[1.33]** years (two decimals), and their RMSE is √((4 + 4 + 0) ÷ 3) ≈ **[1.63]** years (two decimals).

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Leaving out one badly missed abalone lowered the RMSE from 2.62 to 2.48, but the MAE only from 2.01 to 1.94. Why does RMSE react more?**

- [x] RMSE squares each residual before averaging, so one big miss weighs far more than many small ones.
- [ ] RMSE only counts the largest residual.
- [ ] MAE ignores abalone with large residuals.
- [ ] RMSE is measured in squared years, so it is always bigger.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

An R² of 0 means the model predicts an age of 0 for every abalone.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

The lazy model for regression always predicts the training *[average]*. A model with R² = 1 makes *[perfect]* predictions. MAE and RMSE are measured in the label's *[units]*, while R² has none.

<!-- END QUESTION -->

# More Columns, One Slope Each

## A Line With Many Columns

With more columns, the line gets one slope per column:

```
predicted age = b0 + b1 × shell weight + b2 × meat weight + b3 × …
```

With two columns it's no longer a line but a flat surface in 3-D; with nine columns, a flat surface in nine dimensions. Training is the same: least squares picks all the coefficients at once to make the sum of squared residuals as small as possible.

## The Meat Puzzle

Take `meat_g`, the weight of the meat. Fit it alone, and then next to `shell_g`:

```python
LinearRegression().fit(X_train[["meat_g"]], y_train).coef_                # [0.032]
LinearRegression().fit(X_train[["shell_g", "meat_g"]], y_train).coef_     # [0.150, -0.055]
```

- **Alone:** more meat goes with an **older** abalone, +0.032 years per gram (about +3 years per 100 g). Bigger abalone have more meat, and bigger abalone tend to be older.
- **Next to shell weight:** more meat goes with a **younger** abalone, −0.055 years per gram.

The sign flipped. How can more meat mean both older and younger?

Next to `shell_g`, each slope means "**holding the other columns fixed**." The second model compares two abalone with the **same shell weight**, one meatier than the other. Among abalone with equal shells, the meatier one tends to be younger. One likely reason: shells keep thickening as an abalone ages, so an older abalone carries a heavier shell for the amount of meat inside. Alone, meat weight just stands in for size; next to shell weight, it says something about shape. And with the meat in the model, the shell's own slope doubles, from 0.072 to 0.150.

So a coefficient is never a fact about one column by itself. It answers a question about that column **given the other columns in the model**. Add or remove a column, and the answer can shrink, grow, or flip sign. Remember that before reading any coefficient as "the effect of" something.

## Every Column, in a Pipeline

> 🔁 **From Reading 7:** a pipeline chains the preparation steps and the model, and fits every step on the training rows only. Word columns become 0/1 columns with one-hot encoding.

The file has seven number columns and one word column, `sex`. Its three categories hide a biological fact: an abalone's sex can't be told until it matures, so "infant" really means "young." Infants average 9.5 years in the training set, females 13.0, males 12.1. Here everything goes in:

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric = ["length_mm", "diameter_mm", "height_mm", "whole_g", "meat_g", "gut_g", "shell_g"]

model = Pipeline([
    ("prep", ColumnTransformer([
        ("num", "passthrough", numeric),                        # numbers as they are
        ("words", OneHotEncoder(drop="first"), ["sex"]),        # sex → 0/1 columns
    ])),
    ("scale", StandardScaler()),
    ("reg", LinearRegression()),
])
```

Two details are new.

**`drop="first"`.** In Reading 7, `drop="if_binary"` dropped the second column of a two-category word column. A linear model needs a little more. The three `sex` columns always add up to exactly 1 (every abalone is exactly one of the three), and so does the intercept's hidden column of 1s. Then infinitely many coefficients give the same predictions: add 5 to all three `sex` slopes and subtract 5 from the intercept, and nothing changes. `drop="first"` keeps only two of the three columns, `sex_infant` and `sex_male`. The dropped category, `female` (first alphabetically), becomes the **baseline**: the slope for `sex_infant` means "compared with a female of the same size." In this model, an infant is predicted about 1.4 years younger than a female with identical measurements.

**`StandardScaler` after the one-hot step.** For plain least squares, scaling doesn't change any prediction; it only changes the units of the coefficients (per standard deviation instead of per gram or mm). We include it now because page 5's methods do care about scale.

Seven numbers plus two one-hot columns make **9 columns**. Cross-validated on the training abalone, as in Reading 6:

```python
from sklearn.model_selection import cross_validate

scores = cross_validate(model, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error",
                        return_train_score=True)
-scores["train_score"].mean()        # 2.07: RMSE on the folds it learned from
-scores["test_score"].mean()         # 2.19: RMSE on the held-out fold
```

(scikit-learn always maximizes scores, so it reports *negative* RMSE: a smaller error is a bigger negative number. The minus signs turn them back.)

Two things to notice. First, 2.07 against 2.19: a small gap, so **no real overfitting**. Second, the one-line model, cross-validated the same way, scores **2.50**. The other eight columns cut the typical miss by about 0.3 years: weights and sizes together say more about age than shell weight alone.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Alone, more meat goes with an older abalone; next to shell weight, more meat goes with a younger one. What is the best explanation?**

- [x] Next to shell weight, the meat slope compares abalone with the same shell weight; among those, the meatier ones tend to be younger.
- [ ] The second model has a bug, since a column's coefficient can't change sign.
- [ ] Adding a column always reverses the signs of the others.
- [ ] Meat weight is measured wrong for older abalone.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A word column `color` has four categories: brown, green, red and white. With `OneHotEncoder(drop="first")` it becomes **[3]** columns, and the dropped category, **[brown]** (first alphabetically), becomes the baseline the others are compared with.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

In this data, an abalone's sex can't be told while it is young, so the category "infant" also carries information about age.

<!-- END QUESTION -->

# Too Much Freedom: Overfitting Returns

## An Even Smaller Lab

Page 3's 9-column model didn't overfit: 2.07 years on the folds it learned from, 2.19 on the held-out fold. Three hundred abalone are plenty to set 9 coefficients. But counting rings is the slow part, and many labs age far fewer. Suppose ours had aged only **15**.

From here on we'll swap the last step of page 3's pipeline, so it goes in a small function:

```python
def abalone_model(regressor):
    """Page 3's pipeline, with any regressor as its last step."""
    return Pipeline([
        ("prep", ColumnTransformer([
            ("num", "passthrough", numeric),
            ("words", OneHotEncoder(drop="first"), ["sex"]),
        ])),
        ("scale", StandardScaler()),
        ("reg", regressor),
    ])

few = X_train.sample(15, random_state=9)       # pretend the lab aged only these 15
few_age = y_train[few.index]
others = X_train.drop(few.index)                # the other 285 stand in for new abalone
others_age = y_train[others.index]

small = abalone_model(LinearRegression()).fit(few, few_age)
root_mean_squared_error(few_age, small.predict(few))           # 1.77
root_mean_squared_error(others_age, small.predict(others))     # 4.77
```

On the 15 abalone it learned from, the model misses by **1.77** years, closer than page 3's model ever got. On the other 285 it misses by **4.77**, almost twice as much as a single line through shell weight fitted to the same 15 (2.53). Its predictions for the 285 run from **−7.3 to 26.2 years**: six abalone are predicted to be younger than zero.

> 🔁 **From Readings 5 and 6:** great on the data the model learned from, much worse on new data: **overfitting**. kNN with k = 1 and a tree with no depth limit did the same.

## Coefficients That Make No Sense

The model chose 10 numbers (9 coefficients and the intercept) to fit 15 ages: almost one number per abalone. Here are its coefficients next to page 3's, which came from all 300. The columns are standardized, so each coefficient is in **years per standard deviation** of its column:

```python
small[-1].coef_        # the coefficients of the pipeline's last step
```

| column | from 300 abalone | from 15 abalone |
|:---|---:|---:|
| `length_mm` | −0.36 | **+19.78** |
| `diameter_mm` | +1.11 | **−20.45** |
| `height_mm` | +0.83 | −1.64 |
| `whole_g` | +4.90 | +5.72 |
| `meat_g` | −4.92 | **−11.37** |
| `gut_g` | −1.36 | +1.79 |
| `shell_g` | +1.29 | +6.37 |
| `sex_infant` | −0.66 | −1.45 |
| `sex_male` | −0.07 | +0.24 |

Three things are wrong with the second column:

- **Too big.** The abalone here are 4.5 to 24.5 years old. A coefficient of 20 years says that one typical step up in shell length adds more years than most abalone live.
- **A tug of war.** Length gets +19.78 and diameter −20.45. In these 15 abalone, length and diameter have a correlation of **0.996**: they are practically the same column. The model pushes hard on one and pulls just as hard on the other, and the two almost cancel.
- **Columns that add nothing new.** Diameter repeats length. Whole weight is mostly meat, gut and shell. Yet each gets its own large coefficient.

On the 15 training abalone, the tug of war balances out. But it balances on the **tiny differences** between near-twin columns, and in 15 abalone those differences are mostly luck. On a new abalone they are different, the two giant coefficients no longer cancel, and the prediction swings, all the way down to −7.3 years.

Why would least squares choose this? It has one goal: the smallest squared residuals **on the 15**. With near-copies, many pairs of coefficients fit almost equally well (+20 and −20, or +1 and 0), and least squares takes whichever pair wins on these 15, even by a hair, however big it is. Page 3's model shows a milder version with 300 abalone: whole weight +4.90 against meat −4.92, the meat puzzle. With 15 abalone, the meat coefficient more than doubles.

So overfitting in regression has a recognizable symptom: **coefficients that are too big, fight each other, and sit on columns that add nothing new**.

This is the regression version of the semester's lesson. Every model has a dial of **freedom**: k in kNN, depth in a tree, and here, **how many coefficients for how many rows**. Nine coefficients for 300 abalone is fine; nine for 15 is too many.

## Taking Freedom Back

The best fix is more abalone, but counting rings is the slow part. Another fix: drop some columns by hand. But which ones? The next page keeps all 9 and instead makes **big coefficients cost something**, so a tug of war becomes too expensive to play.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Fitted to 15 abalone, the 9-column model misses those 15 by 1.77 years and the other 285 by 4.77. What does that tell you?**

- [x] It is overfitting: it fits the abalone it learned from closely, but its predictions for new abalone are much worse than a simpler model's.
- [ ] It is underfitting: 1.77 years is too high an error.
- [ ] It is the best model so far, because 1.77 is the smallest error yet.
- [ ] The other 285 abalone must contain measurement mistakes.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

Fitted to 15 abalone, length gets +19.8 and diameter −20.4 (years per standard deviation). For an abalone one standard deviation above average in both, the two together change the prediction by about **[-0.6]** years (one decimal).

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Two coefficients of about +20 and −20 sit on length and diameter, which are nearly the same column in the 15 abalone. Why is that a problem for new abalone?**

- [x] The two giant coefficients only cancel on the tiny differences seen in training; on a new abalone those differences change, the cancellation fails, and the prediction swings.
- [ ] Coefficients larger than 20 are not allowed in linear regression.
- [ ] Negative coefficients always make predictions worse.
- [ ] Two columns that are nearly the same can't both be scaled.

<!-- END QUESTION -->

# A Price on Big Coefficients: Ridge, Lasso and Elastic Net

## Ridge

Least squares has one goal: small squared residuals. **Ridge regression** adds a second goal: small coefficients. It minimizes

```
sum of squared residuals  +  α × (b1² + b2² + … + b9²)
```

The second part is a **penalty**: every coefficient costs its square, times a number `α` ("alpha") that we choose.

- **α = 0:** no penalty, plain least squares.
- **Bigger α:** big coefficients get expensive, so every coefficient is pulled toward 0. A column keeps a big coefficient only if it lowers the squared residuals by enough to pay for it.

That is exactly what breaks the tug of war. A +19.8 and a −20.4 that nearly cancel cost 19.8² + 20.4² ≈ 808 in penalty, while barely lowering the residuals. Ridge would rather give both columns small, sensible coefficients. (The intercept `b0` is not penalized; it just positions the surface.)

The penalty compares the coefficients with each other, so they must be on the same ruler. A coefficient per gram and a coefficient per millimeter aren't comparable; a coefficient per **standard deviation** of each is. That's why `StandardScaler` comes right before the regressor, after the one-hot step, so even the 0/1 `sex` columns are scaled.

## Lasso

**Lasso** charges the coefficients' **absolute values** instead of their squares:

```
sum of squared residuals  +  α × (|b1| + |b2| + … + |b9|)
```

The difference looks small, but it changes what happens to weak columns. Under Ridge, a coefficient gets smaller and smaller but almost never reaches exactly 0. Under Lasso, many coefficients go **all the way to 0**, and those columns drop out of the model. So Lasso does two jobs at once: it shrinks the coefficients, and it **chooses columns**.

(scikit-learn's `Lasso` divides the sum of squared residuals by 2 × the number of rows. Same idea; it only shifts the scale of α, which is one reason Lasso's α values below are so much smaller than Ridge's.)

## Elastic Net: Both at Once

**Elastic net** charges both penalties, mixed:

```
sum of squared residuals  +  α × [ r × (|b1| + … + |b9|)  +  (1 − r) × (b1² + … + b9²) ]
```

- **Two knobs.** `alpha` (α) sets **how strong** the whole penalty is. `l1_ratio` (r) sets **the balance**: 1 is pure Lasso, 0 is pure Ridge. ("L1" is the name for Lasso's penalty, "L2" for Ridge's.)
- **Why mix?** Faced with near-copies like length and diameter, Lasso tends to keep one and drop the other, or drop both. Ridge keeps every column. Elastic net can drop some columns while letting near-copies **share** a coefficient.
- **Watch the names.** In R's popular `glmnet` package, `alpha` is the *balance* and `lambda` the strength. In scikit-learn, `alpha` is always the strength.

(Like `Lasso`, scikit-learn's `ElasticNet` divides the squared residuals by 2 × the number of rows, and it also halves the Ridge part.)

## Choosing α

`α` is a knob like k or `max_depth`, so it's chosen the same way: grid search with cross-validation, on the 15 abalone the lab has.

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import GridSearchCV

ridge_search = GridSearchCV(abalone_model(Ridge()),
                            {"reg__alpha": [0.1, 1, 3, 10, 30, 100, 300, 1000]},
                            cv=5, scoring="neg_root_mean_squared_error", return_train_score=True)
ridge_search.fit(few, few_age)

lasso_search = GridSearchCV(abalone_model(Lasso(max_iter=200_000)),
                            {"reg__alpha": [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3]},
                            cv=5, scoring="neg_root_mean_squared_error", return_train_score=True)
lasso_search.fit(few, few_age)
```

(`reg__alpha` is the `alpha` knob of the step named `reg`, as in Reading 7. `max_iter` lets Lasso's step-by-step search run long enough to settle.)

![Two line charts side by side, RMSE in years against α on a log scale, from 5-fold cross-validation on the 15 abalone. Left, Ridge, α from 0.1 to 1,000: the training-fold RMSE (solid blue, circles) rises steadily from 1.73 to 3.35; the held-out RMSE (dashed orange, triangles) starts at 3.85, dips to a minimum of 2.75 at α = 10, then rises to 3.48. Right, Lasso, α from 0.001 to 3, on a taller scale up to 12: the training-fold RMSE rises from 1.03 to 3.43; the held-out RMSE falls from 10.69 to a minimum of 3.02 at α = 0.1, then rises to 3.57. Numbers above the Lasso points give the columns kept: 9, 9, 9, 7, 4, 4, 3, 0. A dotted gray line in both panels marks 3.08, one line through shell weight cross-validated on the same 15 abalone.](images/abalone_alpha.png)

Read both panels from left to right:

- **Small α (left edge):** almost no penalty, so page 4's overfitting. Lasso's left edge is practically plain least squares: 1.03 years on the folds it learned from, **10.69** on the held-out fold. Each training fold has 12 abalone for 10 numbers.
- **As α grows:** the training-fold error rises (the model can no longer chase every abalone), and the held-out error first **falls**. Taking back some freedom helps.
- **Best α:** Ridge bottoms out at **2.75** (α = 10). Lasso bottoms out at **3.02** (α = 0.1), keeping **4** of the 9 columns. The dotted line is one line through shell weight, cross-validated the same way: 3.08.
- **Large α (right edge):** the penalty flattens the coefficients so much that both errors rise together: **underfitting**. Lasso at α = 3 keeps no columns at all and predicts the same age for every abalone.

This is the same picture as k in kNN and depth in trees, with one twist: here a **bigger** knob means a **simpler** model.

📌 **One sample:** each held-out fold here holds only 3 abalone. Another 15 abalone could pick another α, or another winner.

Elastic net has two knobs, so its grid has two lists, and `GridSearchCV` tries every pair (6 × 4 = 24 of them):

```python
from sklearn.linear_model import ElasticNet

net_search = GridSearchCV(abalone_model(ElasticNet(max_iter=200_000)),
                          {"reg__alpha": [0.01, 0.03, 0.1, 0.3, 1, 3],
                           "reg__l1_ratio": [0.1, 0.5, 0.9, 1]},
                          cv=5, scoring="neg_root_mean_squared_error")
net_search.fit(few, few_age)
net_search.best_params_        # {'reg__alpha': 1, 'reg__l1_ratio': 0.1}
```

On these 15 abalone, cross-validation picks a mostly-Ridge balance (l1_ratio = 0.1) with a held-out RMSE of 2.81. Elastic net doesn't have to beat both of its parents to be useful: it lets cross-validation choose the balance too.

## What the Penalties Did

| column | least squares | Ridge, α = 10 | Lasso, α = 0.1 | elastic net, α = 0.1, half and half |
|:---|---:|---:|---:|---:|
| `length_mm` | +19.78 | +0.22 | 0 | +0.14 |
| `diameter_mm` | −20.45 | +0.28 | 0 | +0.14 |
| `height_mm` | −1.64 | +0.35 | 0 | +0.58 |
| `whole_g` | +5.72 | +0.03 | 0 | 0 |
| `meat_g` | −11.37 | −0.38 | −2.55 | −1.82 |
| `gut_g` | +1.79 | +0.08 | 0 | 0 |
| `shell_g` | +6.37 | +0.38 | +3.31 | +1.74 |
| `sex_infant` | −1.45 | −0.75 | −1.14 | −1.14 |
| `sex_male` | +0.24 | +0.63 | +0.50 | +0.61 |

- **Ridge** shrinks everything. The tug of war is gone: length and diameter now get +0.22 and +0.28, small and on the same side. The largest coefficient is 0.75, down from 20.45.
- **Lasso** keeps 4 columns: shell weight, meat weight (still negative: page 3's meat puzzle survives) and the two `sex` columns. It drops length, diameter, height, whole weight and gut weight.
- **Elastic net**, at a half-and-half balance (`l1_ratio=0.5`), drops whole and gut weight like Lasso, but keeps length and diameter **together**, sharing the same small coefficient (+0.14 each), instead of Lasso's all-or-nothing choice.

## The Final Comparison

The other 285 training abalone were never used to fit or tune these models, so they can stand in as new abalone:

| model, learned from the 15 | columns used | RMSE on the other 285 |
|:---|---:|---:|
| one line (shell weight) | 1 | 2.53 |
| least squares, all columns | 9 | 4.77 |
| Ridge, α = 10 | 9 (all shrunk) | 2.62 |
| Lasso, α = 0.1 | 4 | 2.42 |
| elastic net, α = 1, l1_ratio = 0.1 | 9 (all shrunk) | 2.65 |

The penalties turned the worst model in the table (4.77) into models that miss by about 2.5 years, about what one well-chosen line manages. Notice that Lasso, which cross-validation ranked below Ridge, comes out slightly ahead here. With 3 abalone per fold, cross-validation can't really tell them apart.

> 🔁 **From Reading 6:** the best of many scores is optimistic, and differences smaller than the disagreement between folds are noise. When scores tie, prefer the simpler model.

The biggest improvement isn't in this table, though. Page 3's model, the same 9 columns with plain least squares, learned from **all 300** abalone and scored **2.19** on the held-out fold. With 300 abalone there is little left to fix: Lasso on all 300 picks α = 0.01 and scores 2.18, a tie. **More data is the best cure for overfitting.** A penalty is what you reach for when you can't get more, or when the columns keep multiplying.

## Zooming Out: Curves Overfit Too

Columns can multiply. `PolynomialFeatures(2)` adds a square for every measurement (`shell_g²`, which lets the line bend into a curve) and a product for every pair (`length_mm × whole_g`, …): 7 measurements become 35 columns, 37 with `sex`. Even on all 300 abalone, those 37 coefficients overfit: 1.70 years on the folds the model learned from, 2.53 on the held-out fold, worse than one line. Inside, the same symptom: −20.8 on length × whole weight and +20.6 on diameter × whole weight, another tug of war between near-copies. And the same cure: Lasso keeps 21 of the 37 columns and brings the held-out error down to 2.08.

Is 2.08 better than the 9 plain columns' 2.19? By 0.11 years, about six weeks, while single folds of the 9-column model disagree by much more (from 1.71 to 2.60). By Reading 6's rule that is a tie, and the simpler model wins.

Only now, **once**, open the locked test set for the final model: page 3's 9 columns, plain least squares, all 300 training abalone. RMSE **2.21**, MAE **1.65**, R² **0.57** on the 100 test abalone. 74% of them are predicted within 2 years of their true age.

📌 **One split:** 2.21 is one set of 100 abalone from one random lab of 400.

---

## Check Your Understanding

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

Ridge adds a penalty on the *[squares]* of the coefficients, so every coefficient shrinks but almost none reaches zero. Lasso penalizes their *[absolute]* values, so many coefficients become exactly *[zero]* and those columns drop out. With a very large α, both models *[underfit]*.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Why must the columns be standardized before Ridge, Lasso or elastic net?**

- [x] The penalty compares coefficients with each other, and a coefficient's size depends on its column's units; on one ruler, the penalty treats every column alike.
- [ ] Ridge and Lasso can only read numbers between −1 and 1.
- [ ] Standardizing removes the need to choose α.
- [ ] Without scaling, least squares can't find any coefficients.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**In scikit-learn, what do the two numbers in `ElasticNet(alpha=1, l1_ratio=0.1)` control?**

- [x] `alpha` sets how strong the whole penalty is; `l1_ratio` sets the balance between Lasso's penalty (1) and Ridge's (0), so 0.1 is mostly Ridge.
- [ ] `alpha` sets the balance between Ridge and Lasso; `l1_ratio` sets how strong the penalty is.
- [ ] `l1_ratio = 0.1` means that 10% of the columns are dropped.
- [ ] `alpha` is the share of the rows used for cross-validation.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**On the 15 abalone, cross-validation prefers Ridge (2.75) to Lasso (3.02), but on the other 285 abalone Lasso does a little better (2.42 against 2.62). What is the most sensible reading?**

- [x] With only 3 abalone per held-out fold, cross-validation scores are noisy; neither penalty is clearly better here, and both are far better than plain least squares.
- [ ] Cross-validation is broken, so it should not be used to choose α.
- [ ] Ridge is the better model, because cross-validation said so.
- [ ] Lasso is always better than Ridge.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

In these grids, the largest α gave the best model, because a stronger penalty always reduces overfitting more.

<!-- END QUESTION -->

# Regression, Examined

## The Oldest Machine Learner

> 🔁 **From Readings 5–7:** Adrian Mackenzie's *Machine Learners* traces how machine learning turns tables into spaces of points.

The straight line is much older than machine learning. Mackenzie notes that the first independent use of linear regression, by Carl Friedrich Gauss in 1801, was a prediction: where the newly discovered asteroid Ceres would reappear after its orbit took it behind the sun. Astronomers found it where Gauss said. Two centuries later the line is still at the center of the field:

> "The importance of lines and flat surfaces can hardly be under-estimated in machine learning."

Ridge and Lasso are part of how the line kept up. Mackenzie describes how, on genetic data with thousands of columns, the coefficients "are ranked by importance and then are either reduced (L2 regularization) or eliminated (L1 regularization) if they contribute little to the predictive accuracy of the machine learner." (L2 is Ridge's penalty, L1 is Lasso's.) In one cancer study he cites, Lasso kept 1,429 of 16,063 genes, and an elastic net only 384. His comment:

> "Regularization sometimes radically changes the object."

In our small lab, the 9 columns became 7, then 4, then 3, then none, depending on α, a number we chose from a grid. The penalty decided which measurements of an abalone the model looks at.

## The Dataset Has a History Too

The file you downloaded isn't exactly what the biologists wrote down. Its documentation, from 1995, says two things happened on the way into machine learning:

- "From the original data examples with missing values were removed (the majority having the predicted value missing)." Most of the dropped abalone were missing their **age**, the very label we predict. Reading 7's question applies: were those abalone like the others? The file can't tell us.
- "The ranges of the continuous values have been scaled for use with an ANN (by dividing by 200)." Every measurement was divided by 200 to suit a neural network ("ANN"). The file we use multiplies them back to millimeters and grams. A dataset gets reshaped for the machine learners of its day, and the reshaping stays in the file long after.

## Why Old Abalone Fool the Model

Group the test abalone by their true age and look at the average residual of the final model:

| true age | test abalone | average residual (years) |
|:---|---:|---:|
| under 8 | 18 | −1.0 |
| 8 to 12 | 51 | −0.7 |
| 12 to 16 | 21 | +0.7 |
| over 16 | 10 | +4.5 |

For young and middle-aged abalone, the misses are small and go both ways. But the 10 oldest are predicted **4.5 years too young**, on average. (The single line misses them by 5.5.)

The reason is biology, not math. Abalone grow fast when young and slowly when old. Once growth slows, another five years add little shell or meat. To a model that sees only sizes and weights, a 15-year-old and a 22-year-old can look almost identical, so it predicts something in between. No penalty can fix that: the information simply isn't in the columns. The documentation says as much:

> "Further information, such as weather patterns and location (hence food availability) may be required to solve the problem."

An abalone that grew up where food was scarce is small for its age. The model has no column for that.

## Writing the Press Release

Deborah Stone's chapter 4 of *Counting*, "How Numbers Get Their Clout," includes a tongue-in-cheek guide to writing "a letter of recommendation" for your numbers, so people trust them. Some of her steps:

> "Step 1: Brazenly assert, 'My numbers are right.'"

> "Step 4: Deny that fallible human judgment finds its way into your counting method. Instead of using people as the subject of your verbs, use some of the following abstract nouns: Statistical analysis showed . . . [ … ] Models show that . . ."

> "Step 5: Sprinkle your testimonials about your numbers with cautions to reassure doubters and show your humility. … Yes, my measure is imperfect, but it's the best we have."

Try it on our model. *"Advanced machine-learning models show that an abalone's age can be determined from its weight, with no need to cut the shell."* Every word is defensible, and the impression is wrong. Here is the same model, honestly:

- It is typically **1.65 years** off (MAE), and about 1 in 4 abalone are off by **more than 2 years**.
- It explains about **57%** of the variation in age (R² 0.57) on one test set of 100.
- It underestimates the oldest abalone by **4.5 years** on average, because their size stops changing.
- It learned from **400** abalone from one coast, chosen at random from a file whose label was missing for most of the rows that were dropped.
- Someone chose the columns, the model, and whether to add products or a penalty.

The mathematician John Ewing, Stone writes, calls the dressing-up strategies "mathematical intimidation." A prediction printed as "11.37 years" looks precise. With an RMSE of about 2 years, the honest version is "**somewhere between 9 and 14**."

## Questions Worth Asking About Any Regression

- **What is the label, really?** A ring count plus 1.5, a sale price, a test score: who produced it, and how?
- **Which rows were left out before fitting?** Typing mistakes, missing labels, a small random lab.
- **How big is a typical miss, and the worst one?** MAE and RMSE together, compared with a lazy model.
- **What does a coefficient mean here?** Always "holding the other columns fixed," so it changes with the other columns.
- **Do big coefficients fight each other?** Then the model is probably overfitting, and a penalty may help.
- **Who are the big residuals?** Errors that are small on average can be large and one-sided for one group, like the oldest abalone.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**The final model underestimates the oldest abalone by about 4.5 years on average. Why doesn't a penalty or more columns fix this?**

- [x] Old abalone barely grow, so their sizes and weights look like those of younger adults; the information needed to tell them apart isn't in the columns.
- [ ] The penalty always hurts the oldest abalone the most.
- [ ] RMSE is the wrong metric for old abalone.
- [ ] There are too few columns about sex.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**"Models show that an abalone's age can be determined from its weight." Which of Stone's steps does this sentence follow, and what does it hide?**

- [x] Step 4: it makes "models" the subject of the verb, hiding the people who chose the data, the columns and the penalty, and it skips the 2-year typical error.
- [ ] Step 1: it admits the numbers might be wrong.
- [ ] Step 5: it adds a caution to reassure doubters.
- [ ] None: the sentence reports the model's results accurately.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

According to the dataset's documentation, most of the abalone removed before the data was published were missing their ring count, the very value we predict.

<!-- END QUESTION -->
