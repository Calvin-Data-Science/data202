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

Every reading since Reading 5 has predicted one of **two** classes: heart disease or not, high income or not. This one predicts one of **seven**. Along the way we meet two new kinds of models: **logistic regression**, a line that predicts probabilities, and **ensembles**, which combine many models into one, in three recipes: **bagging**, **boosting** and **stacking**.

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

Our file follows his lead. It takes **500 squares of each species** from those rows, 3,500 in all. Now the lazy model is right only about **1 time in 7**, and every species counts the same. (The price: a model trained this way thinks every species is equally common. We come back to that on page 8.)

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

The two numbers in the score shape the S:

- **b1 sets the steepness and the direction.** A bigger b1 makes the S steeper. A negative b1 flips it, so the probability *falls* as the column grows.
- **b0 slides the curve** left or right. The 50/50 point is where the score is 0: where the column equals −b0 ÷ b1.

Make b1 bigger and bigger, and the S turns into a step. A hard rule like "spruce/fir above 3,000 m" is an S-curve with an endless slope. Logistic regression is a softer rule: unsure near the cutoff, sure far from it.

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

> 🔁 **From Reading 5:** kNN also gave a probability: the share of the k neighbors with each label. And it, too, predicted the class above 50% unless we moved the cutoff. Page 3 moves this one.

## Reading the Slope: Odds

In Reading 8, a slope meant "this many dollars more per square foot," the same everywhere. Here, the probability does **not** rise by the same amount per 100 m:

| elevation | 2,800 → 2,900 | 3,000 → 3,100 | 3,200 → 3,300 |
|:---|---:|---:|---:|
| probability of spruce/fir | 0.18 → 0.29 | 0.44 → 0.60 | 0.75 → 0.85 |
| change | +0.11 | +0.16 | +0.10 |

The curve is steepest in the middle and flattens at both ends. So the same push to the score moves a **borderline** square the most: adding 1 to a score takes the probability from 0.50 to 0.73, but from 0.98 only to 0.99. For a borderline square, a small error in the map can flip the prediction. For a clear one, it changes nothing.

What *is* the same everywhere is the change in the **odds**. The odds are the probability of yes divided by the probability of no, p / (1 − p):

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

# Where to Draw the Line

## The 0.5 Is a Choice

`predict` says spruce/fir when the probability is at least **0.5**. That 0.5 is the **threshold**, and nothing forces it. Choosing it means choosing which mistakes to make.

> 🔁 **From Reading 5:** a **positive** is the class we are looking for. **Precision** = TP ÷ (TP + FP): of the cases flagged, the share that really are positive. **Recall** = TP ÷ (TP + FN): of the real positives, the share flagged. Lowering kNN's bar raised recall and lowered precision.

Picture a use for the model. Spruce beetles attack spruce, not pine. Suppose a forest crew plans to hike to every square the model flags as spruce/fir, to look for beetles. A positive is a spruce/fir square:

- A **false positive** is a wasted hike: the crew climbs to a stand of lodgepole pine.
- A **false negative** is a spruce/fir stand nobody checks, where an outbreak can grow unseen.

Page 2's model, with all the columns, gives each of the 773 squares a probability. To keep the scores honest, each square's probability comes from a model trained on the **other** four folds:

```python
from sklearn.model_selection import cross_val_predict

chance = cross_val_predict(model, X_two, y_two, cv=5, method="predict_proba")[:, 1]    # P(spruce/fir)
spruce = (y_two == "spruce/fir").to_numpy()
for threshold in [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]:
    flagged = chance >= threshold
    tp = (flagged & spruce).sum()
    print(threshold, flagged.sum(), tp / flagged.sum(), tp / spruce.sum(), (flagged == spruce).mean())
```

| threshold | squares flagged (hikes) | precision | recall | accuracy |
|---:|---:|---:|---:|---:|
| 0.8 | 142 | 0.83 | 0.30 | 62.0% |
| 0.7 | 233 | 0.80 | 0.48 | 68.0% |
| 0.6 | 325 | 0.77 | 0.64 | 72.2% |
| 0.5 | 397 | 0.74 | 0.76 | 74.3% |
| 0.4 | 480 | 0.68 | 0.85 | 72.6% |
| 0.3 | 555 | 0.65 | 0.93 | 71.4% |
| 0.2 | 629 | 0.60 | 0.97 | 65.5% |

