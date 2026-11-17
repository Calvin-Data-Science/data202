# DATA 202 --- Quiz 5

Week 11 --- Preprocessing, Missing Data & Regression, plus Retakes of Weeks 6--7

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 5`, which
generates `quiz05_A.pdf` and `quiz05_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: The Campus Coffee Shop

The campus coffee shop promises: *your drink in 5 minutes, or a free cookie.* It
recorded 800 orders (simulated data), split into **600 training** and **200 test**
orders. Most questions use them.

- `minutes_since_open`: when the order was placed (0 = 7 am, 780 = 8 pm)
- `queue_length`: people ahead in line; `baristas`: baristas working (1--3)
- `drink` (latte, drip, tea or smoothie), `size` (S, M or L), `items`: drinks in the order
- `wait_minutes`: how long the customer waited (**the label** for regression)
- `late`: 1 = waited more than 5 minutes (**the label** for classification)

**A few rows of `orders`:**

**Version A sample rows:**

| order_id | minutes_since_open | queue_length | baristas | drink | size | items | wait_minutes | late |
|---|---|---|---|---|---|---|---|---|
| C001 | 523 | 1 | 1 | drip | M | 1 | 2.5 | 0 |
| C005 | 366 | 8 | 3 | latte | S | 1 | 3.7 | 0 |
| C006 | 402 | 6 | 1 | smoothie | L | 2 | 8.4 | 1 |
| C009 | 765 | 3 | 2 | latte | M | 3 | 5.8 | 1 |
| C012 | 299 | 10 | 2 | smoothie | M | 2 | 9.2 | 1 |

**Version B sample rows:**

| order_id | minutes_since_open | queue_length | baristas | drink | size | items | wait_minutes | late |
|---|---|---|---|---|---|---|---|---|
| C002 | 628 | 2 | 1 | smoothie | S | 1 | 2.4 | 0 |
| C008 | 223 | 3 | 2 | tea | L | 1 | 2.8 | 0 |
| C011 | 217 | 2 | 1 | tea | S | 1 | 4.4 | 0 |
| C013 | 446 | 5 | 1 | smoothie | L | 1 | 5.9 | 1 |
| C014 | 319 | 6 | 3 | tea | M | 3 | 3.1 | 0 |

## Question 1 (SLO 09A)

**Version A:**

| Column | Step and why |
|---|---|
| `minutes_since_open` | **StandardScaler**: a number on a much bigger ruler (0--780) than the others. Unscaled, it would decide almost every distance kNN measures. |
| `drink` | **OneHotEncoder**: words with no order. Numbering them 1--4 would invent distances (tea "closer" to drip than to smoothie); one 0/1 column per drink keeps every drink equally far apart. |
| `queue_length` | **StandardScaler**: a number. Scaling puts it on the same ruler as the other numbers, so each column counts about the same. |
| `size` | **OrdinalEncoder** (S < M < L): the order is real, so codes 0, 1, 2 keep it. (OneHotEncoder also works, but it throws the order away.) |

Every number column gets scaled, not only the biggest one: kNN adds up the differences in every column, so each needs the same ruler.

**Version B:**

| Column | Step and why |
|---|---|
| `size` | **OrdinalEncoder** (S < M < L): the order is real, so codes 0, 1, 2 keep it. (OneHotEncoder also works, but it throws the order away.) |
| `queue_length` | **StandardScaler**: a number. Scaling puts it on the same ruler as the other numbers, so each column counts about the same. |
| `drink` | **OneHotEncoder**: words with no order. Numbering them 1--4 would invent distances (tea "closer" to drip than to smoothie); one 0/1 column per drink keeps every drink equally far apart. |
| `minutes_since_open` | **StandardScaler**: a number on a much bigger ruler (0--780) than the others. Unscaled, it would decide almost every distance kNN measures. |

Every number column gets scaled, not only the biggest one: kNN adds up the differences in every column, so each needs the same ruler.

## Question 2 (SLO 09B)

**Version A:**

Any sound reason (one well explained is enough):

