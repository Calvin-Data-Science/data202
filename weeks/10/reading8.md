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

This is not a formality. On page 4 we'll build models with **products** of columns, and a single 226 mm height, multiplied by other columns, can send a prediction off by hundreds of years.

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

## Products of Columns

The 9-column model gives each column **one** slope, the same for every abalone. But the plot on page 1 bends: shell weight says a lot about young abalone and little about old ones. A straight line can't bend, unless we hand it new columns that can:

- **Squares:** `shell_g²` lets the prediction curve.
- **Products of two columns:** `length_mm × meat_g`, `height_mm × gut_g`, … let one column's slope depend on another.

scikit-learn's `PolynomialFeatures(2)` makes all of them from the number columns. For our 7 number columns, that's 7 originals, 7 squares and 21 products of two different columns: **35**. Plus the 2 `sex` columns: **37 columns**.

```python
from sklearn.preprocessing import PolynomialFeatures

def abalone_model(regressor, products=False):
    num = (Pipeline([("z", StandardScaler()), ("products", PolynomialFeatures(2, include_bias=False))])
           if products else "passthrough")
    return Pipeline([
        ("prep", ColumnTransformer([("num", num, numeric), ("words", OneHotEncoder(drop="first"), ["sex"])])),
        ("scale", StandardScaler()),
        ("reg", regressor),
    ])
```

