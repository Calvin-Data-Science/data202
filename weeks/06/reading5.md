---
layout: week
title: "Week 6: Classification basics (kNN)"
week_number: 6
---

# Learning From Answers

## A Table That Comes With Answers

Around 1980, researchers in the Western Cape, South Africa, studied men from a region with high rates of heart disease. For each man they recorded a few risk factors (age, smoking, cholesterol, family history) and one more thing: whether he had **coronary heart disease (CHD)**, the narrowing of the arteries that feed the heart.

Suppose a clinic wants to use this table for a new patient. The question is: *given his age, smoking, cholesterol and family history, is he more like the men who had heart disease, or like the men who didn't?*

**📥 Download the dataset: [heart.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/heart.csv)**

This is real data, published with the textbook *The Elements of Statistical Learning* (Hastie, Tibshirani & Friedman), which made it one of machine learning's classic teaching datasets. There are no names in it.

```python
import pandas as pd

heart = pd.read_csv("heart.csv")
heart[["age", "tobacco", "ldl", "famhist", "chd"]].head(3)
```

| age | tobacco | ldl | famhist | chd |
|---:|---:|---:|:---|---:|
| 52 | 12.00 | 5.73 | Present | 1 |
| 63 | 0.01 | 4.41 | Absent | 1 |
| 46 | 0.08 | 3.48 | Present | 0 |

**What is one row about?** One man. The file has nine measurements per man; we'll use four, plus the answer:

| Column | What it measures | Unit |
|:---|:---|:---|
| `age` | his age | years |
| `tobacco` | tobacco smoked over his lifetime | kilograms |
| `ldl` | LDL ("bad") cholesterol | mmol/L |
| `famhist` | heart disease in his family? | Present / Absent |
| `chd` | **does he have coronary heart disease?** | 1 = yes, 0 = no |

## Features and a Label

The first four columns describe each man; they are the **features**. The last column, `chd`, is the answer we'd like to predict for new patients; it is the **label**. Learning from examples that come with a label, and then predicting the label for new cases, is called **supervised learning**: the labels "supervise" the learning by telling the model what the right answers were. (Last week's credit applicants had no label column; that was *unsupervised* learning.)

When the label is a **category** (heart disease or not, spam or not, which species) the task is called **classification**, and a model that does it is a **classifier**. When the label is a number (a price, a weight) the task is called *regression*, which comes later in the semester.

```python
heart["chd"].value_counts()
```

```text
chd
0    302
1    160
Name: count, dtype: int64
```

160 of the 462 men (34.6%) have heart disease. Keep that number in mind; it matters on page 5.

## Looking at Two Features

Here are two of the features, age and lifetime tobacco, with each man colored by his label:

![Scatter plot of 462 men, age in years (15 to 64) across and lifetime tobacco in kilograms (0 to 31) up. Blue circles are men without heart disease; orange triangles are men with it. Young men, at the left, are mostly blue and smoked little. From about age 40 on, orange triangles become common, and most men who smoked more than 10 kilograms are orange. But everywhere above age 40 the blue and orange points are thoroughly mixed.](images/heart_age_tobacco.png)

There is a pattern: older men and heavier smokers are more often orange. But there is no clean border. Plenty of 60-year-old heavy smokers have no heart disease, and some 30-year-olds who barely smoked do. Whatever classifier we build, it will make mistakes, and a large part of this reading is about *measuring* those mistakes honestly.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**In the heart-disease table, what is the *label*?**

- [x] The `chd` column: the answer (heart disease or not) that we want a model to predict for new patients.
- [ ] The `age` column, because it is the first column.
- [ ] Any column with numbers in it.
- [ ] The row number of each man.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Which of these is a *classification* task?**

- [x] Predicting whether a loan applicant will repay (yes or no) from their financial history.
- [ ] Predicting a house's selling price in dollars from its size and location.
- [ ] Grouping customers into types when no one has labeled any customer.
- [ ] Squeezing ten columns into two with PCA.

<!-- END QUESTION -->

# Ask the Neighbors: k-Nearest Neighbors

## The Recipe