- **One object holds every step, in order.** `fit` and `predict` run them all, so new or test orders always get exactly the same preprocessing as the training orders: you can't forget to scale them, or scale them the wrong way.
- **It works with `cross_val_score` and `GridSearchCV`**: they redo every step in each fold, and can tune the steps' knobs (e.g. `kneighborsclassifier__n_neighbors`).
- **Less code, fewer mistakes, reproducible**: the whole workflow is one object you can save, share and rerun.

**Version B:**

Any sound reason (one well explained is enough):

- **One object holds every step, in order.** `fit` and `predict` run them all, so new or test orders always get exactly the same preprocessing as the training orders: you can't forget to scale them, or scale them the wrong way.
- **It works with `cross_val_score` and `GridSearchCV`**: they redo every step in each fold, and can tune the steps' knobs (e.g. `kneighborsclassifier__n_neighbors`).
- **Less code, fewer mistakes, reproducible**: the whole workflow is one object you can save, share and rerun.

## Question 3 (SLO 09C) --- From Practice 07

**Version A:**

| Column | Mechanism | What Practice 07 did |
|---|---|---|
| `age_years` | **MAR**: the blanks depend on something we can see (strays are 40% blank, other animals 3–10%), not on the age itself. | **KNNImputer** (after scaling): each blank age is filled from the 5 most similar animals (fix C). |
| `behavior_score` | **MNAR**: the blanks depend on the missing score itself (the stressed or reactive animals would have scored low). | **SimpleImputer** (median) **+ add an indicator variable** (`add_indicator=True`), so the model can still see "not assessed" (fix D). |

**Version B:**

| Column | Mechanism | What Practice 07 did |
|---|---|---|
| `behavior_score` | **MNAR**: the blanks depend on the missing score itself (the stressed or reactive animals would have scored low). | **SimpleImputer** (median) **+ add an indicator variable** (`add_indicator=True`), so the model can still see "not assessed" (fix D). |
| `age_years` | **MAR**: the blanks depend on something we can see (strays are 40% blank, other animals 3–10%), not on the age itself. | **KNNImputer** (after scaling): each blank age is filled from the 5 most similar animals (fix C). |

## Question 4 (SLO 10A)

**Version A:**

**(a)** Each extra person ahead in line adds about **0.76 minutes** (45 seconds) to the predicted wait, **for orders with the same number of baristas**.

**(b)** The extra baristas work the rush hours, when the lines are long (training orders: 2.7 people ahead with 1 barista, 8.2 with 3). Alone, the `baristas` slope also carries those long rush-hour lines, so more baristas *go with* longer waits. With `queue_length` in the model, each slope means "holding the other column fixed": at the same queue, more baristas mean a shorter wait.

**Version B:**

**(a)** Each extra barista cuts about **1.41 minutes** from the predicted wait, **for orders with the same queue length**.

**(b)** The extra baristas work the rush hours, when the lines are long (training orders: 2.7 people ahead with 1 barista, 8.2 with 3). Alone, the `baristas` slope also carries those long rush-hour lines, so more baristas *go with* longer waits. With `queue_length` in the model, each slope means "holding the other column fixed": at the same queue, more baristas mean a shorter wait.

## Question 5 (SLO 10B)

**Version A:**

| | model | clue |
|---|---|---|
| Model X | Ridge | **Ridge**: every slope is smaller, the near-copies *share* the effect (+1.45 and +0.80), and no slope is exactly 0. |
| Model Y | plain | **plain `LinearRegression`**: huge slopes with opposite signs on the near-copies (+13.91 and −11.96 minutes per SD, on 12 orders that average 3.8 minutes): a tug of war that cancels on these 12 orders only. It even gives `outdoor_temp` a slope. Overfitting. |
| Model Z | Lasso | **Lasso**: some slopes are **exactly 0** (`people_inside`, `items`, `outdoor_temp`): it keeps one of the two near-copies and drops the unrelated column. |

**Version B:**

| | model | clue |
|---|---|---|
| Model X | Lasso | **Lasso**: some slopes are **exactly 0** (`people_inside`, `items`, `outdoor_temp`): it keeps one of the two near-copies and drops the unrelated column. |
| Model Y | Ridge | **Ridge**: every slope is smaller, the near-copies *share* the effect (+1.45 and +0.80), and no slope is exactly 0. |
| Model Z | plain | **plain `LinearRegression`**: huge slopes with opposite signs on the near-copies (+13.91 and −11.96 minutes per SD, on 12 orders that average 3.8 minutes): a tug of war that cancels on these 12 orders only. It even gives `outdoor_temp` a slope. Overfitting. |

