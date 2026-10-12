---
layout: week
title: "Week 7: Decision trees and hyperparameter tuning"
week_number: 7
---

# Twenty Questions: Decision Trees

## Who Earned Over $50,000?

In 1994, the U.S. Census Bureau's monthly household survey asked tens of thousands of Americans about their work, schooling and family, and how much they earned in the past year. Two researchers, Barry Becker and Ronny Kohavi, pulled about 49,000 of those records into a file and posed one question: *from a person's other answers, can a computer tell whether they earned more than $50,000 a year?* (In 1994 that was a high income; in today's dollars it is more than twice as much.) Their file became one of the most used datasets in machine learning.

We'll use a random sample of 2,000 people from it.

**📥 Download the dataset: [income.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/income.csv)**

```python
import pandas as pd

income = pd.read_csv("income.csv")
income[["age", "education", "education_level", "hours_per_week", "married", "high_income"]].head(3)
```

| age | education | education_level | hours_per_week | married | high_income |
|---:|:---|---:|---:|---:|---:|
| 62 | 7th-8th | 4 | 66 | 0 | 0 |
| 18 | 11th | 7 | 25 | 0 | 0 |
| 25 | Bachelors | 13 | 50 | 0 | 1 |

**What is one row about?** One person, as they answered the survey in 1994. We'll use four features and the label:

| Column | What it measures |
|:---|:---|
| `age` | age in years |
| `education_level` | highest schooling, as a code from 1 to 16: 9 = high-school graduate, 10 = some college, 11–12 = associate degree, 13 = bachelor's, 14 = master's, 15 = professional school, 16 = doctorate |
| `hours_per_week` | usual hours worked per week |
| `married` | 1 = married and living with a spouse, 0 = anything else (single, divorced, widowed, separated) |
| `high_income` | **the label: 1 = earned more than $50,000, 0 = did not** |

466 of the 2,000 people (23.3%) have `high_income = 1`. A lazy model that says *no* to everyone is right 76.7% of the time, so that is the score to beat.

![Two scatter plots of age (17 to 90) across and education level (1 to 16) up. Blue circles are people who earned $50,000 or less; orange triangles earned more. Left, "Not married (1,079 people)": almost all blue, with a few orange triangles, mostly at education levels 13 and above. Right, "Married (921 people)": many more orange triangles, crowded at education levels 13 to 16 and ages 30 to 60; at levels 9 and 10 blue and orange are mixed.](images/income_scatter.png)

The two panels already look different: orange is rare among the unmarried and common among married people with more schooling.

## A Tree Is a List of Questions

Think of the game *twenty questions*. You don't guess at random; you ask the question that splits the possibilities best, then pick your next question based on the answer. A **decision tree** plays this game with the data:

1. Ask a yes/no question about one feature, like *"is `education_level` at most 10?"*
2. Each answer sends a person down a different **branch**, where the tree can ask a new question.
3. When the questions stop, the person lands in a **leaf**. The prediction is the majority label of the training people in that leaf.

Each question looks at **one column at a time** and compares it with a cutoff. That means trees need no scaling: "age at most 33" means the same thing whether age is in years or months. (Compare kNN in Reading 5, where every column had to share one ruler.)

## How the Tree Picks a Question: Gini

We first set aside 30% of the people as a test set, exactly as in Reading 5. The 1,400 training people are the only ones the tree gets to see:

```python
from sklearn.model_selection import train_test_split

X = income[["age", "education_level", "hours_per_week", "married"]]
y = income["high_income"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```

A good question leaves each branch **less mixed** than before. Trees measure "mixed" with the **Gini impurity**. With two labels, if a share `p` of the people in a box are high-income:

> **Gini = 2 × p × (1 − p)**

It is **0** when a box holds only one label (pure), and **0.5** when it is half and half (as mixed as it gets).

Before any question, 333 of the 1,400 training people are high-income: p = 0.238, Gini = 2 × 0.238 × 0.762 = **0.363**. Now try the question *"married?"*:

| branch | people | high-income | p | Gini |
|:---|---:|---:|---:|---:|
| not married | 743 | 54 | 0.073 | 0.135 |
| married | 657 | 279 | 0.425 | 0.489 |

The unmarried branch is much purer than before; the married branch is more mixed. Weighted by size, the average is (743 × 0.135 + 657 × 0.489) / 1,400 = **0.301**, down from 0.363. The computer tries **every cutoff of every feature** and keeps the question with the lowest weighted Gini:

| best question on… | weighted Gini after it |
|:---|---:|
| **married?** | **0.301** |
| education level at most 10? | 0.327 |
| age at most 33? | 0.329 |
| hours per week at most 48? | 0.341 |

So "married?" becomes the first question. But notice: 42.5% is still under half, so **both** branches predict "$50,000 or less." A tree with this one question predicts *no* for everyone and scores exactly as well as the lazy model. The question made the groups purer; it didn't yet change a single prediction.

## A Tree of Depth 2

Let each branch ask one more question. `max_depth=2` means at most two questions per person:

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

tree2 = DecisionTreeClassifier(max_depth=2, random_state=0)
tree2.fit(X_train, y_train)
plot_tree(tree2, feature_names=X.columns, class_names=["≤50K", ">50K"])
```

![A decision tree with three questions and four leaves. The top box: "married <= 0.5, gini = 0.363, samples = 1400, value = [1067, 333], class = ≤50K". True (not married) goes left to "education_level <= 13.5, gini = 0.135, samples = 743, value = [689, 54]", which splits into a leaf of 698 people (661 low, 37 high) and a leaf of 45 people (28 low, 17 high), both predicting ≤50K. False (married) goes right to "education_level <= 10.5, gini = 0.489, samples = 657, value = [378, 279]", which splits into a leaf of 407 people (287 low, 120 high) predicting ≤50K, and a leaf of 250 people (91 low, 159 high), the only orange box, predicting >50K. Blue boxes predict ≤50K and orange boxes >50K; darker boxes are purer.](images/income_tree_depth2.png)

How to read a box (a **node**):

| line | means |
|:---|:---|
| first line (here: married ≤ 0.5) | the **question**: true → go left, false → go right |
| `samples` | how many training people reach this box |
| `value` | how many of them are [$50K or less, over $50K] |
| `class` | the majority, which is the **prediction** if the questions stop here |
| `gini` | how mixed the box is |

The whole tree fits on an index card:

> **Married, *and* education level above 10.5 (an associate degree or more) → over $50,000. Everyone else → $50,000 or less.**

Follow two people down it:

- **Married, age 45, education level 12:** married → right; 12 > 10.5 → right → **over $50,000.**
- **Not married, age 50, doctorate (16):** not married → left; 16 > 13.5 → right → a leaf of 45 people, 17 of them high-income → **$50,000 or less.** Even a doctorate doesn't flip the prediction for an unmarried person in this tree.

```python
from sklearn.metrics import accuracy_score

accuracy_score(y_train, tree2.predict(X_train)), accuracy_score(y_test, tree2.predict(X_test))
# (0.811, 0.833)
```

81.1% on the training people and 83.3% on the 600 test people, against the lazy model's 77.8% on the same test people.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**A node in a tree shows `samples = 250, value = [91, 159], class = >50K`. What does it mean?**

- [x] 250 training people reached this box; 91 earned $50,000 or less and 159 earned more, so the box predicts "over $50,000."
- [ ] The tree is 250 levels deep.
- [ ] 159 of the 250 predictions in this box were wrong.
- [ ] The box will ask 91 more questions before it predicts.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

With two labels, Gini impurity is 2 × p × (1 − p). A box where every person has the same label has Gini **[0]**. A box that is exactly half and half has Gini **[0.5]**.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Like kNN, a decision tree needs its features standardized first, because a feature measured in bigger units would otherwise dominate.

<!-- END QUESTION -->

# How Many Questions? Depth and Overfitting

## Growing Without a Limit

`max_depth` is a **hyperparameter**: a knob we set before fitting. What if we remove the limit? Then the tree keeps asking questions until every leaf is pure or no question can split it any more:

```python
tree_full = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)    # no max_depth
tree_full.get_depth(), tree_full.get_n_leaves()                            # (19, 370)
```

**19 questions deep, 370 leaves for 1,400 people.** 155 of those leaves hold a **single person**. The tree has carved out a private rule for each of them. One reads: *not married, 36 or younger, education level 13 or less, works more than 89.5 hours a week → over $50,000.* Exactly one training person fits it: a 31-year-old high-school graduate who reported working 99 hours a week.

| | training people | test people |
|:---|---:|---:|
| depth 2 | 81.1% | **83.3%** |
| no limit | **95.2%** | 77.5% |

The full tree is nearly perfect on people it has seen and *below the lazy model* (77.8%) on people it hasn't. (It can't reach 100% even in training: 180 training people share the exact same four answers with someone whose income was different, and no question about these four features can tell them apart.)

## The Depth Curve

Score every depth on both sets:

```python
for depth in range(1, 20):
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    print(depth, accuracy_score(y_train, tree.predict(X_train)), accuracy_score(y_test, tree.predict(X_test)))
```

![Line chart of accuracy against max_depth from 1 to 19 (19 is no limit). Training accuracy (solid blue) starts at 76.2% at depth 1, rises to 81.1% at depth 2 and then climbs steadily to 95.2% at depth 17 and beyond. Test accuracy (dashed orange) starts at 77.8% at depth 1, peaks at 83.3% at depths 2 and 3, then drifts down to about 78% from depth 10 on, close to a dotted gray line at 77.8% for the lazy model on the test people.](images/income_depth_curve.png)

- **Depth 1:** one question that changes no prediction. Poor on both sets → **underfitting**.
- **Depths 2–3:** the best test scores.
- **Deeper:** the training score keeps climbing, the test score sinks. The growing gap means the tree is memorizing → **overfitting**.

It's the same table as in Reading 5:

| | on data it learned from | on new data |
|:---|:---|:---|
| **Overfitting**: too flexible | great | worse |
| **Underfitting**: too simple | poor | poor |
| **Good fit** | good | good |

But the knob turns the other way. For kNN, a **small** `k` overfit. For a tree, a **large** `max_depth` overfits: more questions, more flexibility.

## Rectangles

Every question cuts along one feature, so a tree carves the feature space into **rectangles**, one per leaf. With only two features (age and education level), we can draw them:

![Three maps with age across and education level up; the background shows each tree's prediction, blue for $50,000 or less and orange for more, with training people as dots. Left, "max_depth=1 (2 leaves)": all blue. Middle, "max_depth=3 (8 leaves)": all blue except one orange rectangle across the top, for people older than about 30 with education level 15 or 16. Right, "no limit (244 leaves)": a patchwork of small orange rectangles scattered across the middle and even near the bottom, many drawn around a single orange triangle.](images/income_maps.png)

The no-limit map has orange slivers around single people, including a few around people with only a 7th–8th-grade education. Those slivers fit the **noise**: the accidents of who happened to land in this sample.

## Pruning

Two ways to keep a tree from memorizing:

| | idea | in scikit-learn |
|:---|:---|:---|
| **Pre-pruning** | stop growing early | `max_depth`; `min_samples_leaf` (every leaf must hold at least this many people); `min_samples_split` |
| **Post-pruning** | grow the full tree, then cut back the branches that help least | `ccp_alpha`: bigger means cut more |

```python
DecisionTreeClassifier(min_samples_leaf=50, random_state=0)    # 19 leaves; test 83.2%
DecisionTreeClassifier(ccp_alpha=0.005, random_state=0)        # cut back to 4 leaves; test 83.3%
```

Both shrink the 370-leaf tree and bring the test score back up. But notice how we judged them: by looking at the **test** score. That is a problem, and the rest of this reading is about fixing it.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**A tree scores 97% on its training data and 74% on its test data. Which change is most likely to help?**

- [x] Limit its growth, for example with a smaller `max_depth` or a larger `min_samples_leaf`.
- [ ] Remove the depth limit so it can ask more questions.
- [ ] Standardize the features before fitting.
- [ ] Use the test data for training as well.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

A tree with a very *[large]* `max_depth` can give single people their own leaves, so it is *[overfitting]*. A tree with `max_depth=1` asks only one question and is *[underfitting]*. For kNN the knob ran the opposite way: a very *[small]* k overfit.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

Setting `min_samples_leaf=50` guarantees that no leaf of the tree is based on fewer than 50 training people.

<!-- END QUESTION -->

# One Test Set Can't Choose

## Five Splits, Five Answers

Which depth is best? The depth curve said 2 or 3. But that curve came from **one** random split. Here is the test accuracy of each depth on five different splits of the same 2,000 people:

| random_state | depth 1 | depth 2 | depth 3 | depth 4 | depth 5 | depth 6 |
|:---|---:|---:|---:|---:|---:|---:|
| 42 | 77.8% | **83.3%** | **83.3%** | 81.2% | 81.5% | 80.7% |
| 1 | 76.7% | **82.2%** | **82.2%** | **82.2%** | 81.7% | 80.0% |
| 7 | 74.8% | 79.0% | 79.3% | **80.3%** | 78.0% | 78.0% |
| 15 | 79.3% | 81.3% | 81.7% | **82.3%** | 82.2% | 80.3% |
| 24 | 77.8% | 82.7% | **83.0%** | **83.0%** | 82.8% | 81.7% |

The "best" depth moves between 2, 3 and 4 depending on the shuffle, and depth 2 alone scores anywhere from 79.0% to 83.3%. Two problems:

1. **Luck.** One test set of 600 people is a noisy judge. A difference of 0.5 points is three people.
2. **Peeking.** If the test set picks the depth, it has become part of building the model. Its score is no longer a fair picture of new people. Reading 5 met this already, when kNN's test curve peaked at k = 91 and it was tempting to pick it.

**The fix:** keep the test set **locked** until the very end. Do all the choosing *inside* the training set, and do it many times so that luck averages out.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**A student tries 20 depths, keeps the one with the highest test accuracy (85%), and reports "my model is 85% accurate on new data." What is wrong?**

- [x] The test set was used to choose the depth, so 85% is the best of 20 tries on that test set and is likely too optimistic for truly new data.
- [ ] Nothing; the test set was never used for fitting, so its score is fair.
- [ ] Depth can only be chosen by looking at the training accuracy.
- [ ] 20 depths is too few to find the best one.

<!-- END QUESTION -->

# Cross-Validation: Everyone Takes a Turn

## The Recipe

**k-fold cross-validation** makes many small "test sets" out of the training set alone. With 5 folds:

1. Cut the 1,400 training people into 5 groups of 280: the **folds**.
2. **Round 1:** fit a tree on folds 2–5, score it on fold 1. **Round 2:** fit on folds 1, 3, 4, 5, score on fold 2. And so on, five times.
3. Every training person is scored **exactly once**, by a tree that never saw them.
4. The **mean** of the 5 scores is the **cross-validation score**.

(The fold scored in each round is often called the **validation** fold, to keep the word "test" for the locked set.)

![Diagram of 5-fold cross-validation. Five rows, one per round. Each row has five boxes labeled fold 1 to fold 5 (280 people each); in round 1 fold 1 is orange ("validate") and the rest blue ("fit"), in round 2 fold 2 is orange, and so on down the diagonal. The rounds score 0.821, 0.807, 0.779, 0.861 and 0.782, and their mean is 0.810. A gray box on the right of every row, "test: locked", holds the 600 test people.](images/income_cv_folds.png)

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(DecisionTreeClassifier(max_depth=2, random_state=0), X_train, y_train, cv=5)
scores, scores.mean()
# array([0.821, 0.807, 0.779, 0.861, 0.782]), 0.810
```