Read down the table:

- **Lower the threshold** to 0.3, and the crew hikes to 555 squares instead of 397. It finds 93% of the spruce/fir instead of 76% (**recall up**), but 35% of its hikes end in lodgepole pine instead of 26% (**precision down**).
- **Raise it** to 0.7, and 4 hikes in 5 find spruce/fir, but more than half of the spruce/fir is never visited.

Accuracy is highest at 0.5: 74.3%, page 2's cross-validation score. But accuracy hides the trade-off, because it counts a wasted hike and a missed stand as the same kind of mistake. They are not. The right threshold depends on what each mistake costs, and who pays: a day of hiking, against an outbreak spreading unseen. That is a decision about the forest and the crew, not a fact in the data.

> 📌 **One split:** these counts come from cross-validation on 773 training squares. Another sample of squares would move each number by a few points.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

Lowering the threshold flags more squares. That raises **[recall]** and lowers **[precision]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**The crew can afford only about 250 hikes this summer. Using the table, which threshold fits, and what is the price?**

- [x] 0.7: about 233 hikes, 80% of them finding spruce/fir, but more than half of the spruce/fir squares go unchecked.
- [ ] 0.5, because it is the default and has the highest accuracy.
- [ ] 0.3, because it has the highest recall.
- [ ] 0.2, because it flags the most squares.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

Six squares get these probabilities of spruce/fir: 0.9, 0.7, 0.6, 0.4, 0.3 and 0.1. Only the squares at 0.9, 0.6 and 0.4 really are spruce/fir. At a threshold of 0.35, the model flags **[4]** squares. Its precision is **[0.75/.75/75%]** and its recall is **[1/1.0/100%]**.

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

For now, read the **left** matrix (the right one comes on page 5). Each row is one actual species; the diagonal counts the squares predicted correctly.

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

**Bagging** (Leo Breiman, 1996) keeps the deep trees but grows **many** of them, each on its own sample:

1. **Each tree gets its own sample.** Draw 2,625 squares **with replacement** from the 2,625 training squares: some squares get drawn twice or three times, others not at all. This is a **bootstrap sample**. With 10 squares numbered 1 to 10, one bootstrap draw might be 1, 1, 1, 2, 2, 3, 6, 9, 9, 9: squares 1 and 9 three times each, and squares 4, 5, 7, 8 and 10 left out. With 2,625 squares, each tree sees about **63%** of them; the other 37% are left out.
2. **The trees vote.** Each tree predicts a species and the majority wins. (Technically, scikit-learn averages the trees' probabilities; for fully grown trees, that's the same as counting votes.)

The name holds both steps: **b**ootstrap **agg**regat**ing**. A model built by combining many models is an **ensemble**.

A **random forest** (Breiman, 2001) is bagging with one more twist: **each question looks at a few random columns.** At every split, a tree may choose only among a random handful of the columns, by default the square root of their number: with 14 columns (10 numbers and 4 wilderness 0/1 columns), about **3**. One tree might have to split without elevation; it finds the next-best question.

```python
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier

bagging = Pipeline([("prep", onehot),
                    ("model", BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=1))])
rf = Pipeline([("prep", onehot), ("model", RandomForestClassifier(random_state=1))])    # 100 trees by default
scores = cross_validate(rf, X_train, y_train, cv=5, return_train_score=True)
```

Both get **100%** of the squares they learned from, like the single tree. But on the held-out squares, bagging gets **74.3%** and the forest **76.3%**: 9 and 11 points better than one tree, and the forest 9 better than logistic regression. The random columns make the forest's trees differ even more, and that helps.

More trees help, up to a point:

| trees in the forest | 1 | 3 | 10 | 30 | 100 | 300 | 1,000 |
|:---|---:|---:|---:|---:|---:|---:|---:|
| held-out accuracy | 61.5% | 66.2% | 72.8% | 75.7% | 76.3% | 76.8% | 77.1% |

