---
layout: week
title: "Week 11: Other Models — logistic regression, ensembles"
week_number: 11
---

# Which Tree Grows Here?

## A Forest Seen From the Map

The Roosevelt National Forest covers the mountains of northern Colorado, west of Fort Collins. Inside it lie four wilderness areas: **Rawah**, **Neota**, **Comanche Peak** and **Cache la Poudre**. In the late 1990s, Jock Blackard, a Forest Service mapping specialist working on a PhD at Colorado State University, asked a simple question about them: **can you tell which trees cover a patch of land from a map alone?**

The question had a practical reason. Forest managers keep careful records of their own lands, but, as his dissertation abstract puts it, they "generally do not have this type of data for inholdings or neighboring lands that are outside their immediate jurisdiction." Sending a crew to every hillside is slow and expensive. A map, though, exists everywhere: elevation, slope, which way the slope faces, how far it is to a stream or a road.

So Blackard cut the four wilderness areas into squares of **30 × 30 meters**, measured each square from maps, and looked up which trees the US Forest Service had recorded there. That gave 581,012 squares, and a dataset that machine learners have used ever since.

Every square is labeled with one of **seven** kinds of tree cover:

| species | what it is |
|:---|:---|
| krummholz | German for "crooked wood": stunted, wind-bent trees at the tree line |
| spruce/fir | the cold, dark forest just below the tree line |
| lodgepole pine | tall, straight pines, once used for lodge poles |
| aspen | white-barked trees whose leaves turn gold in fall |
| Douglas-fir | not a true fir at all (hence the hyphen) |
| ponderosa pine | big pines of the dry, lower slopes |
| cottonwood/willow | trees along streams in the valleys |

Every reading since Reading 5 has predicted one of **two** classes: heart disease or not, high income or not. This one predicts one of **seven**. Along the way we meet two new kinds of models: **logistic regression**, a line that predicts probabilities, and **ensembles**, which combine many models into one.

**📥 Download the dataset: [forest.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/forest.csv)**

```python
import pandas as pd

forest = pd.read_csv("forest.csv")
forest.shape          # (3500, 12): 3,500 squares of land, 12 columns
```

| column | what it holds |
|:---|:---|
| `elevation_m` | height above sea level, in meters |
| `aspect_deg` | which way the slope faces, in compass degrees (0 = north, 90 = east, 180 = south) |
| `slope_deg` | how steep the ground is, in degrees |
| `water_dist_m` | distance to the nearest stream or lake, in meters |
| `water_height_m` | height above that water, in meters (negative = below it) |
| `road_dist_m` | distance to the nearest road, in meters |
| `shade_9am`, `shade_noon`, `shade_3pm` | how much sun reaches the square at that hour on the longest day of the year: 0 = full shade, 255 = full sun |
| `fire_dist_m` | distance to the nearest place where a past wildfire started, in meters |
| `wilderness` | which of the four wilderness areas |
| `species` | the label: the main tree cover |

There are no blanks. All columns are numbers except `wilderness` and `species`.

## 500 of Each

The full dataset is far from even. Of the 581,012 squares, **211,840** are spruce/fir and **283,301** are lodgepole pine: together, **85%** of the forest. Cottonwood/willow covers just 2,747 squares, half of one percent.

That makes the full data a strange test. A lazy model that always says "lodgepole pine" is right 49% of the time, and a model that only ever learned the two big species could be right 85% of the time while knowing nothing about aspen or cottonwood. Blackard faced the same problem, and his solution is in the file: its first 11,340 rows hold **exactly 1,620 squares of each species**, and those were the rows he trained on.

Our file follows his lead. It takes **500 squares of each species** from those rows, 3,500 in all. Now the lazy model is right only about **1 time in 7**, and every species counts the same. (The price: a model trained this way thinks every species is equally common. We come back to that on page 6.)

As always, the test set is locked away until the very end:

```python
from sklearn.model_selection import train_test_split

X = forest.drop(columns="species")
y = forest["species"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
```

That gives **2,625 training squares** and **875 test squares**. In the training set, the most common species is spruce/fir, with 388 squares: the lazy model scores **14.8%**.

## Look Before You Fit

> 🔁 **From Readings 7 and 8:** before fitting anything, look at the columns, and at how the label changes with them.

On a mountain, the obvious column to look at first is elevation:

![Strip plot of elevation in meters for the 2,625 training squares, one row of dots per species, with a black tick at each median. From bottom to top: cottonwood/willow, median about 2,240 m, range 1,991 to 2,526; ponderosa pine, median about 2,410, range 1,903 to 2,831; Douglas-fir, median about 2,435, range 1,874 to 2,869; aspen, median about 2,790, range 2,489 to 2,988; lodgepole pine, median 2,950, range 2,485 to 3,409; spruce/fir, median about 3,140, range 2,630 to 3,615; krummholz, median 3,358, range 2,925 to 3,848. The ponderosa pine and Douglas-fir rows overlap almost completely.](images/forest_elevation.png)