One call fit **5 trees**. The five scores range from 77.9% to 86.1%, the same split-to-split luck as the last page, but now we use all five and average them. And the 600 test people were never touched.

(With `cv` equal to the number of rows, every fold holds a single person: that is **leave-one-out** cross-validation. More folds cost more fits.)

## Choosing the Depth

One cross-validation score per depth, all from the training people only:

```python
for depth in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None]:
    scores = cross_val_score(DecisionTreeClassifier(max_depth=depth, random_state=0), X_train, y_train, cv=5)
    print(depth, scores.mean(), scores.std())
```

![Line chart of 5-fold cross-validation accuracy against max_depth from 1 to 12 and "no limit", with error bars showing the spread of the five rounds. Depth 1 scores 76.2%, exactly on a dotted line for the lazy model. Depth 2 jumps to 81.0%, depth 3 to 81.2%, and depth 4 is the best at 81.9%. From there the scores fall: 79.7% at depth 5, 76.7–78.5% for depths 7 to 12, and 75.9% with no limit, just below the lazy line. The error bars of depths 2, 3 and 4 overlap heavily.](images/income_cv_curve.png)

The same story as the test curve, but told by 1,400 people taking turns instead of one locked set: depth 1 underfits, deep trees overfit, and the best is **depth 4 (81.9%)**, with depths 2 and 3 just behind.