## Question 6 (SLO 10C)

**Version A:**

**Model 2.** Its typical miss is the smaller one (MAE 0.9 min), but RMSE squares each miss before averaging, so a few big misses blow it up (2.2 min, far above its MAE). Model 1's misses are more even: its RMSE (1.4) is close to its MAE (1.1).

**Version B:**

**Model 1.** Its typical miss is the smaller one (MAE 1.0 min), but RMSE squares each miss before averaging, so a few big misses blow it up (2.3 min, far above its MAE). Model 2's misses are more even: its RMSE (1.5) is close to its MAE (1.2).

## Question 7 (SLO 06A) --- Retake from Quiz 4

**Version A:**

k = 1 → **pair Q**, k = 25 → **pair R**, k = 600 → **pair P**.

- **k = 1**: each training order's nearest neighbor is *itself*, so it just repeats its own label: it has memorized the training orders (0.998, not 1, because two identical orders had different labels). On new orders it drops to 0.785: **overfitting**.
- **k = 600**: every training order is a neighbor, so the vote is always the majority, **on time**: the lazy model. Its scores are just the share of on-time orders (0.693 and 0.750): **underfitting**.
- k = 25 is in between, and best on the test orders.

**Version B:**

k = 1 → **pair R**, k = 51 → **pair P**, k = 600 → **pair Q**.

- **k = 1**: each training order's nearest neighbor is *itself*, so it just repeats its own label: it has memorized the training orders (0.998, not 1, because two identical orders had different labels). On new orders it drops to 0.785: **overfitting**.
- **k = 600**: every training order is a neighbor, so the vote is always the majority, **on time**: the lazy model. Its scores are just the share of on-time orders (0.693 and 0.750): **underfitting**.
- k = 51 is in between, and best on the test orders.

## Question 8 (SLO 06B) --- Retake from Quiz 4

**Version A:**

| Model | Answer | Why (for reference) |
|---|---|---|
| A spam filter that deletes every message it flags, with no junk folder to check (positive = spam). | **Precision** | A false positive deletes a real message (a job offer?) forever; a missed spam is only an annoyance. |
| A quick screening test for a serious disease that is treatable if caught early; everyone flagged gets a cheap follow-up test (positive = has the disease). | **Recall** | A false negative sends a sick person home untreated; a false positive costs only a follow-up test. |
| A foraging app that tells hikers which wild mushrooms are safe to eat (positive = safe). | **Precision** | A false positive calls a poisonous mushroom safe, and someone eats it; a false negative only leaves a good mushroom in the woods. |

Precision has FP in its denominator, so it drops with every false alarm; recall has FN, so it drops with every miss. The metric that matters more is the one whose mistake costs more.

**Version B:**

| Model | Answer | Why (for reference) |
|---|---|---|
| A smoke detector (positive = fire). | **Recall** | A false negative is a fire with no alarm; a false positive is a noisy kitchen. |
| A video app's filter that picks which videos may play on the kids' channel (positive = safe for kids). | **Precision** | A false positive shows an unsafe video to a child; a false negative only keeps a fine video off the channel. |
| A drone photographs a bridge and flags beams that may be cracked; an engineer then checks every flagged beam (positive = cracked). | **Recall** | A false negative leaves a cracked beam unchecked; a false positive costs an engineer a few minutes. |

Precision has FP in its denominator, so it drops with every false alarm; recall has FN, so it drops with every miss. The metric that matters more is the one whose mistake costs more.

## Question 9 (SLO 06C) --- Retake from Quiz 4, Code from Practice 05

**Version A:**

```python
text_train, text_test, y_train, y_test = train_test_split(sms["text"], y, test_size=0.2,
                                                          stratify=y, random_state=42)
print(len(text_train), "training messages |", len(text_test), "test messages")
```