The species sit on the mountain like layers of a cake:

- **Cottonwood and willow** in the valleys, around 2,240 m.
- **Ponderosa pine** and **Douglas-fir** on the lower slopes, around 2,400 m.
- **Aspen** at about 2,790 m, then **lodgepole pine** at 2,950 m and **spruce/fir** at 3,140 m.
- **Krummholz** at the top, around 3,360 m, where trees give up growing tall.

Ecologists call these bands **life zones**. Elevation alone will sort a lot of squares. But look at the overlaps. Ponderosa pine and Douglas-fir live at almost exactly the same elevations. Lodgepole pine stretches from 2,485 to 3,409 m, overlapping every other species. For those, a model will need more than one column.

The wilderness areas differ too. All 381 cottonwood/willow squares in the training set are in Cache la Poudre, the lowest of the four areas.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Why does our file take 500 squares of every species, instead of a random sample of the whole forest?**

- [x] In the whole forest, two species cover 85% of the land, so a model could look accurate while knowing almost nothing about the five rare species; equal numbers make every species count the same.
- [ ] Logistic regression can't handle classes of different sizes.
- [ ] The rare species were recorded more accurately.
- [ ] A random sample would contain blanks.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

With 7 species in equal numbers, a lazy model that always guesses the same species is right about 1 time in **[7]**, which is about **[14]** percent.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Looking at the elevation plot, which pair of species will be hardest to tell apart using elevation alone?**

- [x] Ponderosa pine and Douglas-fir
- [ ] Krummholz and cottonwood/willow
- [ ] Aspen and krummholz
- [ ] Spruce/fir and ponderosa pine

<!-- END QUESTION -->

# Spruce or Pine? The S-Curve

## Two Species, One Question

Before taking on all seven, start with the two that matter most in the real forest: **spruce/fir** and **lodgepole pine**, 85% of the land. Which one grows in a given square?

```python
two = y_train.isin(["spruce/fir", "lodgepole pine"])
X_two = X_train[two]
y_two = y_train[two]          # 773 squares: 388 spruce/fir, 385 lodgepole pine
```

With two nearly equal groups, the lazy model scores **50.2%**.

> 🔁 **From Reading 8:** a line predicts a **number**: price = b0 + b1 × area.

A classification label isn't a number, but we can make it one: **1 = spruce/fir, 0 = lodgepole pine**. Then fit a line on elevation, and read its prediction as "the chance this square is spruce/fir":

```python
from sklearn.linear_model import LinearRegression

is_spruce = (y_two == "spruce/fir").astype(int)
line = LinearRegression().fit(X_two[["elevation_m"]], is_spruce)
line.predict(X_two[["elevation_m"]]).min(), line.predict(X_two[["elevation_m"]]).max()     # (-0.18, 1.23)
```

The line says some squares have a **−18%** chance of being spruce/fir, and others a **123%** chance. That's nonsense: 29 squares get a "chance" below 0 and 5 get one above 1. A straight line keeps going forever; a probability must stay between 0 and 1. We need a line that **bends** to stay inside.

## Squeezing a Line Into a Curve

**Logistic regression** does it in two steps:

1. Compute a **score** with a line, exactly as in Reading 8: z = b0 + b1 × elevation. The score can be any number.
2. **Squeeze** the score into a probability with the S-shaped **logistic curve** (also called the *sigmoid*):

```
p = 1 / (1 + e^(−z))
```

| score z | −4 | −2 | −1 | 0 | 1 | 2 | 4 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| probability p | 0.02 | 0.12 | 0.27 | 0.50 | 0.73 | 0.88 | 0.98 |

A score of 0 means 50/50. Big positive scores approach 1 but never reach it; big negative scores approach 0. Despite the word "regression" in its name, logistic regression is a **classifier**: it predicts the class whose probability is above 0.5.

```python
from sklearn.linear_model import LogisticRegression

logit = LogisticRegression().fit(X_two[["elevation_m"]], y_two)
logit.intercept_, logit.coef_           # (-19.91, 0.00656)
```

So the score is z = −19.91 + 0.00656 × elevation. The score is 0, and the model is unsure, where 0.00656 × elevation = 19.91: at **3,035 m**. Above that, it predicts spruce/fir; below, lodgepole pine.

![Scatter plot of the 773 training squares against elevation from 2,450 to 3,650 m: lodgepole pine squares as blue circles along y = 0, spruce/fir squares as orange triangles along y = 1, overlapping between about 2,700 and 3,300 m. A dashed straight line rises from about −0.22 at 2,450 m to 1.27 at 3,650 m, leaving the band between 0 and 1 at both ends (the regions outside are shaded gray). A black S-shaped logistic curve rises from about 0.02 to 0.98 and stays inside the band; a dot marks 50/50 at 3,035 m.](images/forest_scurve.png)

To get the probabilities themselves, use `predict_proba`. It returns one column per class, in alphabetical order (`logit.classes_` is `["lodgepole pine", "spruce/fir"]`), so column 1 is spruce/fir:

```python
heights = pd.DataFrame({"elevation_m": [2800, 3000, 3200]})
logit.predict_proba(heights)[:, 1]      # [0.18, 0.44, 0.75]
logit.predict(heights)                  # ['lodgepole pine', 'lodgepole pine', 'spruce/fir']
```

A square at 3,000 m is 44% spruce/fir: the model says lodgepole pine, but barely. At 3,200 m it's 75% spruce/fir.

> 🔁 **From Reading 5:** kNN also gave a probability: the share of the k neighbors with each label. And it, too, predicted the class above 50% unless we moved the cutoff.

## Reading the Slope: Odds

In Reading 8, a slope meant "this many dollars more per square foot," the same everywhere. Here, the probability does **not** rise by the same amount per 100 m:

| elevation | 2,800 → 2,900 | 3,000 → 3,100 | 3,200 → 3,300 |
|:---|---:|---:|---:|
| probability of spruce/fir | 0.18 → 0.29 | 0.44 → 0.60 | 0.75 → 0.85 |
| change | +0.11 | +0.16 | +0.10 |

The curve is steepest in the middle and flattens at both ends. What *is* the same everywhere is the change in the **odds**. The odds are the probability of yes divided by the probability of no, p / (1 − p):

- At 3,000 m: 0.442 / 0.558 = **0.79**. Lodgepole pine is a bit more likely.
- At 3,100 m: 0.604 / 0.396 = **1.53**. Now spruce/fir is more likely.

1.53 / 0.79 ≈ **1.93**. Every 100 m up multiplies the odds of spruce/fir by e^(100 × 0.00656) = e^0.656 = **1.93**, no matter where you start. Roughly: **every 100 m of elevation doubles the odds of spruce/fir.** That is how to read a logistic regression slope:

- The **sign** says which way: positive, so higher squares lean spruce/fir.
- **e to the slope** says by how much the odds are multiplied for one more unit of the column.

How good is one column? With 5-fold cross-validation, elevation alone gets **72.3%** right, against 50.2% for the lazy model.

## All the Columns

> 🔁 **From Reading 7:** a pipeline scales the number columns and one-hot encodes the word columns, fitting each step on the training rows only.

```python
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numbers = [c for c in X.columns if c != "wilderness"]
prep = ColumnTransformer([
    ("num", StandardScaler(), numbers),
    ("cat", OneHotEncoder(), ["wilderness"]),
])
model = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=5000))])
cross_val_score(model, X_two, y_two, cv=5).mean()      # 0.743
```

All the columns together reach **74.3%**, only 2 points more than elevation alone. Fit on the 773 squares, the slopes (per standard deviation, since the numbers were scaled) show why. (`num__` and `cat__` are the names of the two steps in `prep`.)

```python
model.fit(X_two, y_two)
slopes = pd.Series(model["model"].coef_[0], index=model["prep"].get_feature_names_out())
slopes.sort_values().round(2)
```

```text
num__slope_deg                    -0.54
cat__wilderness_Neota             -0.52
num__water_dist_m                 -0.51
num__shade_noon                   -0.50
num__shade_9am                    -0.43
num__shade_3pm                    -0.20
num__road_dist_m                  -0.07
num__water_height_m               -0.07
num__aspect_deg                   -0.07
cat__wilderness_Cache la Poudre   -0.03
num__fire_dist_m                   0.01
cat__wilderness_Rawah              0.13
cat__wilderness_Comanche Peak      0.36
num__elevation_m                   1.64
```

Positive slopes lean spruce/fir, negative ones lodgepole pine. Elevation's slope is three times bigger than any other. One more standard deviation of elevation multiplies the odds of spruce/fir by e^1.64 ≈ 5.2. Each slope means "holding the other columns fixed," as in Reading 8. That explains a surprise: Neota is the highest wilderness area, yet its slope points toward lodgepole pine. At the **same** elevation, Neota squares lean lodgepole; Neota's height is already counted by the elevation column.

One more property to keep in mind: the 50/50 squares are where the score is 0, and the score is a line. So the **boundary** between the two predictions is always straight: a single cutoff with one column, a straight line with two, a flat surface with more.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

The model gives a square at 3,000 m a probability of 0.44 of being spruce/fir. So it predicts **[lodgepole]** pine, because 0.44 is below **[0.5/0.50/50%]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**The elevation slope is 0.00656 per meter, and e^0.656 ≈ 1.93. What does that mean?**

- [x] Every 100 m higher multiplies the odds of spruce/fir (versus lodgepole pine) by about 1.93, wherever you start.
- [ ] Every 100 m higher adds 1.93 percentage points to the probability of spruce/fir.
- [ ] Above 1,930 m, every square is spruce/fir.
- [ ] Spruce/fir is 1.93 times as common as lodgepole pine.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Going from 3,000 m to 3,100 m raises the probability of spruce/fir by the same amount as going from 3,200 m to 3,300 m.