Only now, **once**, open the test set:

```python
final = DecisionTreeClassifier(max_depth=4, random_state=0).fit(X_train, y_train)   # all 1,400
accuracy_score(y_test, final.predict(X_test))       # 0.812
```

81.2%. Lower than the 83.3% depth 2 scored on page 2, and that's fine: depth 2 *looked* better on this test set, but we only know that because we peeked. 81.2% is the number we can report honestly, because the test set chose nothing.

The same tool settles Reading 5's question about kNN's `k`: score each `k` by cross-validation instead of by the test set. (For kNN the scaler must also be re-fit inside each fold; scikit-learn's `Pipeline` does that, and we'll meet it later.)

📌 **One split:** 81.2% is the score on *these* 600 test people.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

A training set has 1,000 rows. With `cv=10`, each fold holds **[100]** rows, and `cross_val_score` fits **[10]** models.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

In 5-fold cross-validation, the test set is cut into 5 folds, and each fold takes a turn as the training data.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Why is a cross-validation score more trustworthy than a single validation split for choosing `max_depth`?**

- [x] Every training row gets scored once by a model that never saw it, and averaging five rounds smooths out the luck of any one split.
- [ ] Cross-validation uses the test set five times, so it sees more data.
- [ ] Cross-validation always gives a higher score.
- [ ] Cross-validation removes the need for a test set.

