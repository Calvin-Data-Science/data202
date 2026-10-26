# DATA 202 --- Quiz 4

Week 9 --- Covering Weeks 6--7: kNN, Metrics, Trees & Cross-Validation

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 4`, which
generates `quiz04_A.pdf` and `quiz04_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: Campus Library

The campus library keeps four related tables (simulated data). Every question
on this quiz uses them.

- `loans` --- one row per book loan: `loan_id`, the `student_id` who borrowed
  it, the `book_id` borrowed, and `late` (**the label**: 1 = returned late,
  0 = on time). There are 800 loans.
- `students` --- one row per student: `student_id`, `class_year` (1--4) and
  `prior_late` (how many books they returned late last year).
- `books` --- one row per book: `book_id`, `genre` and `pages`.
- `monthly_loans` --- one row per student: how many books they borrowed in
  each month (`sep`, `oct`, `nov`).

The models in Questions 1--6 predict `late` from `pages`, `prior_late` and
`class_year` (found by joining `loans` to `students` and `books`).

**A few rows of `loans`:**

**Version A sample rows:**

| loan_id | student_id | book_id | late |
|---|---|---|---|
| L101 | S011 | B204 | 0 |
| L102 | S012 | B087 | 1 |
| L103 | S012 | B150 | 0 |
| L104 | S015 | B204 | 1 |

**Version A** -- **A few rows of `students`:**

| student_id | class_year | prior_late |
|---|---|---|
| S011 | 2 | 0 |
| S012 | 4 | 3 |
| S013 | 1 | 1 |

**Version B sample rows:**

| loan_id | student_id | book_id | late |
|---|---|---|---|
| L201 | S021 | B033 | 1 |
| L202 | S023 | B118 | 0 |
| L203 | S024 | B033 | 0 |
| L204 | S024 | B301 | 1 |

**Version B** -- **A few rows of `students`:**

| student_id | class_year | prior_late |
|---|---|---|
| S022 | 3 | 0 |
| S023 | 1 | 2 |
| S024 | 2 | 4 |

## Question 1 (SLO 06A)

**Version A:**

Distances from the new loan: 1 (late), 1.41, 2, 2.24 (three on time), 2.83 (late), 3 (on time), 4.24 (late).

- **k = 1: late** (the single nearest loan was late).
- **k = 5: on time** (the 5 nearest: 3 on time, 2 late).
- **k = 1 is more likely to overfit**: it follows single training points (noise), so it is perfect on the data it learned from but less reliable on new loans.

**Version B:**

Distances from the new loan: 1 (late), 1.41, 2, 2.24 (three on time), 2.83 (late), 3 (on time), 4.24 (late).

- **k = 1: late** (the single nearest loan was late).
- **k = 5: on time** (the 5 nearest: 3 on time, 2 late).
- **k = 1 is more likely to overfit**: it follows single training points (noise), so it is perfect on the data it learned from but less reliable on new loans.

## Question 2 (SLO 06B)

**Version A:**

| Metric | Fraction | Value |
|---|---|---|
| Accuracy | (132 + 22) / 200 | 0.770 |
| Precision (late) | 22 / (22 + 15) = 22/37 | 0.595 |
| Recall (late) | 22 / (22 + 31) = 22/53 | 0.415 |
| Lazy model | 147 / 200 | 0.735 |

Accuracy 77.0% beats the lazy model's 73.5% only a little, and recall shows the model catches fewer than half of the late loans.

**Version B:**

| Metric | Fraction | Value |
|---|---|---|
| Accuracy | (134 + 20) / 200 | 0.770 |
| Precision (late) | 20 / (20 + 13) = 20/33 | 0.606 |
| Recall (late) | 20 / (20 + 33) = 20/53 | 0.377 |
| Lazy model | 147 / 200 | 0.735 |

Accuracy 77.0% beats the lazy model's 73.5% only a little, and recall shows the model catches fewer than half of the late loans.

## Question 3 (SLO 06C)

**Version A:**

```python
X = data[["pages", "prior_late", "class_year"]]
y = data["late"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=1)
scaler = StandardScaler().fit(X_train)
knn = KNeighborsClassifier(n_neighbors=5).fit(scaler.transform(X_train), y_train)
knn.score(scaler.transform(X_test), y_test)   # accuracy on NEW loans
```

Test set: **200** loans (800 × 0.25).

The scaler and the model are fit on the training rows only; the test rows are used only to score, playing the part of new loans.

**Version B:**

```python
X = data[["pages", "prior_late", "class_year"]]
y = data["late"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1)
scaler = StandardScaler().fit(X_train)
knn = KNeighborsClassifier(n_neighbors=5).fit(scaler.transform(X_train), y_train)
knn.score(scaler.transform(X_test), y_test)   # accuracy on NEW loans
```

Test set: **160** loans (800 × 0.2).

The scaler and the model are fit on the training rows only; the test rows are used only to score, playing the part of new loans.

## Question 4 (SLO 07A)

**Version A:**

| prior_late | pages | class_year | prediction |
|---|---|---|---|
| 0 | 600 | 2 | **late** |
| 3 | 200 | 1 | **on time** |
| 2 | 400 | 4 | **late** |

`class_year` is never asked by this tree, so it doesn't matter. Each loan follows one path from the top question to a leaf.

**Version B:**

| prior_late | pages | class_year | prediction |
|---|---|---|---|
| 1 | 300 | 3 | **on time** |
| 4 | 320 | 2 | **late** |
| 2 | 250 | 1 | **on time** |

`class_year` is never asked by this tree, so it doesn't matter. Each loan follows one path from the top question to a leaf.