<!-- END QUESTION -->

# Seven Species at Once

## One Score per Species

With two classes, one score was enough: high means spruce/fir, low means lodgepole pine. With seven, logistic regression gives **each species its own score**, from its own line, with its own intercept and slopes. Then:

1. Turn each score z into e^z, a positive number.
2. Divide each by the total, so the seven numbers **add up to 1**. (This step is called the **softmax**.)
3. Predict the species with the **largest** probability.

The code doesn't change at all. Give `LogisticRegression` a label with seven names and it builds seven scores:

```python
model = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=5000))])
model.fit(X_train, y_train)
```

`coef_` now has seven rows, one per species. Elevation is the first column after `prep`, so `coef_[:, 0]` holds its slope (per standard deviation) in each species' score:

```python
pd.Series(model["model"].coef_[:, 0], index=model.classes_).sort_values(ascending=False).round(2)
```

| species | elevation slope in its score |
|:---|---:|
| krummholz | +10.18 |
| spruce/fir | +4.51 |
| lodgepole pine | +1.62 |
| aspen | −0.10 |
| Douglas-fir | −4.32 |
| ponderosa pine | −5.15 |
| cottonwood/willow | −6.73 |

It's the mountain again, from the top down. Going up, krummholz's score climbs fastest; cottonwood/willow's falls fastest.

Here is one training square, a gentle slope at 2,598 m in Comanche Peak, right beside a stream:

```python
square = X.loc[[2619]]
pd.Series(model.predict_proba(square)[0], index=model.classes_).sort_values(ascending=False).round(2)
```

```text
Douglas-fir          0.50
aspen                0.25
ponderosa pine       0.14
lodgepole pine       0.08
cottonwood/willow    0.02
spruce/fir           0.01
krummholz            0.00
```

The seven probabilities add up to 1. The model predicts **Douglas-fir**, with only a 50% probability, and it's right. Its second guess, aspen, also lives near this elevation. Krummholz, a tree-line species, gets essentially zero.

Cross-validated, the seven-species model gets **66.8%** right, against a lazy 14.8%. With the number columns alone, it gets 64.1%: the wilderness area adds about 3 points.

## The C Knob

> 🔁 **From Reading 8:** Ridge adds a penalty, α × (sum of squared slopes), so big slopes cost something. A bigger α means a simpler model.

`LogisticRegression` has the Ridge penalty **built in**, always on. Its knob is called `C`, and it works **backwards**: `C` is 1 / α. A **small C** is a **big** penalty. The default is C = 1. Like every knob, it is chosen by cross-validation:

```python
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(model, {"model__C": [0.001, 0.01, 0.1, 1, 10, 100, 1000]},
                      cv=5, return_train_score=True)
search.fit(X_train, y_train)
```

| C | folds it learned from | held-out fold |
|---:|---:|---:|
| 0.001 | 50.6% | 49.8% |
| 0.01 | 57.6% | 56.7% |
| 0.1 | 64.0% | 63.0% |
| 1 | 68.5% | 66.8% |
| 10 | 69.2% | 67.6% |
| 100 | 69.5% | 66.8% |
| 1000 | 69.5% | 67.0% |

At C = 0.001 the penalty squashes every slope toward 0, and both scores sit near 50%: **underfitting**. The best is **C = 10**, at **67.6%**. And there is no overfitting side: the two columns never drift more than 3 points apart. Seven lines with 15 numbers each (14 columns plus an intercept) are 105 numbers in all, too little freedom to memorize 2,625 squares.

## Where the Mistakes Go

> 🔁 **From Reading 5:** a confusion matrix counts each combination of actual and predicted class. **Recall** for a class is the share of its actual members the model catches.

With seven species, the confusion matrix is 7 × 7. To build it without touching the test set, `cross_val_predict` predicts each training square with the model trained on the **other** four folds:

```python
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix

best = Pipeline([("prep", prep), ("model", LogisticRegression(C=10, max_iter=5000))])
predicted = cross_val_predict(best, X_train, y_train, cv=5)
mountain = ["krummholz", "spruce/fir", "lodgepole pine", "aspen", "Douglas-fir", "ponderosa pine", "cottonwood/willow"]
confusion_matrix(y_train, predicted, labels=mountain)      # rows and columns from the top of the mountain down
```

![Two 7 by 7 confusion matrices side by side, rows = actual species, columns = predicted species, both in the order krummholz, spruce/fir, lodgepole pine, aspen, Douglas-fir, ponderosa pine, cottonwood/willow; darker blue = more squares. Left, logistic regression with C = 10, 67.6% right. Diagonal: 326, 240, 179, 276, 242, 174, 337. Biggest mistakes: lodgepole pine predicted as spruce/fir 96 and as aspen 83; ponderosa pine predicted as Douglas-fir 104 and as cottonwood/willow 61; Douglas-fir predicted as ponderosa pine 77; spruce/fir predicted as lodgepole pine 73 and as krummholz 54. The top-right and bottom-left corners are all zeros. Right, random forest with 100 trees, 76.3% right. Diagonal: 349, 249, 224, 315, 271, 229, 365. Biggest mistakes: lodgepole pine as spruce/fir 93; Douglas-fir as ponderosa pine 67; ponderosa pine as Douglas-fir 79; spruce/fir as lodgepole pine 73.](images/forest_confusion.png)