<!-- END QUESTION -->

# Grid Search: Tuning Several Knobs

## Parameters and Hyperparameters

Two kinds of numbers make up a tree:

- **Parameters** are *learned* from the data by `fit`: which feature each question asks about, and its cutoff (`married <= 0.5`, `education_level <= 10.5`).
- **Hyperparameters** are *set by us* before `fit`: `max_depth`, `min_samples_leaf`, `ccp_alpha`. Choosing them is called **tuning**.

## Every Combination

A tree has several knobs, and they interact: a deep tree with large leaves can behave like a shallow one. **Grid search** lists values for each knob and cross-validates **every combination**:

```python
from sklearn.model_selection import GridSearchCV

grid = {"max_depth": [1, 2, 3, 4, 5, 6, 8, None],
        "min_samples_leaf": [1, 5, 10, 20, 50]}

search = GridSearchCV(DecisionTreeClassifier(random_state=0), grid, cv=5)
search.fit(X_train, y_train)                 # training people only
search.best_params_, search.best_score_      # ({'max_depth': 4, 'min_samples_leaf': 5}, 0.819)
```

8 depths × 5 leaf sizes = **40 combinations**, each cross-validated with 5 folds: **200 trees**, plus one final refit of the winner on all 1,400 training people. Here are all 40 cross-validation scores:

| `min_samples_leaf` ↓ / `max_depth` → | 1 | 2 | 3 | 4 | 5 | 6 | 8 | no limit |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | .762 | .810 | .812 | .819 | .797 | .787 | .785 | .759 |
| 5 | .762 | .810 | .812 | **.819** | .797 | .796 | .786 | .784 |
| 10 | .762 | .810 | .809 | .813 | .798 | .801 | .804 | .802 |
| 20 | .762 | .811 | .810 | .812 | .804 | .798 | .797 | .799 |
| 50 | .762 | .811 | .810 | .809 | .810 | .814 | .814 | .814 |

Look at the bottom row: with leaves of at least 50 people, even "no limit" scores 81.4%, because the leaf rule stops the tree before it memorizes. The two knobs can do each other's job.

## The Best of Many

The winner (depth 4, leaves of at least 5) scored 81.9%. Many cells are within one point of it: depth 2, for instance, scores 81.0–81.1%. That gap is about **12 people out of 1,400**. The winner has 15 leaves; depth 2 has 4.

Open the test set once more, for both:

| | cross-validation | test |
|:---|---:|---:|
| grid winner (depth 4, leaf 5) | 81.9% | 81.5% |
| depth 2 | 81.0% | 83.3% |

The winner did not win on new people. Part of being the best of 40 was luck in these particular folds, so **the best of many scores is optimistic**. The more combinations you try, the more chances one has to be lucky.