(The numbers are standardized before the products, as in Reading 7, so a product of grams and millimeters doesn't produce one enormous column.)

## 37 Columns for 240 Abalone

```python
scores = cross_validate(abalone_model(LinearRegression(), products=True), X_train, y_train, cv=5,
                        scoring="neg_root_mean_squared_error", return_train_score=True)
```

| model | columns | training folds RMSE | held-out fold RMSE |
|:---|---:|---:|---:|
| one line | 1 | 2.50 | 2.50 |
| all columns | 9 | 2.07 | 2.19 |
| all columns + products | 37 | 1.70 | 2.53 |

On the folds it learned from, the 37-column model is the best by far: 1.70 years. On the held-out fold it is the **worst**: 2.53, worse even than one line.

> 🔁 **From Readings 5 and 6:** great on the data the model learned from, worse on new data: **overfitting**. kNN with k = 1 and a tree with no depth limit did the same.

## A Tug of War

Look inside the 37-column model and you find something strange. Its two biggest coefficients, in standard-deviation units:

| column | coefficient |
|:---|---:|
| length × whole weight | −20.8 |
| diameter × whole weight | +20.6 |

Length and diameter go almost perfectly together (a longer shell is a wider shell), so these two products are nearly the same column. The model has learned to push hard on one and pull just as hard on the other, and the two almost cancel. Several other pairs do the same.

On the training abalone the tug of war balances out. But it balances on the **tiny differences** between near-twin columns, and those differences are mostly luck in these 240 abalone (each cross-validation round fits on 4 folds of the 300). On a new abalone, the tiny differences are different, the two giant coefficients no longer cancel, and the prediction swings.

So overfitting in regression has a recognizable symptom: **big coefficients that fight each other**. The seven measurements are all versions of "how big is this abalone" (whole weight and meat weight go together with a correlation of 0.97), and every product multiplies the overlap.

This is the regression version of the semester's lesson. Every model has a dial of **freedom**: k in kNN, depth in a tree, and here, **how many columns** the line gets. Too little freedom: underfitting. Too much: overfitting.

## Taking Freedom Back

One fix: go back to 9 columns. But that throws away every square and product, including the ones that let the line bend for old abalone. The next page keeps all 37 columns and instead makes **big coefficients cost something**, so a tug of war becomes too expensive to play.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**The 37-column model has a training-fold RMSE of 1.70 years but a held-out RMSE of 2.53. What does that tell you?**

- [x] It is overfitting: it fits the abalone it learned from closely, but its predictions for new abalone are worse than a simpler model's.
- [ ] It is underfitting: 1.70 years is too high an error.
- [ ] It is the best model, because 1.70 is the smallest error in the table.
- [ ] The held-out folds must contain measurement mistakes.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

`PolynomialFeatures(2)` on 3 number columns a, b and c makes the 3 originals, the 3 squares (a², b², c²) and the products ab, ac and bc: **[9]** columns in all.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Two coefficients of about −21 and +21 sit on two products that are nearly the same column. Why is that a problem for new abalone?**

- [x] The two giant coefficients only cancel on the tiny differences seen in training; on a new abalone those differences change, the cancellation fails, and the prediction swings.
- [ ] Coefficients larger than 20 are not allowed in linear regression.
- [ ] Negative coefficients always make predictions worse.
- [ ] Two columns that are nearly the same can't both be scaled.

<!-- END QUESTION -->

# A Price on Big Coefficients: Ridge and Lasso

## Ridge

Least squares has one goal: small squared residuals. **Ridge regression** adds a second goal: small coefficients. It minimizes

```
sum of squared residuals  +  α × (b1² + b2² + … + b37²)
```

The second part is a **penalty**: every coefficient costs its square, times a number `α` ("alpha") that we choose.

- **α = 0:** no penalty, plain least squares.
- **Bigger α:** big coefficients get expensive, so every coefficient is pulled toward 0. A column keeps a big slope only if it lowers the squared residuals by enough to pay for it.

That is exactly what breaks the tug of war. A −21 and a +21 that nearly cancel cost 21² + 21² = 882 in penalty, while barely lowering the residuals. Ridge would rather give both columns small, sensible slopes. (The intercept `b0` is not penalized; it just positions the surface.)

The penalty compares the coefficients with each other, so they must be on the same ruler. A slope per gram and a slope per millimeter aren't comparable; a slope per **standard deviation** of each is. That's why `StandardScaler` comes right before the regressor, after the one-hot step, so even the 0/1 `sex` columns are scaled.

## Lasso

**Lasso** charges the coefficients' **absolute values** instead of their squares:

```
sum of squared residuals  +  α × (|b1| + |b2| + … + |b37|)
```

The difference looks small, but it changes what happens to weak columns. Under Ridge, a coefficient gets smaller and smaller but almost never reaches exactly 0. Under Lasso, many coefficients go **all the way to 0**, and those columns drop out of the model. So Lasso does two jobs at once: it shrinks the coefficients, and it **chooses columns**.

## Choosing α

`α` is a knob like k or `max_depth`, so it's chosen the same way: grid search with cross-validation on the training abalone.

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import GridSearchCV

ridge_search = GridSearchCV(abalone_model(Ridge(), products=True),
                            {"reg__alpha": [0.1, 1, 3, 10, 30, 100, 300, 1000]},
                            cv=5, scoring="neg_root_mean_squared_error", return_train_score=True)
ridge_search.fit(X_train, y_train)

lasso_search = GridSearchCV(abalone_model(Lasso(max_iter=200_000), products=True),
                            {"reg__alpha": [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1]},
                            cv=5, scoring="neg_root_mean_squared_error", return_train_score=True)
lasso_search.fit(X_train, y_train)
```

(`reg__alpha` is the `alpha` knob of the step named `reg`, as in Reading 7. `max_iter` lets Lasso's step-by-step search run long enough to settle.)

![Two line charts side by side sharing a y-axis, RMSE in years from 1.5 to 2.9, against α on a log scale. Left, Ridge, α from 0.1 to 1,000: the training-fold RMSE (solid blue, circles) rises steadily from 1.72 to 2.57; the held-out RMSE (dashed orange, triangles) starts at 2.26, dips to a minimum of 2.09 at α = 3, then rises to 2.59, where the two lines meet. Right, Lasso, α from 0.001 to 1: the training-fold RMSE rises from 1.72 to 2.68; the held-out RMSE falls from 2.30 to a minimum of 2.08 at α = 0.01 and rises to 2.69. Numbers above the Lasso points give the columns kept: 32, 29, 21, 15, 9, 6, 2. A dotted gray line in both panels marks 2.19, the 9-column model without products.](images/abalone_alpha.png)

Read both panels from left to right:

- **Small α (left edge):** almost no penalty. Training folds about 1.7, held-out about 2.3: the overfitting of page 4.
- **As α grows:** the training-fold error rises (the model can no longer chase every abalone), and the held-out error first **falls**. Taking back some freedom helps.
- **Best α:** Ridge's held-out RMSE bottoms out at **2.09** (α = 3); Lasso's at **2.08** (α = 0.01), keeping **21** of the 37 columns. Both beat the 9-column model's 2.19, which no penalty could give.
- **Large α (right edge):** the penalty flattens the slopes so much that both errors rise together: **underfitting**. Lasso at α = 1 keeps only 2 columns and misses by 2.69 years, worse than the single line.

This is the same picture as k in kNN and depth in trees, with one twist: here a **bigger** knob means a **simpler** model.

## What the Penalties Did

The tug of war is gone. Ridge's biggest coefficient at α = 3 is 3.3, down from 20.8. Lasso's best model keeps 21 columns: shell weight, whole weight and meat weight (still with a negative sign: page 3's meat puzzle survives), the infant column, and a handful of squares and products, the bends a straight line couldn't make. It drops 16 columns, among them diameter itself and most of its products: once length is in, diameter adds little.

Raise Lasso's price to α = 0.1 and it keeps just 9 columns, scoring 2.21, about as well as the 9-column model without products. At α = 1 it keeps two: shell weight and a whisper of height.

## The Final Comparison

| model | columns used | held-out fold RMSE |
|:---|---:|---:|
| one line (shell weight) | 1 | 2.50 |
| all columns | 9 | 2.19 |
| all columns + products | 37 | 2.53 |
| Ridge, α = 3 | 37 (all shrunk) | 2.09 |
| Lasso, α = 0.01 | 21 | 2.08 |
| Lasso, α = 0.1 | 9 | 2.21 |

> 🔁 **From Reading 6:** the best of many scores is optimistic, and differences smaller than the disagreement between folds are noise. When scores tie, prefer the simpler model.

The penalties turned the worst model in the table (2.53) into the best (2.08–2.09). Ridge and Lasso tie, and the gain over the 9-column model is about 0.1 years, a little over a month, while single folds disagree by much more (from 1.7 to 2.6 years for the 9-column model). Either penalized model is a reasonable choice; Lasso's has fewer columns to explain.

Only now, **once**, open the locked test set for the best Lasso: RMSE **2.17**, MAE **1.63**, R² **0.59** on the 100 test abalone. 71% of them are predicted within 2 years of their true age.

📌 **One split:** 2.17 is one set of 100 abalone from one random lab of 400.

---

## Check Your Understanding

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

Ridge adds a penalty on the *[squares]* of the coefficients, so every coefficient shrinks but almost none reaches zero. Lasso penalizes their *[absolute]* values, so many coefficients become exactly *[zero]* and those columns drop out. With a very large α, both models *[underfit]*.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Why must the columns be standardized before Ridge or Lasso?**

- [x] The penalty compares coefficients with each other, and a coefficient's size depends on its column's units; on one ruler, the penalty treats every column alike.
- [ ] Ridge and Lasso can only read numbers between −1 and 1.
- [ ] Standardizing removes the need to choose α.
- [ ] Without scaling, least squares can't find any coefficients.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Ridge at α = 3 and Lasso at α = 0.01 have held-out RMSEs of 2.09 and 2.08 years. Which statement is the most sensible?**

- [x] They are tied: a 0.01-year difference is far smaller than the disagreement between folds, so either is fine, and Lasso's has fewer columns to explain.
- [ ] Lasso is clearly better, because 2.08 is smaller than 2.09.
- [ ] Ridge is clearly better, because it keeps all 37 columns.
- [ ] Neither works, because both errors are above 2 years.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

In this grid, the largest α gave the best model, because a stronger penalty always reduces overfitting more.

<!-- END QUESTION -->

# Regression, Examined

## The Oldest Machine Learner

> 🔁 **From Readings 5–7:** Adrian Mackenzie's *Machine Learners* traces how machine learning turns tables into spaces of points.

The straight line is much older than machine learning. Mackenzie notes that the first independent use of linear regression, by Carl Friedrich Gauss in 1801, was a prediction: where the newly discovered asteroid Ceres would reappear after its orbit took it behind the sun. Astronomers found it where Gauss said. Two centuries later the line is still at the center of the field:

> "The importance of lines and flat surfaces can hardly be under-estimated in machine learning."

Ridge and Lasso are part of how the line kept up. Mackenzie describes how, on genetic data with thousands of columns, the coefficients "are ranked by importance and then are either reduced (L2 regularization) or eliminated (L1 regularization) if they contribute little to the predictive accuracy of the machine learner." (L2 is Ridge's penalty, L1 is Lasso's.) In one cancer study he cites, Lasso kept 1,429 of 16,063 genes. His comment:

> "Regularization sometimes radically changes the object."

Our 37 columns became 21, then 9, then 2, depending on α, a number we chose from a grid. The penalty decided which measurements of an abalone this model looks at.

## The Dataset Has a History Too

The file you downloaded isn't exactly what the biologists wrote down. Its documentation, from 1995, says two things happened on the way into machine learning:

- "From the original data examples with missing values were removed (the majority having the predicted value missing)." Most of the dropped abalone were missing their **age**, the very label we predict. Reading 7's question applies: were those abalone like the others? The file can't tell us.
- "The ranges of the continuous values have been scaled for use with an ANN (by dividing by 200)." Every measurement was divided by 200 to suit a neural network ("ANN"). The file we use multiplies them back to millimeters and grams. A dataset gets reshaped for the machine learners of its day, and the reshaping stays in the file long after.

## Why Old Abalone Fool the Model

Group the test abalone by their true age and look at the average residual of the best Lasso model:

| true age | test abalone | average residual (years) |
|:---|---:|---:|
| under 8 | 18 | −0.8 |
| 8 to 12 | 51 | −0.6 |
| 12 to 16 | 21 | +0.7 |
| over 16 | 10 | +4.3 |

For young and middle-aged abalone, the misses are small and go both ways. But the 10 oldest are predicted **4.3 years too young**, on average. (The single line misses them by 5.5.)

The reason is biology, not math. Abalone grow fast when young and slowly when old. Once growth slows, another five years add little shell or meat. To a model that sees only sizes and weights, a 15-year-old and a 22-year-old can look almost identical, so it predicts something in between. No penalty can fix that: the information simply isn't in the columns. The documentation says as much:

> "Further information, such as weather patterns and location (hence food availability) may be required to solve the problem."

An abalone that grew up where food was scarce is small for its age. The model has no column for that.

## Writing the Press Release

Deborah Stone's chapter 4 of *Counting*, "How Numbers Get Their Clout," includes a tongue-in-cheek guide to writing "a letter of recommendation" for your numbers, so people trust them. Some of her steps:

> "Step 1: Brazenly assert, 'My numbers are right.'"

> "Step 4: Deny that fallible human judgment finds its way into your counting method. Instead of using people as the subject of your verbs, use some of the following abstract nouns: Statistical analysis showed . . . [ … ] Models show that . . ."

> "Step 5: Sprinkle your testimonials about your numbers with cautions to reassure doubters and show your humility. … Yes, my measure is imperfect, but it's the best we have."

Try it on our model. *"Advanced machine-learning models show that an abalone's age can be determined from its weight, with no need to cut the shell."* Every word is defensible, and the impression is wrong. Here is the same model, honestly:

- It is typically **1.6 years** off (MAE), and 3 in 10 abalone are off by **more than 2 years**.
- It explains about **59%** of the variation in age (R² 0.59) on one test set of 100.
- It underestimates the oldest abalone by **4 years** on average, because their size stops changing.
- It learned from **400** abalone from one coast, chosen at random from a file whose label was missing for most of the rows that were dropped.
- Someone chose the columns, the products, the penalty and α.

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

**The best model underestimates the oldest abalone by about 4 years on average. Why doesn't a stronger penalty or more products fix this?**

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