For now, read the **left** matrix (the right one comes on page 4). Each row is one actual species; the diagonal counts the squares predicted correctly.

| species | recall |
|:---|---:|
| cottonwood/willow | 88% |
| krummholz | 87% |
| aspen | 76% |
| Douglas-fir | 65% |
| spruce/fir | 62% |
| ponderosa pine | 49% |
| lodgepole pine | 46% |

The species at the top and bottom of the mountain are easy. **Lodgepole pine** is the hardest: of its 385 training squares, 179 are caught, 96 are called spruce/fir and 83 aspen, its neighbors on the mountain. **Ponderosa pine** is second-hardest: 104 of its squares are called Douglas-fir, the species at the same elevation.

Now look at the corners. The top right and bottom left are all zeros: no krummholz or spruce/fir square is ever called ponderosa pine or cottonwood/willow, and no ponderosa pine or cottonwood/willow square is ever called krummholz or spruce/fir. The mistakes stay among **neighbors on the mountain**, exactly where the elevation plot showed overlaps.

The lines have a deeper limit too. Each species' score **adds up** its columns' contributions: so much for elevation, plus so much for the distance to water, and so on. It can't say "being near water matters only in the valleys." A decision tree can say exactly that kind of thing: it asks one question, then a different question depending on the answer. That's where we go next.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

For any one square, the seven probabilities from `predict_proba` add up to **[1/1.0/100%]**, and the model predicts the species with the **[largest/highest/biggest]** probability.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**At C = 0.001 the model gets about 50% on the folds it learned from and about 50% on the held-out folds. What is happening?**

- [x] Underfitting: such a small C is a huge penalty, so every slope is squashed toward 0 and the model can't even fit the squares it learned from.
- [ ] Overfitting: the model memorized the training squares.
- [ ] The model is perfect; 50% is the best possible with seven species.
- [ ] C = 0.001 turns off the penalty.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**In the confusion matrix, the mistakes almost all stay between species that grow at similar elevations. What is the best explanation?**

- [x] Elevation is the column the model leans on most, so squares at the same height look alike to it, and species sharing a height get mixed up.
- [ ] The Forest Service mislabeled the squares at middle elevations.
- [ ] A confusion matrix can only show mistakes between neighboring rows.
- [ ] Logistic regression can't predict more than two species at once.

<!-- END QUESTION -->

# A Forest of Trees

## One Tree Again

> 🔁 **From Reading 6:** a decision tree asks one yes/no question after another. With no depth limit, it keeps asking until every leaf is pure, and memorizes the training data.

Trees compare numbers with thresholds, so they don't need scaling; the pipeline only one-hot encodes the wilderness area:

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate

onehot = ColumnTransformer([
    ("num", "passthrough", numbers),         # numbers go through unchanged
    ("cat", OneHotEncoder(), ["wilderness"]),
])
tree = Pipeline([("prep", onehot), ("model", DecisionTreeClassifier(random_state=1))])
scores = cross_validate(tree, X_train, y_train, cv=5, return_train_score=True)
```

With no depth limit, the tree grows **20 levels** deep with **534 leaves**. It gets **100%** of the squares it learned from and **65.6%** of the held-out ones: overfitting, and slightly worse than logistic regression's 67.6%. The best depth limit, 8, reaches **68.1%**. One tree, tuned or not, is about as good as a line here.

## Many Trees, Each a Little Different

A **random forest** (Leo Breiman, 2001) keeps the deep trees but grows **many** of them, and makes them **different on purpose**:

1. **Each tree gets its own sample.** Draw 2,625 squares **with replacement** from the 2,625 training squares: some squares get drawn twice or three times, others not at all. This is a **bootstrap sample**. With 10 squares numbered 1 to 10, one bootstrap draw might be 1, 1, 1, 2, 2, 3, 6, 9, 9, 9: squares 1 and 9 three times each, and squares 4, 5, 7, 8 and 10 left out. With 2,625 squares, each tree sees about **63%** of them; the other 37% are left out.
2. **Each question looks at a few random columns.** At every split, a tree may choose only among a random handful of the columns, by default the square root of their number: with 14 columns (10 numbers and 4 wilderness 0/1 columns), about **3**. One tree might have to split without elevation; it finds the next-best question.
3. **The trees vote.** Each tree predicts a species and the forest goes with the majority. (Technically, scikit-learn averages the trees' probabilities; for fully grown trees, that's the same as counting votes.)

Why make the trees different? Because a vote among identical trees is just one tree. Different trees make **different mistakes**, and a mistake that only a few trees make gets outvoted. This recipe, many models trained on bootstrap samples and then combined, is called **bagging** (short for *bootstrap aggregating*). A model built by combining many models is an **ensemble**.

```python
from sklearn.ensemble import RandomForestClassifier