A reasonable rule, decided *before* looking at the test set: **when scores are within a person or two of each other, prefer the simpler model.** Here that would have picked depth 2, for a reason we could defend without peeking.

The Adult dataset's own documentation shows the same scene at the scale of a whole field. Next to the data, its README lists the error rates of 16 algorithms, all run on one fixed test split: from 14.05% to 21.42%, plus a 17th that "Crashed. Unknown why." Every row is one entry in a contest. A ranking of many entries on one test set is still one split, and the top entry was partly lucky.

📌 **One split:** 81.5% and 83.3% are scores on *these* 600 people. Page 3 showed how much another shuffle can move them.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

A grid search tries `max_depth` in [2, 4, 6] and `min_samples_leaf` in [1, 10] with `cv=5`. It cross-validates **[6]** combinations and fits **[30]** trees before the final refit.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Which of these is a *parameter* (learned by `fit`) rather than a *hyperparameter*?**

- [x] The cutoff 10.5 in the question `education_level <= 10.5`.
- [ ] `max_depth=4`.
- [ ] `min_samples_leaf=5`.
- [ ] `cv=5`.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**`GridSearchCV` reports a `best_score_` of 0.819 after trying 40 combinations. Why might the winner score lower on the locked test set?**

- [x] Picking the highest of 40 cross-validation scores favors a combination that was partly lucky on these folds, so the best score tends to be optimistic.
- [ ] `GridSearchCV` trains on the test set, so the test score must be lower.
- [ ] Cross-validation scores are always higher than test scores by about 4 points.
- [ ] The final refit uses fewer training rows than cross-validation did.

<!-- END QUESTION -->

# Trees, Examined

## A Model You Can Read

The sociologist Adrian Mackenzie (whose book *Machine Learners* appeared in Reading 5) gives decision trees a chapter of their own. He starts with their appeal: "Decision trees promise an understanding of machine learning." Our depth-2 tree fits on an index card. Few models in this course will be that easy to read.

He also names the price: "The cost of decision tree comprehensibility, however, is a certain highly restricted framing of differences." He quotes the textbook *Elements of Statistical Learning*: tree methods "partition the feature space into a set of rectangles." Every person who lands in the same rectangle gets the same answer, and every border is a sharp line: education level 10 and 11 are treated as different worlds, 10 and 9 as the same.

## Sorting People Since 1963

Trees were born, Mackenzie shows, in the social sciences. In the early 1960s, James Morgan and John Sonquist at the University of Michigan's Institute for Social Research wrote a program called AID (*Automatic Interaction Detector*) to search large social surveys for patterns. Its uses spread quickly, to "education, politics, economics, population control, advertising, mass media, and family planning." A tree Mackenzie reprints from their 1963 paper sorts people's **annual earnings**, splitting on race, education and whether the person was a farmer.

Thirty years later, the Census survey behind our data asked similar questions, and our tree's first two cuts were marriage and education.

Critics came soon. In 1972, the statistician Hillel Einhorn warned:

> "The purely empirical approach is particularly dangerous in an age when computers and packaged programs are readily available, since there is temptation to substitute immediate empirical analysis for more analytic thought and theory building."