The simplest classifier there is follows a common-sense idea: **a new patient is probably like the patients most similar to him.** It's called **k-nearest neighbors (kNN)**:

1. **Measure** the distance from the new patient to every patient whose label we know.
2. **Take** the `k` closest: his *neighbors*.
3. **Vote:** the most common label among the neighbors is the prediction.

The `k` in kNN is a **hyperparameter**: a setting *we* choose before the model runs. The data doesn't choose it.

## Distance Needs One Ruler

"Closest" means the straight-line (Euclidean) distance from Reading 4: square the difference in each column, add them up, take the square root. And Reading 4's warning applies here too: columns in different units don't get a fair vote. Age varies by about 15 years from man to man, LDL cholesterol by about 2 mmol/L. Measured raw, a two-year age gap would count as much as a 2-point jump in LDL, which is the whole difference between normal and high cholesterol.

So we **standardize** first: every column becomes a z-score (subtract its mean, divide by its standard deviation), and then a difference of 1 means "one typical difference" in any column. Family history, a yes/no column, is coded as 1 (Present) or 0 (Absent) so that it can be measured too:

```python
heart["famhist"] = (heart["famhist"] == "Present").astype(int)
```

## One New Patient

A new patient walks in: **age 52, 2.0 kg of tobacco, LDL 5.5, with family history.** Which of the 323 patients with known labels (the next page explains why not all 462) are most like him?

To *see* the recipe, start with just two of his features, age and LDL. The black star is the new patient; each dashed circle reaches out until it holds his `k` nearest neighbors, and those neighbors vote:

![Three zoomed-in panels of age (41 to 63) against LDL cholesterol (3.9 to 7.1), all centered on a black star at age 52, LDL 5.5. Faint blue circles and orange triangles in the background are other training patients. Left, "k = 1: 1 no CHD, predict no CHD": a small dashed circle reaches the single nearest patient, a blue circle at age 51, LDL 5.67. Middle, "k = 5: 2 CHD, 3 no CHD, predict no CHD": a slightly larger circle holds five patients joined to the star by thin lines, three blue and two orange. Right, "k = 25: 13 CHD, 12 no CHD, predict CHD": a large circle spanning ages 45 to 59 holds 25 patients, 13 orange and 12 blue, so the orange triangles win by one vote.](images/heart_knn_neighbors.png)

(The axes are drawn so that one standard deviation of age is as long as one standard deviation of LDL, so the circles you see are exactly the "equally close" circles kNN uses after standardizing. Where two neighbors sat on top of each other, one was nudged sideways so both show.)

The bigger the circle, the more patients get a vote, and the further away some of them are: some of the 25 are as much as 7 years older or younger than him. With k = 1 the answer depends on one man; with k = 25 it depends on a crowd.

The model we'll actually use measures distance with all four features. That can't be drawn on a flat page, but the recipe is identical. Here are his five nearest neighbors in four dimensions, with distances in standardized units:

| neighbor | age | tobacco | ldl | famhist | chd | distance |
|:---|---:|---:|---:|---:|---:|---:|
| 1st | 51 | 2.38 | 5.67 | 1 | 0 | 0.14 |
| 2nd | 54 | 1.70 | 5.28 | 1 | 0 | 0.18 |
| 3rd | 53 | 1.25 | 4.69 | 1 | 0 | 0.43 |
| 4th | 49 | 0.70 | 4.90 | 1 | **1** | 0.46 |
| 5th | 51 | 0.00 | 6.06 | 1 | 0 | 0.52 |

- **k = 1:** his single nearest neighbor has no heart disease → **predict 0.**
- **k = 5:** 1 of 5 neighbors has heart disease → **predict 0.**
- **k = 25:** 13 of his 25 nearest neighbors have heart disease → **predict 1.**

With four features the neighbors change a little (the 5-neighbor vote is now 1 to 4 instead of 2 to 3), but the verdicts are the same as in the picture. Same patient, same data, a different `k`, and the prediction flips. Notice also how close that last vote was: 13 to 12. kNN's prediction is a vote count, and a vote count can be close.

## kNN in scikit-learn