rf = Pipeline([("prep", onehot), ("model", RandomForestClassifier(random_state=1))])    # 100 trees by default
scores = cross_validate(rf, X_train, y_train, cv=5, return_train_score=True)
```

The forest gets **100%** of the squares it learned from, like the single tree. But on the held-out squares it gets **76.3%**: 10 points better than one tree, and 9 better than logistic regression. More trees help, up to a point:

| trees in the forest | 1 | 3 | 10 | 30 | 100 | 300 | 1,000 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| held-out accuracy | 61.5% | 66.2% | 72.8% | 75.7% | 76.3% | 76.8% | 77.1% |

A forest of **one** tree (61.5%) is worse than a plain tree (65.6%): it learned from a bootstrap sample and was limited to 3 columns per question. Alone, each forest tree is a weaker model. Together, they win. And adding trees never makes the forest overfit; after a hundred or so, the gains are small, and more trees just take longer.

## Why the Forest Doesn't Overfit

Now give both the single tree and the forest the knob from Reading 6, `max_depth`:

![Line chart of accuracy against max_depth (2, 4, 6, 8, 10, 12, 15, 20, no limit). One tree (blue, circles): folds it learned from (dashed) rise from 48% to 100%; held-out folds (solid) rise from 47% to a peak of 68.1% at depth 8, then slip to 65.6% with no limit. Forest of 100 trees (orange, triangles): folds it learned from (dashed) rise from 56% to 100% by depth 15; held-out folds (solid) rise from 56% at depth 2 to 73.9% at depth 8 and keep inching up to 76.3% with no limit.](images/forest_depth.png)

Both models reach 100% on the squares they learned from: both memorize. But the single tree's held-out accuracy peaks at depth 8 and then **slips** (overfitting), while the forest's keeps **climbing** all the way to no limit. Each deep tree memorizes the quirks of its own bootstrap sample, and every sample has different quirks. In the vote, the quirks disagree and cancel out; the patterns that are real, like "krummholz grows at the top," are in every sample and win. **Many overfit trees, averaged, overfit much less than one.** That's why a random forest usually needs no depth limit.

Look back at the **right** matrix of the confusion figure on page 3. The forest catches more of every species: lodgepole pine's recall goes from 46% to **58%**, ponderosa pine's from 49% to **64%**, aspen's from 76% to **87%**. The mistakes still stay among neighbors on the mountain; there are just fewer of them.

## Which Columns Did the Forest Use?

A forest has no slopes to read. What it offers instead is `feature_importances_`: how much each column's questions reduced the impurity (the Gini index from Reading 6), added up over all the trees and scaled to sum to 1.

```python
rf.fit(X_train, y_train)
importance = pd.Series(rf["model"].feature_importances_, index=rf["prep"].get_feature_names_out())
importance.sort_values(ascending=False).round(2)
```

```text
num__elevation_m                   0.27
num__road_dist_m                   0.11
num__fire_dist_m                   0.08
num__water_dist_m                  0.07
num__shade_9am                     0.07
num__aspect_deg                    0.07
num__water_height_m                0.06
num__shade_noon                    0.06
num__shade_3pm                     0.06
cat__wilderness_Cache la Poudre    0.05
num__slope_deg                     0.04
cat__wilderness_Rawah              0.02
cat__wilderness_Comanche Peak      0.02
cat__wilderness_Neota              0.00
```

Elevation first, by far. The **second** most important column is the distance to the nearest **road**. Hold on to that; page 6 asks what it means.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What is a bootstrap sample of the 2,625 training squares?**

- [x] 2,625 squares drawn with replacement, so some squares appear several times and about a third don't appear at all.
- [ ] The 525 squares of one cross-validation fold.
- [ ] The 2,625 squares in a random new order.
- [ ] 2,625 new squares measured from the map.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Adding more trees to a random forest makes it overfit, so the number of trees must be kept small.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Every tree in the forest gets 100% of its own training squares, yet the forest's held-out accuracy keeps rising with depth while one tree's falls. Why?**

- [x] Each tree memorizes different quirks of its own bootstrap sample; in the vote those quirks disagree and cancel out, while the real patterns, shared by all samples, win.
- [ ] The forest secretly uses the test set.
- [ ] The trees in a forest have a depth limit even when max_depth is None.
- [ ] Voting always gives 100% accuracy.

<!-- END QUESTION -->

# Boosting, and the Final Comparison

## Trees in a Row

A forest grows its trees **side by side**: each one on its own sample, none knowing about the others. **Gradient boosting** grows them **in a row**:

1. Start with a simple guess for every square.
2. Build a **small** tree (3 levels by default) aimed at what the guesses still get **wrong**: for each square, how far its scores are from the truth.
3. Add that tree's answer to the scores, shrunk by the **learning rate** (0.1 by default, so each tree only gets a tenth of a say).
4. Repeat, each new tree working on the mistakes that are left.

A forest's trees each try to answer the whole question, and vote. A boosting tree only answers "what's still missing?", and the answers are **added up**. With seven species, each round builds one small tree for each species' score, so 300 rounds means 2,100 trees.

```python
from sklearn.ensemble import GradientBoostingClassifier