A forest of **one** tree (61.5%) is worse than a plain tree (65.6%): it learned from a bootstrap sample and was limited to 3 columns per question. Alone, each forest tree is a weaker model. Together, they win. And adding trees never makes the forest overfit; after a hundred or so, the gains are small, and more trees just take longer.

## Why Make the Trees Different?

Test it. Turn the bootstrap off, so all 100 trees learn from the **same** 2,625 squares:

```python
clones = Pipeline([("prep", onehot),
                   ("model", BaggingClassifier(DecisionTreeClassifier(), n_estimators=100,
                                               bootstrap=False, random_state=1))])
```

The 100 trees score **66.5%**: about one tree's 65.6%, and far below real bagging's 74.3%. Trees grown from the same squares make the same mistakes, and a vote among copies only repeats them. Different trees make **different mistakes**, and a mistake that only a few trees make gets outvoted. **An ensemble gains only from members that differ.**

## Why the Forest Doesn't Overfit

Now give both the single tree and the forest the knob from Reading 6, `max_depth`:

![Line chart of accuracy against max_depth (2, 4, 6, 8, 10, 12, 15, 20, no limit). One tree (blue, circles): folds it learned from (dashed) rise from 48% to 100%; held-out folds (solid) rise from 47% to a peak of 68.1% at depth 8, then slip to 65.6% with no limit. Forest of 100 trees (orange, triangles): folds it learned from (dashed) rise from 56% to 100% by depth 15; held-out folds (solid) rise from 56% at depth 2 to 73.9% at depth 8 and keep inching up to 76.3% with no limit.](images/forest_depth.png)

Both models reach 100% on the squares they learned from: both memorize. But the single tree's held-out accuracy peaks at depth 8 and then **slips** (overfitting), while the forest's keeps **climbing** all the way to no limit. Each deep tree memorizes the quirks of its own bootstrap sample, and every sample has different quirks. In the vote, the quirks disagree and cancel out; the patterns that are real, like "krummholz grows at the top," are in every sample and win. **Many overfit trees, averaged, overfit much less than one.** That's why a random forest usually needs no depth limit.

Look back at the **right** matrix of the confusion figure on page 4. The forest catches more of every species: lodgepole pine's recall goes from 46% to **58%**, ponderosa pine's from 49% to **64%**, aspen's from 76% to **87%**. The mistakes still stay among neighbors on the mountain; there are just fewer of them.

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

Elevation first, by far. The **second** most important column is the distance to the nearest **road**. Hold on to that; page 8 asks what it means.

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

---

<!-- QUESTION:multiple-choice -->

**100 trees that all learn from the same 2,625 squares score 66.5%, about the same as one tree. Real bagging, with a bootstrap sample per tree, scores 74.3%. Why?**

- [x] Trees grown from the same squares make the same mistakes, so the vote only repeats them; bootstrap samples make the trees differ, and mistakes that only a few trees make get outvoted.
- [ ] Without bootstrap samples, each tree sees fewer squares.
- [ ] 100 is too few; with 1,000 identical trees, the vote would beat bagging.
- [ ] Bagging's trees are shallower, so they overfit less.

<!-- END QUESTION -->

# Boosting: Trees in a Row

## One Mistake at a Time

A forest grows its trees **side by side**: each one on its own sample, none knowing about the others. **Boosting** grows them **in a row**: each new tree focuses on what the ones before it got wrong. The classic recipe is **AdaBoost** (*adaptive boosting*), by Yoav Freund and Robert Schapire in the 1990s:

1. Every training square starts with the same **weight**.
2. Fit a small tree, by default a **stump**: a tree with a single question.
3. The stump's **error** is the total weight of the squares it gets wrong. Its **say** is ½ ln((1 − error) ÷ error): the fewer its mistakes, the bigger its say.
4. **Reweight:** the squares it got wrong get heavier, the rest lighter.
5. Back to step 2 with the new weights. To predict, the stumps vote, each with its say.

| the stump's error | 0.5 | 0.3 | 0.2 | 0.1 | 0.01 |
|:---|---:|---:|---:|---:|---:|
| its say | 0 | 0.42 | 0.69 | 1.10 | 2.30 |