**(a)** It shuffles the messages and splits them, with their labels, into **80% for training** (`text_train`, `y_train`) and **20% for testing** (`text_test`, `y_test`): that's `test_size=0.2`, 1,032 of 5,160 messages. `stratify=y` keeps the **same share of spam** (about 1 in 8) in both parts, so the test set can't end up short of spam by chance. (`random_state=42` gives the same split every run.)

**(b)** The test messages play the part of **new messages the model has never seen**. If the model learned from them, the test score would measure memory, not how well it works on new messages: too optimistic.

**Version B:**

```python
text_train, text_test, y_train, y_test = train_test_split(sms["text"], y, test_size=0.2,
                                                          stratify=y, random_state=42)
print(len(text_train), "training messages |", len(text_test), "test messages")
```

**(a)** `text_train` holds 80% of the messages (the ones the model learns from); `y_train` holds their labels, spam or not, in the same order. `stratify=y` keeps the **same share of spam** (about 1 in 8) in the training and test parts, so neither ends up short of spam by chance.

**(b)** On the messages it learned from, a model can score well just by **memorizing** them (kNN with k = 1 is almost perfect there). The test messages play the part of **new messages**, so their score shows how the filter will do on messages it has never seen.

## Question 10 (SLO 07A) --- Retake from Quiz 4

**Version A:**

- **baristas <= 1.5?** yes → **queue_length <= 3.5?** yes → **on time** (2 on time); no → **late** (4 late)
- no → **on time** (7 on time, 1 late)

Each leaf predicts the majority of the training orders in its region. (The cut values don't have to be exact: any number between the two nearest points is right.)

**No depth limit:** higher on the training orders (100%: it adds cuts around the odd orders), but probably **lower on new orders**, because those extra cuts chase noise: **overfitting**. A tree that is too shallow (depth 1) would underfit.

**Version B:**

- **queue_length <= 6.5?** yes → **on time** (7 on time, 1 late)
- no → **baristas <= 1.5?** yes → **late** (3 late); no → **on time** (3 on time, 1 late)

Each leaf predicts the majority of the training orders in its region. (The cut values don't have to be exact: any number between the two nearest points is right.)

**No depth limit:** higher on the training orders (100%: it adds cuts around the odd orders), but probably **lower on new orders**, because those extra cuts chase noise: **overfitting**. A tree that is too shallow (depth 1) would underfit.

## Question 11 (SLO 07B) --- Retake from Quiz 4

**Version A:**

Learns from **480**, scored on **120** (600 / 5 = 120 held out). Over the 5 rounds, each training order is held out exactly once.

**Version B:**

Learns from **450**, scored on **150** (600 / 4 = 150 held out). Over the 4 rounds, each training order is held out exactly once.

## Question 12 (SLO 07C) --- Retake from Quiz 4

**Version A:**

```python
best = 0
for depth in [2, 4, 6, 8, None]:
    for leaf in [1, 10, 30]:
        tree = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=leaf)
        tree.fit(X_train, y_train)
        score = tree.score(X_test, y_test)
        if score > best:
            best, best_params = score, (depth, leaf)
print(best_params, best)     # (4, 10) 0.84
```

**(a)** The test set **chose** the winner: of 15 trees, it kept the one that happened to do best on these 200 test orders, partly by luck. The best of 15 is optimistic, and the test set is no longer new data.

**(b)** **Cross-validation on the training orders only**: each combination is scored on held-out folds of `X_train`. `X_test` is used **once, at the end**, to score the chosen model (refit on all the training orders).

**Version B:**

```python
best = 0
for depth in [2, 3, 5, 10]:
    for leaf in [5, 20]:
        tree = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=leaf)
        tree.fit(X_train, y_train)
        score = tree.score(X_test, y_test)
        if score > best:
            best, best_params = score, (depth, leaf)
print(best_params, best)     # (5, 20) 0.86
```

**(a)** The test set **chose** the winner: of 8 trees, it kept the one that happened to do best on these 200 test orders, partly by luck. The best of 8 is optimistic, and the test set is no longer new data.

**(b)** **Cross-validation on the training orders only**: each combination is scored on held-out folds of `X_train`. `X_test` is used **once, at the end**, to score the chosen model (refit on all the training orders).