## Question 5 (SLO 07B)

**Version A:**

**max_depth = 2** (best CV score, 0.770; depth 3 is about the same). **Underfits:** depth 1 (poor on both rows, 0.735 / 0.718). **Overfits:** no limit (0.935 on the folds it learned from but only 0.710 held out; depths 6 and 8 too). The growing gap between the rows is the sign of overfitting.

**Version B:**

**max_depth = 2** (best CV score, 0.770). The training score keeps rising to 0.935 with no limit because a deep tree memorizes the folds it was fit on; on held-out folds it falls to 0.710 (overfitting). **Underfits:** depth 1 (poor on both rows).

## Question 6 (SLO 07C)

**Version A:**

```python
grid = {"max_depth": [2, 4, 6, None],
 "min_samples_leaf": [1, 10, 30]}
search = GridSearchCV(DecisionTreeClassifier(), grid, cv=5)
search.fit(X_train, y_train)
search.best_params_   # {'max_depth': 4, 'min_samples_leaf': 30}
search.best_score_    # 0.782
search.score(X_test, y_test)   # 0.74
```

**12 combinations** × 5 folds = **60 trees** (plus one final refit of the winner on all the training loans).

Why 0.74 < 0.782: `best_score_` is the **best of 12** cross-validation scores, so the winner was partly lucky on these folds (the best of many is optimistic). The test set is new data that played no part in choosing, so its score is the honest one (and it is one split).

**Version B:**

```python
grid = {"max_depth": [2, 3, 5],
 "min_samples_leaf": [5, 20, 40]}
search = GridSearchCV(DecisionTreeClassifier(), grid, cv=5)
search.fit(X_train, y_train)
search.best_params_   # {'max_depth': 5, 'min_samples_leaf': 20}
search.best_score_    # 0.783
search.score(X_test, y_test)   # 0.76
```

**9 combinations** × 5 folds = **45 trees** (plus one final refit of the winner on all the training loans).

Why 0.76 < 0.783: `best_score_` is the **best of 9** cross-validation scores, so the winner was partly lucky on these folds (the best of many is optimistic). The test set is new data that played no part in choosing, so its score is the honest one (and it is one split).

## Question 7 (SLO 04A) --- Retake from Quiz 3

**Version A:**

| Table | Column | Answer |
|---|---|---|
| `loans` | `loan_id` | Primary key |
| `loans` | `student_id` | Foreign key -> students (it repeats: a student can borrow many books) |
| `students` | `student_id` | Primary key |
| `loans` | `book_id` | Foreign key -> books |
| `books` | `pages` | Neither (a measurement, not an identifier) |

**Version B:**

| Table | Column | Answer |
|---|---|---|
| `loans` | `book_id` | Foreign key -> books |
| `books` | `book_id` | Primary key |
| `students` | `prior_late` | Neither (a measurement, not an identifier) |
| `loans` | `student_id` | Foreign key -> students (it repeats: a student can borrow many books) |
| `loans` | `loan_id` | Primary key |

## Question 8 (SLO 04B) --- Retake from Quiz 3

**Version A:**

| Result | how= | rows |
|---|---|---|
| 1 | **right** | 4 |
| 2 | **inner** | 3 |
| 3 | **outer** | 5 |
| 4 | **left** | 4 |

S011 and S012 appear in both tables (3 loans): that's **inner**. **Left** keeps every loan, so L104 (student S015, not in `students`) appears with class_year NaN. **Right** keeps every student, so S013 (no loans) appears with loan_id NaN. **Outer** keeps both, so it has both NaN rows.

Left and right both give 4 rows here, so the row count alone can't tell them apart: look at **which side has the NaN**.

**Version B:**

| Result | how= | rows |
|---|---|---|
| 1 | **left** | 4 |
| 2 | **outer** | 5 |
| 3 | **inner** | 3 |
| 4 | **right** | 4 |

S023 and S024 appear in both tables (3 loans): that's **inner**. **Left** keeps every loan, so L201 (student S021, not in `students`) appears with class_year NaN. **Right** keeps every student, so S022 (no loans) appears with loan_id NaN. **Outer** keeps both, so it has both NaN rows.

Left and right both give 4 rows here, so the row count alone can't tell them apart: look at **which side has the NaN**.

## Question 9 (SLO 04C) --- Retake from Quiz 3

**Version A:**

```python
loans_long = pd.melt(
    monthly_loans,
    id_vars=["student_id"],
    value_vars=["sep", "oct", "nov"],
    var_name="month",
    value_name="n_loans",
)
```

| student_id | month | n_loans |
|---|---|---|
| S003 | sep | 0 |
| S003 | oct | 2 |
| S003 | nov | 1 |
| S007 | sep | 2 |
| S007 | oct | 0 |
| S007 | nov | 2 |

6 rows: 2 wide rows × 3 month columns. Row order may differ (pd.melt lists all sep rows first, then oct, then nov); any order is fine.

**Version B:**

```python
loans_long = pd.melt(
    monthly_loans,
    id_vars=["student_id"],
    value_vars=["sep", "oct", "nov"],
    var_name="month",
    value_name="n_loans",
)
```

| student_id | month | n_loans |
|---|---|---|
| S002 | sep | 0 |
| S002 | oct | 1 |
| S002 | nov | 1 |
| S005 | sep | 1 |
| S005 | oct | 0 |
| S005 | nov | 1 |

6 rows: 2 wide rows × 3 month columns. Row order may differ (pd.melt lists all sep rows first, then oct, then nov); any order is fine.