Every supervised model in scikit-learn works the same way: create it with its hyperparameters, `fit` it on features `X` and labels `y`, then `predict` labels for new rows.

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=25)
knn.fit(X_train_scaled, y_train)          # features and labels of the patients we know
knn.predict(new_patient_scaled)           # → array([1])
```

(`X_train_scaled` and `y_train` are built on the next page.) Notice what `fit` does for kNN: almost nothing. It just *stores* the known patients. All the work (measuring distances, taking a vote) happens at `predict` time. That is why kNN is sometimes called a "lazy learner."

---

## Check Your Understanding

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

To classify a new case, kNN measures the *[distance]* to every labeled case, takes the k *[closest]* ones, and predicts the label that wins the *[vote]*. Because we choose k before the model runs, k is a *[hyperparameter]*.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A new email's 7 nearest neighbors are 4 spam and 3 not spam. With k = 7, kNN predicts **[spam]**. If only its 3 nearest neighbors were used and they were 1 spam and 2 not spam, kNN with k = 3 would predict **[not spam]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**A dataset has `income` (in dollars, varying by tens of thousands) and `num_children` (varying by about 1). Why should you standardize before running kNN?**

- [x] Otherwise distances are decided almost entirely by income, so the neighbors are just people with similar incomes and the number of children barely counts.
- [ ] kNN can't run on columns with different units, so scikit-learn would raise an error.
- [ ] Standardizing removes the label, which kNN doesn't need.
- [ ] Standardizing makes kNN choose k automatically.

<!-- END QUESTION -->

# Testing on Patients the Model Has Never Seen

## A Score That Means Nothing

How good is kNN at this? The tempting test: predict the label of every patient we know, and count how often it's right. That share is the **accuracy**. With k = 1 it is **100%**.

That's no achievement. Every known patient's nearest neighbor is *himself*, at distance 0, so k = 1 just copies his own label back. A model scored on the data it learned from can score perfectly by **memorizing**. The question that matters is about the *next* patient, one the model has never seen.

## Make Some Patients "New": the Train/Test Split

We don't have next year's patients. So we **hide some of the ones we have**:

1. Shuffle the 462 patients and set aside 30% of them: the **test set**. Lock it away.
2. `fit` the model on the other 70%: the **training set**.
3. `predict` the test set and compare with its true labels: the **test score**.

**The rule:** nothing from the test set goes into `fit`. Not the model's `fit`, and not the scaler's `fit` either. The test patients play the part of future patients, and future patients aren't around when you build the model.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X = heart[["age", "tobacco", "ldl", "famhist"]]
y = heart["chd"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler().fit(X_train)       # means and std devs of the TRAINING patients only
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)     # test patients measured with the training ruler
```

`train_test_split` shuffles the rows, then cuts `X` and `y` at the same place, so you always get four pieces in this order:

| | features `X` | label `y` |
|:---|:---|:---|
| **training set** (323 patients) | `X_train` | `y_train` |
| **test set** (139 patients) | `X_test` | `y_test` |

The rows stay matched: the 5th row of `X_test` is the patient whose label is the 5th entry of `y_test`. `random_state=42` makes the "random" shuffle the same every time the code runs.

## Training Score vs. Test Score

```python
from sklearn.metrics import accuracy_score

for k in [1, 25]:
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train_scaled, y_train)
    print(f"k = {k} | train: {accuracy_score(y_train, knn.predict(X_train_scaled)):.3f}"
          f" | test: {accuracy_score(y_test, knn.predict(X_test_scaled)):.3f}")
```

```text
k = 1 | train: 1.000 | test: 0.647
k = 25 | train: 0.746 | test: 0.748
```

| | on the training patients | on the test patients |
|:---|---:|---:|
| k = 1 | **100%** | 64.7% |
| k = 25 | 74.6% | **74.8%** |

k = 1 is perfect on patients it has seen and much worse on patients it hasn't. That **gap between training and test score** is the signature of a model that memorized instead of learned. k = 25 scores about the same on both, and better on the test set, which is the score that predicts how it would do on the next patient.

📌 **One split:** 74.8% is the score on *these* 139 test patients. Another shuffle would put other patients in the test set, and the score would move. Page 4 shows by how much.

---