boost = Pipeline([("prep", onehot),
                  ("model", GradientBoostingClassifier(n_estimators=300, random_state=1))])
scores = cross_validate(boost, X_train, y_train, cv=5, return_train_score=True)    # about a minute
```

The knob is `n_estimators`, the number of rounds:

![Line chart of accuracy against the number of trees (1 to 1,000, log scale). Boosting, folds it learned from (blue dashed): 66.9% at 1 round, 72.9% at 10, 81.2% at 30, 93.7% at 100, and 100% at 300 and 1,000. Boosting, held-out folds (blue solid): 62.7% at 1, 67.1% at 10, 70.5% at 30, 72.5% at 100, 73.2% at 300, 73.0% at 1,000. Forest, held-out folds (orange): 61.5% with 1 tree, 72.8% with 10, 75.7% with 30, 76.3% with 100, 76.8% with 300, 77.1% with 1,000.](images/forest_more_trees.png)

Boosting improves quickly at first, then levels off: **73.2%** at 300 rounds, 73.0% at 1,000. Meanwhile its score on the folds it learned from runs all the way to **100%**. That widening gap is the shape of overfitting: every new tree chases the mistakes that are left, and in the end those are the odd squares, the ones that look like a different species. Here the held-out score only stops improving; on other data it can fall. So `n_estimators` must be chosen with cross-validation, together with the learning rate. (A bigger learning rate, like 0.3, gets there in fewer rounds: 72.4% after 30, but the same 73.2% at the top.)

On these squares, boosting lands **between** the single tree and the forest. Boosting is famous for winning machine learning competitions, especially in fast versions called **XGBoost**, **LightGBM** and **CatBoost**, but no model wins everywhere.

## The Final Comparison

> 🔁 **From Reading 6:** choose with cross-validation on the training data. Open the test set **once**, at the very end, to estimate how the chosen model does on new data.

Each model with its knob chosen by cross-validation, then scored once on the 875 test squares:

| model | 5-fold CV | test |
|:---|---:|---:|
| lazy model (always spruce/fir) | 14.8% | 12.8% |
| logistic regression, C = 10 | 67.6% | 67.4% |
| one tree, max_depth = 8 | 68.1% | 66.5% |
| gradient boosting, 300 rounds | 73.2% | 73.6% |
| random forest, 100 trees | 76.3% | 78.1% |

The random forest wins, and by more than luck: in **each** of the five cross-validation folds it beats logistic regression, by 7 to 11 points. On the test squares it catches 97% of cottonwood/willow and 96% of krummholz, but only 60% of lodgepole pine and 61% of ponderosa pine. And **98** of the 875 test squares (11%) fool all four models: squares where the map says one species and the forest grew another.

> 📌 **One split:** these scores come from one set of 875 squares, drawn from Blackard's training rows, with 125 of each species on average. A different split would move every number by a point or two. It wouldn't close a 10-point gap.

---

## Check Your Understanding

<!-- QUESTION:true-false
answer: false
-->

In gradient boosting, each tree is trained independently on its own bootstrap sample, and the trees vote at the end.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Boosting's score on the folds it learned from reaches 100% at 300 rounds, while its held-out score stays near 73%. What should you take from that?**

- [x] The model is fitting the training squares far better than new ones, the pattern of overfitting; the number of rounds should be chosen by cross-validation, not by the training score.
- [ ] Boosting is perfect: 100% is the best possible score.
- [ ] The held-out folds must contain mislabeled squares.
- [ ] More rounds will eventually bring the held-out score to 100% too.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**The forest beat logistic regression by about 9 points in cross-validation and 11 points on the test set, and won in every fold. Which conclusion is the most sensible?**

- [x] On this data the forest really is better: the gap is consistent and much bigger than the fold-to-fold noise. Its bendy, if-then boundaries fit how species sort on a mountain.
- [ ] The two models are tied, because any gap could be luck.
- [ ] Random forests are always better than logistic regression.
- [ ] The test set must be easier than the training set.

<!-- END QUESTION -->

# Forests, Examined

## An Old Curve

> 🔁 **From Readings 5–8:** Adrian Mackenzie's *Machine Learners* looks at where machine learning's tools come from, and what they do to the things they describe.

The S-curve is much older than machine learning. Mackenzie quotes the historian of statistics J. S. Cramer:

> "The logistic function was invented in the nineteenth century for the description of the growth of organisms and populations and for the course of autocatalytic chemical reactions."

The Belgian mathematician Pierre-François Verhulst named it the *logistic curve* in the 1830s and 1840s, to describe how a population grows quickly at first and then levels off as it reaches a limit. For a century it was a curve of **growth**. Logistic regression borrowed its shape for a different job: turning a score into a probability. Mackenzie's comment:

> "Note that the shape of this curve has no intrinsic connection or origin in the data."

Nobody measured an S-shape in the Colorado forest. We **chose** it, because it keeps probabilities between 0 and 1 and makes the slopes readable as odds. The forest made no such choice, and on these squares it did better.

So why is logistic regression still everywhere? Mackenzie quotes a team of biomedical researchers: "logistic regression is the default 'simple' model for predicting a subject's group status." Part of the answer is that it can be **read**. "Every 100 m of elevation doubles the odds of spruce/fir" is a sentence a forester can check against what they know about mountains. A forest of 100 trees, each with hundreds of leaves, gives a prediction and a list of importances, not a sentence. Sometimes 10 points of accuracy are worth that; sometimes being able to explain the model is worth more.

## A Population of Models

A random forest is a crowd of models. Mackenzie describes how machine learning increasingly treats its models this way, as "members of a population whose variations and uncertainties, whose tendencies and predispositions must be sampled, tested, and monitored." Bootstrap samples, random columns, votes: the forest takes that sentence literally.

Breiman's 2001 paper introducing random forests is, Mackenzie notes, "perhaps the most cited journal paper in the machine learning literature." He also notices the datasets Breiman tested it on:

> "Glass, Breast cancer, Diabetes, Sonar, Vowel, Ionosphere, Vehicle, Soybean, German credit, Image, Ecoli, Votes, Liver, Letters, Sat-images, Zip-code, Waveform, Twonorm, Threenorm, Ringnorm"

Patients, soybeans, radar echoes, handwritten digits, loan applicants: the same algorithm, "a similarly diagonal line across human and nonhuman worlds," as Mackenzie puts it. The code that sorted our squares of forest would sort German credit applicants without changing a line. The forest doesn't know it is made of trees, or that it is predicting trees.

## What the Map Can't See

Blackard's documentation explains why he chose wilderness areas:

> "These areas represent forests with minimal human-caused disturbances, so that existing forest cover types are more a result of ecological processes rather than forest management practices."

That was a careful choice: in a wilderness, the label reflects what the mountain grows, not what someone planted or cut. But remember the purpose: predicting the trees on "inholdings or neighboring lands that are outside their immediate jurisdiction." Those neighboring lands may have been logged, burned or grazed. A model that learned where people left the forest alone, used where they didn't, sees the same kinds of columns in a different world.

Then there is the forest's second most important column: the distance to the nearest **road**. Trees don't care about roads. But roads are built along valleys and toward towns, so the distance to a road quietly stands in for things the map doesn't name: how low and accessible the land is, which wilderness area it's in, perhaps how it was used before it became wilderness. A column can carry information about something it doesn't measure, and an importance score can't tell you which. It says how much the forest **used** a column, not **why** the column helped.

Finally, our 500 squares of each species. The model believes all seven species are equally common, so it will call a square cottonwood/willow far more often than the real forest, where cottonwood/willow covers half a percent of the land, would justify. Blackard's own neural network, trained on 1,620 squares of each species, was tested on the remaining **565,892** squares with their real mix. It got **70.58%** right, against **58.38%** for a line-based method called linear discriminant analysis. (Those numbers can't be compared with our 78%: different test squares, with a very different mix of species.) Even in 1998, the flexible model beat the line.

## Questions Worth Asking About Any Classifier

- **What is the label, and who recorded it?** Here, the main tree cover in the Forest Service's records, one label per 30-meter square.
- **How were the rows chosen?** 500 of each species, not the real mix; wilderness, not managed land.
- **What does the lazy model score?** One in seven here; 49% on the real mix.
- **Which classes get confused, and how often is each caught?** One accuracy hides a 97% and a 60%.
- **Can you read the model?** Odds per 100 m, or a hundred trees and a list of importances.
- **Where will it be used?** On land like the land it learned from?

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Mackenzie writes that the logistic curve's shape "has no intrinsic connection or origin in the data." What does he mean?**

- [x] The S-shape was invented to describe growth and then borrowed by modelers; nobody measured it in the data, it is a choice made because it keeps predictions between 0 and 1.
- [ ] The logistic curve never fits real data.
- [ ] Logistic regression ignores the data entirely.
- [ ] The S-shape is calculated from the data with cross-validation.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Why might the forest do worse on land just outside the wilderness areas, where the Forest Service wants to use it?**

- [x] It learned from wilderness, where tree cover follows ecological processes; on logged, burned or grazed land the same map measurements can come with different trees.
- [ ] Maps outside wilderness areas don't have elevation.
- [ ] Random forests can only predict the land they were trained on.
- [ ] The forest has too many trees for a larger area.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Because distance to the nearest road is the forest's second most important column, roads must be one of the causes of which trees grow where.

<!-- END QUESTION -->