AID's power was its problem, he wrote: "it may make sense out of 'noise'." Our 370-leaf tree did exactly that: 155 private rules for 155 single people.

## "Quite a Different Tree Occurs"

In 1973, the marketing researcher Peter Doyle raised a second objection: trees are **arbitrary**.

> "a second variable may be almost as discriminating as the one chosen, but if the program is made to split on this, quite a different tree occurs."

Our data shows both sides of this. With `married` available, "married?" wins the first question by a wide margin (Gini 0.301 against 0.327 for the runner-up), and in all five splits on page 3 the tree asked it first. But **drop `married`**, and the top two candidates, education and age, are almost tied. Grow a depth-2 tree on eight different random splits of the same 2,000 people: six open with an education question, two open with **age**, and one of those then asks about **hours worked**. Same people, same recipe, a different story about who earns more.

The *Elements of Statistical Learning*, as Mackenzie quotes it, says it plainly: "One major problem with trees is their high variance. Often a small change in the data can result in a different series of splits, making interpretation somewhat precarious." Mackenzie's verdict: "The diagrammatic form that allows decision trees to be observed and interpreted is also the source of their instability." A tree is easy to read; that doesn't make what it says stable.

## Learning When to Stop

How did trees survive their critics? Mackenzie's answer is this week's whole topic: "much of the development of decision trees did not revolve around how to construct them but how to limit their growth." The *Elements* states the problem in words you could now write yourself:

> "How large should we grow the tree? Clearly a very large tree might overfit the data, while a small tree might not capture the important structure. Tree size is a tuning parameter governing the model's complexity, and the optimal tree size should be adaptively chosen from the data."

"Adaptively chosen from the data" means pruning, cross-validation and grid search. These tools answer Einhorn's worry about noise. They don't answer Doyle's: a well-tuned tree can still tell a different story on a slightly different sample.

## What the Questions Sort

Our tree never sees anyone's sex; `sex` isn't one of its features. But look at who answers its first question:

| | women | men |
|:---|---:|---:|
| not married (1,079) | 560 | 519 |
| married (921) | **99** | **822** |

In this file, 89% of the married people are men. So "married?" also splits a group that is mostly men from one that is about half women, and men here are much more often high-income (29.0% against 11.7% for women). A question that isn't *about* sex can still sort by it. (Why are so few married women in the file? That's a question about how the file was built, and it's worth asking before trusting any rule learned from it.)

Mackenzie ends with a question of his own: "Decision trees have been heavily used in credit risk assessment as well as many biomedical models. Does their popularity stem from the legibility of the statements they produce, even if those patterns prove unstable?"

## Questions Worth Asking About Any Tree

- **How deep is it, and who chose?** Was its size chosen by cross-validation, or by peeking at the test set?
- **How many tries came before the winner?** The best of many is optimistic.
- **Would a slightly different sample grow the same questions?** If the runner-up feature was close, maybe not.
- **What do its questions stand in for?** A feature can carry information the model was never given directly.
- **Readable for whom?** A rule anyone can read is easier to question. It isn't automatically right.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Doyle wrote that "a second variable may be almost as discriminating as the one chosen, but if the program is made to split on this, quite a different tree occurs." What does this warn about?**

- [x] Trees can be unstable: when two questions are nearly tied, a small change in the data can swap them and change everything below.
- [ ] Trees can only use two variables.
- [ ] Trees always choose the wrong first question.
- [ ] Trees need scaled features to choose questions correctly.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Because a decision tree can be read as a list of rules, the rules it learns are guaranteed to stay the same if it is trained on a different sample from the same population.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Our tree does not use `sex` as a feature, yet its first question ("married?") splits a group that is 89% men from one that is about half women. What does this show?**

- [x] A feature can act as a stand-in for information the model was never given, so leaving a column out doesn't guarantee the model ignores it.
- [ ] The tree must have secretly used the `sex` column.
- [ ] Marital status is a meaningless feature and should always be removed.
- [ ] This only happens with decision trees, never with other models.

<!-- END QUESTION -->