## Check Your Understanding

<!-- QUESTION:true-false
answer: false
-->

A kNN model with k = 1 scores 100% accuracy on its own training data. This shows it will be very accurate on new data.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**A student standardizes all 462 patients with `StandardScaler().fit_transform(X)` and only *then* splits into training and test sets. What's the problem?**

- [x] The scaler's means and standard deviations were computed using the test patients too, so information from the "future" leaked into the model before it was tested.
- [ ] There is no problem; scaling before or after the split gives the same test score in every case.
- [ ] `StandardScaler` can only be used on the test set.
- [ ] The split will no longer keep rows of X and y matched.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A dataset has 500 rows. `train_test_split(X, y, test_size=0.2)` puts **[400]** rows in the training set and **[100]** rows in the test set.

<!-- END QUESTION -->

# Choosing k: Overfitting and Underfitting

## Three Maps

Color every spot of the age/tobacco plot by what kNN would predict for a patient standing there, and you get the model's **map**. (This uses only two features, so it fits on a page; the dots are the 323 training patients.)

![Three panels with age across and tobacco up, background colored by kNN's prediction: blue for "no CHD," orange for "CHD." Left, "k = 1: too wiggly": the background is a patchwork of small blue and orange islands, one around almost every dot, including orange islands among young non-smokers. Middle, "k = 25: in between": mostly blue for younger men and light smokers, orange for older men, especially older heavy smokers, with a ragged border between. Right, "k = 151: too simple": the whole map is blue; the model never predicts heart disease.](images/heart_knn_maps.png)

- **k = 1 is too wiggly.** Every unusual patient gets his own island. The map follows the *noise*, the accidents of who happened to be in this sample. This is **overfitting**: too flexible, fitting the training data so closely that it fits its quirks.
- **k = 151 is too simple.** With 151 voters, the majority (no CHD) wins everywhere. The map can't see any pattern at all. This is **underfitting**: too rigid to capture the structure that is there.
- **k = 25 is in between.**

## The Accuracy Curve

Instead of eyeballing maps, score every k from 1 to 151 on both sets:

```python
scores = []
for k in range(1, 152, 2):
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train_scaled, y_train)
    scores.append({"k": k,
                   "train": accuracy_score(y_train, knn.predict(X_train_scaled)),
                   "test": accuracy_score(y_test, knn.predict(X_test_scaled))})
```

(Odd values of k only, so a two-label vote can't tie.)

![Line chart of accuracy against k from 1 to 151, for training patients (solid blue) and test patients (dashed orange). At k = 1, training accuracy is 100% and test accuracy is 64.7%. Training accuracy falls fast, to about 75% by k = 10, then slowly to 66% at k = 151. Test accuracy rises from 64.7% to about 74% by k = 20, wobbles between 72% and 78% up to about k = 100, then falls to 65.5% at k = 151. A dotted gray line at 64.7% marks the lazy model that always predicts "no CHD."](images/heart_k_curve.png)

Read it from left to right:

- **Small k (left):** training accuracy near 100%, test accuracy much lower. Big gap → **overfitting**.
- **Large k (right):** both scores sink toward the dotted line, the score of a "model" that says *no heart disease* to everyone. → **underfitting**.
- **In between:** both scores close together, and the test score at its best.

This is the idea that will follow us all semester:

| | on data it learned from | on new data |
|:---|:---|:---|
| **Overfitting**: too flexible | great | worse |
| **Underfitting**: too simple | poor | poor |
| **Good fit** | good | good |

`k` is kNN's knob between the two failures. Almost every model this semester has a knob like it.

## Don't Chase the Bumps

The test curve peaks at **k = 91 (78.4%)**. Should we pick k = 91? Two warnings.

First, the test set has 139 patients, so one more correct patient is +0.7 percentage points. Between k = 15 and k = 100, the bumps are a few patients flipping back and forth: noise, not a real difference.

Second, if we try 76 values of k and keep whichever scores best *on the test set*, the test set has become part of how we built the model. Its score is no longer a fair picture of new patients. (Week 7's *cross-validation* is the way out.) For the rest of this reading we use **k = 25**, a value in the middle of the flat region.

## Another Split, Another Score

How much does the luck of the shuffle matter? Same model (k = 25), same 462 patients, different `random_state`:

| random_state | 42 | 1 | 7 | 15 | 24 | 99 | 2026 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| test accuracy | 74.8% | 73.4% | 71.2% | 71.2% | 74.1% | 76.3% | 74.1% |
| recall (next page) | 0.39 | 0.37 | 0.55 | 0.40 | 0.52 | 0.55 | 0.49 |

From 71.2% to 76.3%, and recall from 0.37 to 0.55, without changing anything about the model. Anyone who tried a handful of splits and reported only the best one would be overselling it.

📌 **One split:** every number in this reading is one draw from a range like this.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**A model scores 99% accuracy on its training data and 70% on its test data. What is the most likely diagnosis?**

- [x] Overfitting: it has fit the quirks of the training data and doesn't carry over to new cases.
- [ ] Underfitting: it is too simple to capture the pattern.
- [ ] A good fit: 99% is excellent.
- [ ] The test set must have been too large.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

With a very *[small]* k, kNN's map is full of tiny islands and the model is *[overfitting]*. With a very *[large]* k, the majority label wins almost everywhere and the model is *[underfitting]*.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

The best way to choose k is to try many values and keep the one with the highest test-set accuracy; that test accuracy is then a fair estimate of how the model will do on new data.

<!-- END QUESTION -->

# Is 75% Good? Precision and Recall

## The Lazy Model

74.8% sounds decent. But compare it with a "model" that does no work at all: say **no heart disease** to every patient. In our test set, 90 of the 139 patients have no heart disease, so the lazy model is right **90 / 139 = 64.7%** of the time while finding *zero* sick patients.

Accuracy is only meaningful next to that baseline. When one label is much more common, a model can score well just by predicting it, and miss exactly the cases we care about.

## The Confusion Matrix

To see *which* mistakes kNN makes, count every combination of true label and predicted label:

```python
from sklearn.metrics import confusion_matrix

knn = KNeighborsClassifier(n_neighbors=25).fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)
confusion_matrix(y_test, y_pred)
```

| | predicted: no CHD | predicted: CHD | total |
|:---|---:|---:|---:|
| **truly no CHD** | **85** | 5 | 90 |
| **truly CHD** | 30 | **19** | 49 |
| **total** | 115 | 24 | 139 |

Rows are the **truth**, columns are the **prediction**, and the diagonal (bold) is where the model is right: (85 + 19) / 139 = 74.8%. The two off-diagonal cells are the two kinds of mistakes, and they are not equally serious:

| mistake | name | here |
|:---|:---|:---|
| predicted CHD, but he doesn't have it | **false positive** | 5 healthy men sent for more tests |
| has CHD, but predicted no CHD | **false negative** | 30 sick men sent home |

## Two Questions Accuracy Doesn't Ask

Treat "has CHD" as the **positive** class, the thing we are trying to find.

- **Recall:** *of the patients who really have CHD, how many did we find?* That's the CHD **row**: 19 / 49 = **0.39**.
- **Precision:** *of the patients we flagged as CHD, how many really have it?* That's the CHD **column**: 19 / 24 = **0.79**.

```python
from sklearn.metrics import precision_score, recall_score

precision_score(y_test, y_pred), recall_score(y_test, y_pred)    # about 0.792 and 0.388
```

So when this model raises an alarm, it's usually right (precision 0.79). But it raises too few alarms: it misses 30 of the 49 sick men (recall 0.39). For a screening tool, where a missed patient goes home with an untreated disease, that's the number that matters most, and the 74.8% accuracy hid it. The lazy model, for comparison, has recall **0**.

## Moving the Vote

kNN's prediction is a vote, and "majority wins" is only one possible rule. `predict_proba` gives the share of the 25 neighbors with CHD, and we can choose where to draw the line:

```python
votes = knn.predict_proba(X_test_scaled)[:, 1]     # share of the 25 neighbors with CHD
flagged = votes >= 0.3                             # flag him if at least 8 of 25 had CHD
```

| flag a patient when CHD neighbors are at least | flagged | accuracy | precision | recall |
|:---|---:|---:|---:|---:|
| 13 of 25 (majority) | 24 | 74.8% | 0.79 | 0.39 |
| 10 of 25 | 49 | 68.3% | 0.55 | 0.55 |
| 8 of 25 | 77 | 64.0% | 0.49 | 0.78 |

Lowering the bar finds more of the sick men (recall up from 0.39 to 0.78) at the price of more false alarms (precision down from 0.79 to 0.49). Accuracy even drops *below* the lazy model's 64.7%, yet for screening this version is arguably the most useful of the three. There's no setting that is best at everything. **Choosing the threshold is choosing which mistake you'd rather make**, and that is a decision about people, not a fact about the data.

📌 **One split:** 0.39 and 0.79 describe *these* 49 men with CHD. Page 4's table showed recall moving from 0.37 to 0.55 across splits.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

A test for a disease is run on 100 people; 20 of them truly have the disease. The model flags 25 people, and 15 of those really have the disease. Its recall is 15 / 20 = **[0.75]** and its precision is 15 / 25 = **[0.6/0.60]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**A fraud detector labels every transaction "not fraud." Fraud is 1% of transactions. Which statement is true?**

- [x] Its accuracy is 99%, but its recall for fraud is 0 — it never finds a single fraud.
- [ ] Its accuracy is 1%, because it is wrong about every fraud.
- [ ] Its precision is 99%, because most transactions are not fraud.
- [ ] It can't be scored, because it never predicts fraud.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**In a confusion matrix with true labels as rows and predictions as columns, a *false negative* for "has CHD" is…**

- [x] A patient who has CHD but was predicted not to have it: in the CHD row, the "predicted no CHD" column.
- [ ] A patient who doesn't have CHD but was predicted to have it.
- [ ] Any patient on the diagonal.
- [ ] A patient whose label is missing.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

Lowering the share of neighbors needed to flag a patient as "CHD" will usually raise recall and lower precision.

<!-- END QUESTION -->

# Machine Learners, Examined

## A Patient Becomes a Point

The sociologist Adrian Mackenzie spent years inside machine learning, reading its textbooks, taking its online courses and running its code, to ask what kind of knowledge it produces. His book *Machine Learners: Archaeology of a Data Practice* (2017) spends many pages on the very textbook our heart data comes from. He notes how it mixes worlds: "Maps of New Zealand fishing patterns lie next to plots of factors in South African heart disease." To a classifier, men, fish, penguins and emails are all the same thing: rows of numbers.

The first move is turning each man into a point. Mackenzie calls the space those points live in a **vector space**: "Every distinct column in a table adds a new dimension to the vector space." Our patients are points in a four-dimensional space. Even family history, a story about parents and grandparents, became a column of 0s and 1s so that it could be measured with a ruler. About this kind of coding, Mackenzie writes: "Complex natures become simple natures."

Then comes kNN's one big assumption. Mackenzie states it plainly:

> "The assumption here, as in nearly all machine learners transforming the vector space, is that proximity in vector space implies similarity in class or grouping."

*You are like your neighbors.* But "neighbor" was built by us: which four columns went in (and which five stayed out), and the standardizing that decided how much a year of age weighs against a kilogram of tobacco. Change those choices and a patient gets different neighbors, and a different prediction.

## Accurate but Unstable

kNN is old. Mackenzie traces it to a 1951 paper by the statisticians Evelyn Fix and Joseph Hodges, who wanted a way to classify cases that would work "even if no parametric form can be assumed," that is, without assuming anything about the shape of the data. That's kNN's appeal: no equations to fit, just neighbors. He quotes the textbook's verdict on the trade-off:

> "The method of k-nearest neighbors makes very mild structural assumptions: its predictions are often accurate but can be unstable."

We saw the instability on page 2 (one patient, three values of k, two different answers) and on page 4 (one model, seven splits, seven scores). Mackenzie's most striking example comes from genomics. In a large project where 36 research teams built classifiers to tell "normal" from "disease" samples, almost half of the 19,779 models submitted were kNN, and they "varied greatly in their predictions." One team, trying to tame the variation, wrote that they

> "systematically generated 463,320 k-nn [k-nearest neighbor] models by varying feature ranking method, number of features, distance metric, number of neighbors, vote weighting and decision threshold."

Every item on that list is a choice you met in this reading: which features, how many, how to measure distance, which k, and where to set the vote threshold. Each choice moves the score. A single reported number hides all the other numbers that a slightly different set of choices would have produced.

## The Test Set as an Examination

Why go to so much trouble to hold out a test set? Because, as Mackenzie puts it, "training errors … are not always a good guide to test generalization error." That's the 100% / 64.7% gap of page 3.

But Mackenzie also notices what the test set *does* socially. On competition platforms like Kaggle, teams get labeled training data and unlabeled test data, submit predictions, and are ranked on a public leaderboard by their test error, a scene the platform itself describes as "the joys of regularization and the agony of overfitting." Mackenzie compares this to what the philosopher Michel Foucault called the **examination**: a ritual that sets a problem, scores everyone the same way, and ranks them. "The learning of machine learning," he writes, "takes place in examinations that rank both human and nonhuman machine learners according to error rates."

An exam measures what it asks. A test set can only ask: *does the model agree with the labels in data like this?* It cannot ask whether the labels were the right ones, or whether data like this resembles the world where the model will be used.

## What Is in This Table?

The heart data has its own fine print. Its official description reads: "A retrospective sample of males in a heart-disease high-risk region of the Western Cape, South Africa. There are roughly two controls per case of CHD. Many of the CHD positive men have undergone blood pressure reduction treatment and other programs to reduce their risk factors after their CHD event. In some cases the measurements were made after these treatments."

Each sentence changes how to read our scores:

- **"Males."** Nothing in this table speaks for women.
- **"A high-risk region"**, around 1980. A test split from this table inherits the same place and time, so a good test score says nothing about a clinic elsewhere today.
- **"Two controls per case."** The researchers chose about two healthy men for every sick one. The 34.6% CHD rate is a *design choice*, not the real rate. Precision depends on it: in a clinic where 10% of patients have CHD, a model with our recall (0.39) and false-alarm rate (5 of 90) would flag about 39 sick men and 50 healthy ones per 1,000 patients, so its precision would fall from 0.79 to about **0.44**.
- **"Measured after treatment."** Some of the sick men's numbers were changed *by* their diagnosis; for example, their blood pressure was lowered by the treatment it led to. A model can learn patterns that point backward, from the disease to the measurement.

None of this shows up in the confusion matrix. Every one of our test patients was split off from the same table, so the test set has the same blind spots as the training set.

Mackenzie's conclusion fits the whole week: "Machine learners, as we have seen, vary too much: they are biased, they overfit, they underfit, and they often fail to generalize."

## Questions Worth Asking About Any Classifier

- **What makes two cases "neighbors"?** Which columns went in, and on what ruler?
- **What does it score on cases it has never seen,** and how much does that move from split to split?
- **Compared with what?** Is the accuracy better than the lazy model's?
- **Which mistakes does it make, and who pays for them?** Precision, recall, and where the threshold sits.
- **Where did the labels and the rows come from?** A test set can't see outside the table it was split from.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Mackenzie writes that kNN assumes "proximity in vector space implies similarity in class." Which choice made by the data scientist most directly changes who counts as "proximate"?**

- [x] Which columns are used as features and how they are scaled before distances are measured.
- [ ] The name given to the label column.
- [ ] Whether the predictions are printed as 0/1 or as words.
- [ ] The number of rows shown by `.head()`.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

If a model scores well on a test set that was randomly split from a dataset, we can be confident it will score just as well on data collected in a different place or time.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**A dataset was built with two healthy people for every sick person, so 33% of rows are "sick." A model is then used in a clinic where only 5% of patients are sick. If its recall and false-alarm rate stay the same, what happens to its precision?**

- [x] It goes down: with many more healthy patients, the same false-alarm rate produces many more false positives for each true positive.
- [ ] It goes up, because there are fewer sick people to find.
- [ ] It stays the same, because precision doesn't depend on how common the disease is.
- [ ] It becomes exactly 5%.

<!-- END QUESTION -->