A stump that is wrong half the time is a coin flip, and gets no say at all.

## Ten Squares, Three Stumps

Here is AdaBoost by hand, on 10 of page 2's squares and two columns:

```python
import numpy as np

few = X_two.sample(10, random_state=180)[["elevation_m", "water_dist_m"]]
few_species = y_two[few.index]
```

| square | elevation (m) | distance to water (m) | species |
|:---|---:|---:|:---|
| A | 2,875 | 277 | lodgepole pine |
| B | 2,925 | 787 | lodgepole pine |
| C | 2,979 | 67 | spruce/fir |
| D | 2,984 | 283 | lodgepole pine |
| E | 2,997 | 30 | spruce/fir |
| F | 2,999 | 551 | lodgepole pine |
| G | 3,052 | 366 | spruce/fir |
| H | 3,166 | 30 | spruce/fir |
| I | 3,195 | 469 | spruce/fir |
| J | 3,318 | 408 | spruce/fir |

(Sorted by elevation, and lettered for this page.) One round of AdaBoost, steps 1 to 4:

```python
weight = np.full(10, 1 / 10)                                              # step 1: all the same
stump = DecisionTreeClassifier(max_depth=1).fit(few, few_species, sample_weight=weight)   # step 2
wrong = (stump.predict(few) != few_species).to_numpy()
error = weight[wrong].sum()                                               # step 3
say = 0.5 * np.log((1 - error) / error)
weight = weight * np.where(wrong, np.exp(say), np.exp(-say))              # step 4
weight = weight / weight.sum()                                            # the weights add up to 1 again
```

Run it three times:

- **Stump 1** asks "elevation ≤ 3,025 m?" and says lodgepole pine below, spruce/fir above. It misses **C** and **E**: two spruce/fir squares below the cut, both right beside a stream (67 m and 30 m away). Error 0.1 + 0.1 = 0.2, say **0.69**.
- **Reweighting:** C and E now weigh **0.25** each, the other eight only 0.0625. Together, the two squares stump 1 missed hold **half** the weight. (That's always true in AdaBoost: after reweighting, the squares just missed hold exactly half.)
- **Stump 2** is fit with the new weights, where C and E count for half of everything. So it asks a different question: "within 172 m of water?", and says spruce/fir if yes. C and E are now right. It misses G, I and J instead, spruce/fir far from water: error 3 × 0.0625 = 0.19, say **0.73**.
- **Stump 3** goes back to elevation, with a lower cut, "elevation ≤ 2,952 m?". It misses D and F, the two highest lodgepole pine squares: error 0.08, say **1.24**.

Now the vote. Each stump backs its answer with its say. Square **D**: stumps 1 and 2 say lodgepole pine (0.69 + 0.73 = 1.42), stump 3 says spruce/fir (1.24). Lodgepole pine wins, 1.42 to 1.24, and it's right. Do this for all ten and the vote gets **every square right**, though each stump alone misses two or three. No square is missed by two stumps: each was trained to get right what the ones before it missed, so their mistakes don't line up.

Spruce beside a stream, below its usual elevation, is a known pattern: cold air and moisture drain down the valleys, and spruce follows them down. Stump 1 knew only elevation; stump 2 learned about the streams because stump 1's mistakes pointed there.

## Seven Species: Stumps Are Too Weak

`AdaBoostClassifier` runs these rounds for you. With its default stumps, on all seven species:

```python
from sklearn.ensemble import AdaBoostClassifier

ada = Pipeline([("prep", onehot), ("model", AdaBoostClassifier(n_estimators=300, random_state=1))])
cross_val_score(ada, X_train, y_train, cv=5).mean()      # 0.455
```

**45.5%**: worse than a single tree. A stump asks one question, so it can name only **two** species, and every stump leaves five out. No number of rounds fixes that: the stumps top out at 48%. That's **underfitting**: the members are too simple.

The fix is to give each round a small tree instead of a stump. The depth of those trees becomes a second knob, next to the number of rounds, and cross-validation chooses both:

```python
ada = Pipeline([("prep", onehot), ("model", AdaBoostClassifier(DecisionTreeClassifier(), random_state=1))])
grid = {"model__estimator__max_depth": [1, 2, 4, 6, 8, 10, 12],
        "model__n_estimators": [30, 100, 300, 1000]}
search = GridSearchCV(ada, grid, cv=5, return_train_score=True).fit(X_train, y_train)     # several minutes
```

Held-out accuracy:

| depth of each tree | 30 rounds | 100 rounds | 300 rounds | 1,000 rounds |
|:---|---:|---:|---:|---:|
| 1 (stumps) | 48.1% | 48.0% | 45.5% | 42.2% |
| 2 | 54.3% | 50.8% | 50.6% | 50.3% |
| 4 | 63.6% | 66.4% | 67.8% | 70.0% |
| 6 | 70.5% | 73.1% | 74.8% | 75.4% |
| 8 | 74.3% | 75.5% | 76.8% | 76.5% |
| 10 | 75.2% | 76.6% | **77.6%** | 77.0% |
| 12 | 75.0% | 77.0% | 77.0% | 77.3% |

The top rows underfit: stumps and 2-level trees can't sort seven species, however many rounds they get. Deeper trees climb. The best cell is **trees 10 levels deep, 300 rounds: 77.6%**. Past it, deeper trees or more rounds stop helping and slip a little: choose both knobs with cross-validation. (📌 The best few cells are within a point of each other, the size of the fold-to-fold noise.)

![Line chart of held-out accuracy against the number of rounds (AdaBoost) or trees (forest), from 1 to 1,000 on a log scale. AdaBoost with trees 10 levels deep (blue circles): 66.6% with 1 tree, 67.8% with 3, 70.9% with 10, 75.2% with 30, 76.6% with 100, 77.6% with 300, 77.0% with 1,000. Random forest (orange triangles): 61.5%, 66.2%, 72.8%, 75.7%, 76.3%, 76.8%, 77.1%; the blue and orange lines run together from 30 on. AdaBoost with trees 4 levels deep (green squares): 62.2%, 59.8%, 62.3%, 63.6%, 66.4%, 67.8%, 70.0%. AdaBoost with stumps (amber diamonds): 29.2%, 25.6%, 36.6%, 48.1%, 48.0%, 45.5%, 42.2%.](images/forest_boosting.png)

Next to the forest, AdaBoost with 10-level trees climbs the same way and ends in the same place. A 10-level tree is not a weak member: alone it gets 66.6%. Boosting still adds 11 points by putting 300 of them in a row. And like the forest's, its score on the squares it learned from is **100%** from 10 rounds on, while its held-out score keeps climbing to 300.

The other famous family, **gradient boosting**, also grows trees in a row. Each new tree is fit to how far the scores still are from the truth, and its answer is added to the scores. Fast versions called **XGBoost**, **LightGBM** and **CatBoost** win many machine learning competitions. On these squares, scikit-learn's `GradientBoostingClassifier`, with 300 rounds of 3-level trees, gets 73.2%.

---

## Check Your Understanding

<!-- QUESTION:true-false
answer: false
-->

In boosting, each tree is trained independently on its own bootstrap sample, and the trees vote at the end.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A stump misses 2 of 10 equally weighted squares, so its error is **[0.2/.2/0.20]**. After reweighting, the 2 squares it missed together hold **[half/50%/0.5]** of the weight, so the next stump focuses on them.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**AdaBoost with 300 stumps gets 45.5% on the seven species, worse than one tree, and about the same on the squares it learned from. What is going on?**

- [x] Underfitting: a stump asks one question, so it can name only two of the seven species. Giving each round a bigger tree fixes it.
- [ ] Overfitting: 300 stumps memorize the training squares.
- [ ] AdaBoost can only predict two classes.
- [ ] The stumps' says are all 0, so they never vote.

<!-- END QUESTION -->

# Stacking, and the Final Comparison

## Different Kinds of Models

Bagging and boosting combine many copies of **one kind** of model: trees. **Stacking** combines **different kinds**:

- Each **base model** predicts a probability for every species.
- A **meta-learner**, here one more logistic regression, takes those probabilities as its columns and learns **how much to trust each model**.
- It learns from **cross-validated** probabilities, so a base model that memorized its training squares (like the forest, at 100%) can't fool it.

```python
from sklearn.ensemble import StackingClassifier
from sklearn.neighbors import KNeighborsClassifier

stack = StackingClassifier(
    estimators=[("logistic", Pipeline([("prep", prep), ("model", LogisticRegression(C=10, max_iter=5000))])),
                ("knn", Pipeline([("prep", prep), ("model", KNeighborsClassifier(n_neighbors=15))])),
                ("forest", Pipeline([("prep", onehot), ("model", RandomForestClassifier(random_state=1))]))],
    final_estimator=LogisticRegression(), cv=5)
cross_val_score(stack, X_train, y_train, cv=5).mean()      # 0.758, about a minute
```

Stacked: **75.8%**. The forest alone: 76.3%. No gain.

Inside, the meta-learner has 21 columns: seven probabilities from each base model. Its slopes show whom it trusts. In each species' score, the slope on the forest's probability for that species averages **3.7**; on logistic regression's, **1.2**; on kNN's, **0.7** (kNN with 15 neighbors gets 61.1% alone). It has learned to lean on the forest.

Why doesn't stacking beat the forest? Count the training squares each base model gets wrong in cross-validation: logistic regression misses 851, kNN 1,022, the forest 623. **389** squares fool all three. And where the forest is wrong, the other two are rarely both right: on just 46 squares. The others know little that the forest doesn't. (kNN's number of neighbors barely matters here: with 1 or 5, stacking lands within half a point.)

## What Makes an Ensemble Work

Page 5's 100 identical trees scored like one tree. Stacking's three models gained nothing because they mostly miss the same squares. An ensemble gains only from members that are **different**, so each recipe builds the differences in:

| recipe | the members differ in |
|:---|:---|
| bagging, random forest | the squares each tree learns from (and, in a forest, the columns each question may use) |
| boosting | what each tree focuses on: the squares the ones before it missed |
| stacking | the kind of model |

## The Final Comparison

> 🔁 **From Reading 6:** choose with cross-validation on the training data. Open the test set **once**, at the very end, to estimate how the chosen model does on new data.

Each model with its knobs chosen by cross-validation, then scored once on the 875 test squares:

| model | 5-fold CV | test |
|:---|---:|---:|
| lazy model (always spruce/fir) | 14.8% | 12.8% |
| logistic regression, C = 10 | 67.6% | 67.4% |
| one tree, max_depth = 8 | 68.1% | 66.5% |
| stacking: logistic + kNN + forest | 75.8% | 76.3% |
| bagging: random forest, 100 trees | 76.3% | 78.1% |
| boosting: AdaBoost, 300 rounds of 10-level trees | 77.6% | 79.3% |

The ensembles win, and by more than luck: in **each** of the five cross-validation folds, the forest beats logistic regression by 7 to 11 points, and AdaBoost by 8 to 14. Among the ensembles, though, the order isn't settled. AdaBoost leads the forest in four folds and trails it in one, and the gap between them, about a point, is the size of the fold-to-fold noise. With a near-tie, prefer the simpler one: the forest needed no tuning at all, while AdaBoost needed a 28-cell grid.

On the test squares, the forest catches 97% of cottonwood/willow and 96% of krummholz, but only 60% of lodgepole pine and 61% of ponderosa pine; AdaBoost's pattern is nearly the same. And **103** of the 875 test squares (12%) fool all five models: squares where the map says one species and the forest grew another. No vote can fix a mistake that every member makes.

> 📌 **One split:** these scores come from one set of 875 squares, drawn from Blackard's training rows, with 125 of each species on average. A different split would move every number by a point or two. It could reorder the ensembles; it wouldn't close a 10-point gap to the line.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What does the meta-learner in a stacking classifier learn?**

- [x] How much to trust each base model's probabilities, learned from cross-validated predictions.
- [ ] Which columns of the original data each base model should use.
- [ ] The best depth for each tree in the forest.
- [ ] Nothing: it averages the base models' probabilities with equal weights.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Stacking logistic regression, kNN and a forest scored 75.8%, no better than the forest alone (76.3%). What is the best explanation?**

- [x] The three models mostly miss the same squares (389 fool all three), and where the forest is wrong the other two are rarely both right, so the meta-learner has little new to work with.
- [ ] The meta-learner overfit, because it learned from the forest's 100% predictions on its own training squares.
- [ ] Stacking always scores below its best base model.
- [ ] kNN should have used a different number of neighbors.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**AdaBoost scored 77.6% in cross-validation and 79.3% on the test squares; the forest, 76.3% and 78.1%. AdaBoost led in four of the five folds and trailed in one. Which conclusion is the most sensible?**

- [x] The two are about tied: a one-point gap is the size of the fold-to-fold noise. Both clearly beat logistic regression, by 7 to 14 points in every fold.
- [ ] AdaBoost is better, because it won both in cross-validation and on the test set.
- [ ] Boosting is always better than bagging.
- [ ] Neither really beats logistic regression: any gap could be luck.

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

A random forest is a crowd of models. Mackenzie describes how machine learning increasingly treats its models this way, as "members of a population whose variations and uncertainties, whose tendencies and predispositions must be sampled, tested, and monitored." Bootstrap samples, random columns, votes: the forest takes that sentence literally. And page 5's 100 identical trees show why the *variations* matter: a population of copies is just one model, repeated.

Breiman's 2001 paper introducing random forests is, Mackenzie notes, "perhaps the most cited journal paper in the machine learning literature." He also notices the datasets Breiman tested it on:

> "Glass, Breast cancer, Diabetes, Sonar, Vowel, Ionosphere, Vehicle, Soybean, German credit, Image, Ecoli, Votes, Liver, Letters, Sat-images, Zip-code, Waveform, Twonorm, Threenorm, Ringnorm"

Patients, soybeans, radar echoes, handwritten digits, loan applicants: the same algorithm, "a similarly diagonal line across human and nonhuman worlds," as Mackenzie puts it. The code that sorted our squares of forest would sort German credit applicants without changing a line. The forest doesn't know it is made of trees, or that it is predicting trees.

## What the Map Can't See

Blackard's documentation explains why he chose wilderness areas:

> "These areas represent forests with minimal human-caused disturbances, so that existing forest cover types are more a result of ecological processes rather than forest management practices."

That was a careful choice: in a wilderness, the label reflects what the mountain grows, not what someone planted or cut. But remember the purpose: predicting the trees on "inholdings or neighboring lands that are outside their immediate jurisdiction." Those neighboring lands may have been logged, burned or grazed. A model that learned where people left the forest alone, used where they didn't, sees the same kinds of columns in a different world.

Then there is the forest's second most important column: the distance to the nearest **road**. Trees don't care about roads. But roads are built along valleys and toward towns, so the distance to a road quietly stands in for things the map doesn't name: how low and accessible the land is, which wilderness area it's in, perhaps how it was used before it became wilderness. A column can carry information about something it doesn't measure, and an importance score can't tell you which. It says how much the forest **used** a column, not **why** the column helped.

Finally, our 500 squares of each species. The model believes all seven species are equally common, so it will call a square cottonwood/willow far more often than the real forest, where cottonwood/willow covers half a percent of the land, would justify. Blackard's own neural network, trained on 1,620 squares of each species, was tested on the remaining **565,892** squares with their real mix. It got **70.58%** right, against **58.38%** for a line-based method called linear discriminant analysis. (Those numbers can't be compared with our 78–79%: different test squares, with a very different mix of species.) Even in 1998, the flexible model beat the line.

## Questions Worth Asking About Any Classifier

- **What is the label, and who recorded it?** Here, the main tree cover in the Forest Service's records, one label per 30-meter square.
- **How were the rows chosen?** 500 of each species, not the real mix; wilderness, not managed land.
- **What does the lazy model score?** One in seven here; 49% on the real mix.
- **Which classes get confused, and how often is each caught?** One accuracy hides a 97% and a 60%.
- **Where is the threshold, and who chose it?** 0.5 by default; the right one depends on which mistake costs more, and to whom.
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
