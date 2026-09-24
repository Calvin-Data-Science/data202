---
layout: week
title: "Week 5: Clustering and Dimensionality Reduction"
week_number: 5
---

# Sorting Without an Answer Key

## A Table With No Labels

A small credit union has a file of 300 people who applied for a loan or a credit card. Its manager asks: *what types of applicants do we have?* There is no column saying "good borrower" or "risky borrower," and nobody knows how many types there are. There are only numbers.

In machine learning, a column that holds an answer you'd want a model to learn ("did this person repay?") is called a **label**. This week's data has no label. Finding structure in data *without* labels is called **unsupervised learning**, and it's what this reading is about: how to find groups, how to decide how many, and how to squeeze many columns into a few, or even into one.

**📥 Download the dataset: [applicants.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/applicants.csv)**

This is a teaching and fake dataset, built to behave like credit records, but there is no real people data here!

```python
import pandas as pd

applicants = pd.read_csv("applicants.csv")
applicants.head(3)
```

| applicant_id | annual_income | credit_history_years | late_payments | credit_utilization_pct | open_accounts |
|:---|---:|---:|---:|---:|---:|
| A001 | 35000 | 3.8 | 0 | 28 | 2 |
| A002 | 42500 | 4.3 | 3 | 33 | 6 |
| A003 | 28900 | 2.3 | 0 | 5 | 1 |

Start with the question to ask of any table: **what is one row about?** Here, one row is *one applicant*. Five columns describe them:

| Column | What it measures | Unit |
|:---|:---|:---|
| `annual_income` | yearly income | dollars |
| `credit_history_years` | time since their first credit account (card, loan...) | years |
| `late_payments` | payments made late in the last 2 years | a count |
| `credit_utilization_pct` | share of their available credit currently in use | percent (0–100) |
| `open_accounts` | number of credit accounts they have open | a count |

## Starting With Two Columns

To keep everything visible, we start with just two columns, so every applicant fits on one flat plot: income across, late payments up.

![Scatter plot of 300 applicants, annual income on the horizontal axis (about $12k to $130k) and late payments in the last two years on the vertical axis (0 to 15). All dots are the same gray. Many applicants sit along the bottom at zero or one late payment, spread across all incomes; a looser cloud with 5 to 10 late payments sits at low incomes; and a band with 2 to 5 late payments sits at middle incomes.](images/applicants_unlabeled.png)

(`late_payments` is a whole number, so in the plots we've nudged each dot up or down a little so that dots sharing the same value don't hide each other.)

Before reading on, decide: how many groups do you see here? Keep your answer in mind. The next page is about how a computer can make that decision *without eyes*.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What makes this week's task *unsupervised*?**

- [x] The algorithm is given only the features (the columns describing each row) — there is no label column of correct answers to learn from or check against.
- [ ] The algorithm runs without any human writing code for it.
- [ ] The data is fake, so it can't be used for supervised learning.
- [ ] The dataset has fewer than 1,000 rows.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Unsupervised learning can only be used when a dataset has no label column at all; if a label exists, you are not allowed to run an unsupervised method.

<!-- END QUESTION -->

# Finding Groups: k-means

## "Similar" Needs a Number

To group applicants, a computer first needs to know what it means for two applicants to be **similar**. The most common answer is geometric: two applicants are similar if their dots are **close together** on the plot, and "close" can be measured with a ruler.

Take three made-up applicants:

| Applicant | annual_income | late_payments |
|:---|---:|---:|
| A | 92,000 | 0 |
| B | 40,000 | 0 |
| C | 38,000 | 7 |

The straight-line distance between two points comes from the Pythagorean theorem: take the difference in each column, square each difference, add them up, and take the square root.

| Pair | Difference in income | Difference in late payments | Distance |
|:---|---:|---:|---:|
| A – B | 52,000 | 0 | √(52,000² + 0²) = **52,000** |
| A – C | 54,000 | 7 | √(54,000² + 7²) = **54,000** |
| B – C | 2,000 | 7 | √(2,000² + 7²) = **2,000** |

This is **Euclidean distance**, and it turns "which applicants are similar?" into a question with a numerical answer. By this measure, B's closest neighbor is C.

Stop and look at that. B has *never* paid late; C paid late seven times. Yet they count as nearly identical, because a $2,000 income difference is a much bigger *number* than 7. The seven late payments add 7² = 49 to a squared distance of 4,000,049, about 0.001%. Hold on to that; it will matter a lot on the next page.

## Centroids: The Middle of a Group

The second idea is the **centroid** of a group: its average position, meaning the mean of each column over the rows in that group. For B and C together, the centroid is at income (40,000 + 38,000) / 2 = 39,000 and late payments (0 + 7) / 2 = 3.5. A centroid doesn't have to be a real applicant. It's the point in the middle of the group's dots.

## The Recipe

**k-means** groups points using nothing but distances and centroids. You tell it how many groups to find (that number is the **k**), and it follows this recipe:

1. **Start:** pick `k` starting centroids (for example, `k` randomly chosen points).
2. **Assign:** give every point to its **nearest** centroid. Each centroid now "owns" a group of points.
3. **Update:** move each centroid to the **mean** of the points it owns.
4. **Repeat** steps 2 and 3 until an assign step changes nothing. The algorithm has **converged**.

Here it is on the applicants with `k = 4`. Each black ✕ is a centroid; each color shows which centroid an applicant currently belongs to.

![Four small scatter plots of the applicants showing k-means at work. Top left, "Start": all dots gray, four black X centroids picked from the data. Top right, "Round 1 - assign": every dot colored by its nearest centroid. Bottom left, "Round 1 - update": each X moved to the middle of its colored dots. Bottom right, "Round 13: nothing moves - done": four groups that are vertical slices of the plot by income — every color spans the full height from 0 to many late payments.](images/kmeans_steps.png)

Each update moves the centroids, which changes who is nearest to whom, which changes the groups... After 13 rounds nothing moves, and the algorithm stops. It never sees a label; its only question is "which centroid is closest?"

Some choices are ours, not the algorithm's: `k = 4`, the starting points, and the straight-line ruler. Settings you pick *before* running an algorithm are called **hyperparameters**. The starting points matter more than you'd expect: a different start can settle into a worse set of groups, and the algorithm can't tell. So scikit-learn runs the recipe from several starts and keeps the best result (that's `n_init=10` below).

## Running It With scikit-learn

**scikit-learn** is the Python library we'll use for machine learning all semester. Almost every model follows the same pattern: create it with its hyperparameters, then fit it to data.

```python
from sklearn.cluster import KMeans

two = applicants[["annual_income", "late_payments"]]

kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
applicants["cluster"] = kmeans.fit_predict(two)
```

`fit_predict` runs the recipe and returns one cluster number per applicant, stored here as a new column. The cluster numbers (0, 1, 2, 3) are arbitrary, so on another computer "cluster 0" might be a different group. Below, we've renamed them **A, B, C, D** from lowest to highest average income.

![Scatter plot of the applicants colored by four k-means clusters, with a black X at each centroid. The four clusters are vertical slices by income: cluster A below about $38k, B from about $38k to $55k, C from about $55k to $80k, D above about $80k. Within each slice, applicants with zero late payments and applicants with eight or nine late payments share the same color.](images/kmeans_clusters_raw.png)

## Checking Without an Answer Key

With no label to compare against, how do we know what k-means found? We **describe** each cluster, with a `groupby` from Week 3:

```python
applicants.groupby("cluster").agg(
    n_applicants=("applicant_id", "count"),
    avg_income=("annual_income", "mean"),
    avg_late=("late_payments", "mean"),
).round(1)
```

| cluster | n_applicants | avg_income | avg_late |
|:---|---:|---:|---:|
| A | 77 | 30,070.1 | 3.7 |
| B | 76 | 45,193.4 | 3.1 |
| C | 75 | 66,588.0 | 2.8 |
| D | 72 | 96,727.8 | 0.4 |

These are **four income brackets**, and almost nothing else. Clusters A, B, and C have similar average late payments, because each one mixes never-late applicants with frequently-late ones. You can see it in the plot: every slice runs from the bottom of the chart to the top. The distance table already told us why. Measured in dollars, late payments barely count. The next page shows the fix.

---

## Check Your Understanding

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

k-means begins by picking k starting *[centroids]*. In the *[assign]* step, every point goes to its nearest centroid. In the *[update]* step, each centroid moves to the *[mean]* of the points it owns. These two steps repeat until nothing changes, and we say the algorithm has *[converged]*.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

Point P is at (2, 1) and point Q is at (5, 5). Their differences are 3 and 4, so the Euclidean distance between them is √(3² + 4²) = **[5]**.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Because k-means always follows the same two steps, running it from two different sets of starting centroids is guaranteed to produce the same final clusters.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Which of these is a *hyperparameter* of k-means — something you choose before the algorithm runs?**

- [x] The number of clusters, `k`.
- [ ] Which cluster each point ends up in.
- [ ] The final position of each centroid.
- [ ] The number of points in each cluster.

<!-- END QUESTION -->

# One Ruler for Every Column: Scaling

## Why Income Wins

The **standard deviation** (`.std()`, the same number that appears in `.describe()`) measures how far values typically sit from their column's average:

```python
two.std().round(1)
```

```text
annual_income    25872.7
late_payments        3.0
dtype: float64
```

Incomes typically differ from the average by about $26,000; late payments by about 3. So in raw units, a *typical* income difference is thousands of times bigger than a typical late-payment difference, and after squaring (as the distance formula does), income decides essentially everything. Nobody told k-means that income matters more. The unit made it so.

Yet 7 late payments is a *huge* difference between two applicants (more than two standard deviations), while $2,000 of income is an ordinary one.

## Standardizing: Measuring in "Typical Differences"

The fix is to put every column on the same ruler before measuring distances. **Standardizing** (computing **z-scores**) does this column by column:

1. **Subtract the column's mean.** Now 0 means "exactly average."
2. **Divide by the column's standard deviation.** Now 1 means "one typical difference above average."

In a formula: **z = (value − column mean) ÷ column standard deviation**.

Here the means are $59,029 (income) and 2.5 (late payments), and the standard deviations are about $25,800 and 3.0. Applicants A, B, and C before and after:

| Applicant | income | late | income (z) | late (z) |
|:---|---:|---:|---:|---:|
| A | 92,000 | 0 | 1.28 | −0.85 |
| B | 40,000 | 0 | −0.74 | −0.85 |
| C | 38,000 | 7 | −0.81 | 1.51 |

Read it like this: C's income is 0.81 standard deviations *below* average, and C's late payments are 1.51 standard deviations *above* average. Every standardized column has mean 0 and standard deviation 1, so a difference of 1 means the same in any column.

Now recompute the distances with the z-scores:

| Pair | Distance before (dollars and counts) | Distance after (z-scores) |
|:---|---:|---:|
| A – B | 52,000 | 2.01 |
| A – C | 54,000 | 3.15 |
| B – C | 2,000 | 2.36 |

B's closest neighbor is now **A**, the other applicant who never paid late, not C. Late payments finally get a real vote.

scikit-learn does this with `StandardScaler`:

```python
from sklearn.preprocessing import StandardScaler

two_scaled = StandardScaler().fit_transform(two)

kmeans_scaled = KMeans(n_clusters=4, n_init=10, random_state=42)
applicants["cluster_scaled"] = kmeans_scaled.fit_predict(two_scaled)
```

(`fit_transform` first computes each column's mean and standard deviation, the *fit*, then turns every value into a z-score, the *transform*.)

![Two side-by-side scatter plots of the applicants on the same income and late-payment axes, colored by k-means cluster. Left, "Before scaling": four vertical income slices. Right, "After StandardScaler": cluster A is low-income applicants with many late payments (around 7); cluster B is low-to-middle-income applicants with almost no late payments; cluster C is middle-income applicants with a few late payments (around 3); cluster D is high-income applicants with almost no late payments.](images/kmeans_scaled_vs_raw.png)

Same algorithm, same applicants, different ruler, and the boundaries now fall where your eye probably put them. Describe the new clusters the same way:

| cluster | n_applicants | avg_income | avg_late |
|:---|---:|---:|---:|
| A | 68 | 37,492.6 | 7.0 |
| B | 86 | 39,569.8 | 0.5 |
| C | 62 | 62,882.3 | 3.3 |
| D | 84 | 93,540.5 | 0.3 |

Now A and B have almost the same average income, but A averages 7 late payments and B averages half of one. Those are two very different kinds of applicant, and unscaled k-means had lumped them together.

## When to Scale

| If your columns are... | Then... |
|:---|:---|
| in **different units** (dollars and counts, grams and millimeters, minutes and percentages) | **scale first**, or the biggest numbers decide everything |
| in the **same unit** with very **different spreads** | **usually scale**, unless you *want* the wider column to count more |
| already on one shared scale (pixel brightness, 0 to 255) | optional, and sometimes unhelpful: it inflates columns that barely vary |

The lesson: **any method that measures distance or spread depends on units.** Choosing how to scale is choosing how much each column is allowed to count.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**A housing dataset has `price` (in dollars, varying by hundreds of thousands) and `bedrooms` (varying by about 1). You run k-means on both columns without scaling. What will most likely happen?**

- [x] Price will decide almost all of the distances, so the clusters will be price brackets and the number of bedrooms will barely matter.
- [ ] Bedrooms will dominate, because it is the smaller number.
- [ ] Both columns will count equally, because k-means treats all columns the same.
- [ ] k-means will raise an error because the units don't match.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A column has mean 50 and standard deviation 10. After standardizing, a value of 70 becomes a z-score of **[2]**, and a value of 50 becomes a z-score of **[0]**.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

After `StandardScaler`, every column has a mean of 0 and a standard deviation of 1.

<!-- END QUESTION -->

# How Many Groups?

## The Question k-means Can't Answer

We told k-means to find 4 groups because of how the plot looked. But k-means will happily find 2, or 5, or 40, and never say a `k` is wrong. With no labels, nobody hands you the right `k`. Here are the two most common ways to compare values of `k` using only the data.

## The Elbow Method (Inertia)

**Inertia** measures how *tight* the clusters are: for every point, square its distance to its own centroid, and add everything up. Small inertia means points sit close to their centroids.

The catch: inertia **always goes down** as you add clusters, since more centroids means every point can find one closer by. With `k = 300`, every applicant would be their own cluster and inertia would be 0. So instead of looking for the smallest inertia, you plot it for several values of `k` and look for the **elbow**: where the curve stops dropping steeply. Before the elbow, each new cluster splits a real group; after it, new clusters just chop existing groups into pieces.

```python
inertias = []
for k in range(1, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(two_scaled)
    inertias.append(km.inertia_)
```

## The Silhouette Score

The **silhouette score** asks, point by point: *is this point much closer to its own cluster than to the nearest other cluster?*

- Near **+1**: snugly in its own cluster, far from the others.
- Near **0**: on the boundary between two clusters.
- Below **0**: closer to another cluster than its own, so probably in the wrong one.

The score for a whole clustering is the average over all points, and **higher is better**. Unlike inertia, it does *not* automatically improve as `k` grows, because chopping a real group in half creates lots of boundary points.

```python
from sklearn.metrics import silhouette_score

sil_scores = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(two_scaled)
    sil_scores.append(silhouette_score(two_scaled, labels))
```

(It starts at `k = 2`: with only one cluster there's no "other" cluster to compare with.)

![Two line charts side by side for the standardized income and late-payment columns. Left, "Elbow: inertia keeps falling": inertia drops from 600 at k=1 to 321 at k=2 and 156 at k=3, then 103 at k=4 and flattens after that, with an arrow marking a bend around k = 3 or 4. Right, "Silhouette: higher is better": the score is 0.43 at k=2, 0.50 at k=3, peaks at 0.51 at k=4, then falls to 0.50 at k=5 and 0.46 at k=6.](images/elbow_silhouette.png)

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|:---|---:|---:|---:|---:|---:|---:|
| inertia | 600.0 | 320.6 | 156.3 | **103.2** | 83.0 | 67.4 |
| silhouette | — | 0.428 | 0.497 | **0.512** | 0.495 | 0.463 |

Inertia drops steeply up to `k = 3`, still noticeably at 4, then flattens: the bend is around 3 or 4. Silhouette is highest at 4, but 3 and 5 are close behind. That's a common result. The metrics narrow the choice down; they don't make it for you.

Both only measure how well separated the groups are *in the columns and on the ruler you chose*; neither knows what the groups are for. With no label to check against, the other test is the one from the previous page: **describe the groups** and ask whether they are meaningful for your purpose.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Why can't you simply choose the `k` with the lowest inertia?**

- [x] Inertia always decreases as k increases — the lowest inertia would come from giving every point its own cluster, which tells you nothing.
- [ ] Inertia can only be computed for k = 3.
- [ ] Lower inertia means the clusters are worse, so you should choose the highest.
- [ ] Inertia measures how many points are in each cluster, not how tight they are.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

In the elbow method, you plot *[inertia]* for several values of k and look for the point where the curve stops dropping steeply. The silhouette score compares each point's distance to its own cluster with its distance to the nearest *[other]* cluster; a score near *[1]* means the point is well matched, and a score near *[0]* means it sits on a boundary.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**The elbow and silhouette both suggest k = 3 for a dataset with no labels, but your project needs exactly 5 groups. What's the best way to think about this?**

- [x] The metrics describe how separated the groups are in these columns; they don't know your purpose. Choosing 5 can be reasonable, as long as you describe the groups and know the extra ones are less clearly separated.
- [ ] You must use k = 3, since the metrics have found the true number of groups.
- [ ] The metrics are broken, since they disagree with your project.
- [ ] You should keep adding columns until the metrics say 5.

<!-- END QUESTION -->

# More Than Two Columns: PCA

## The Problem With a Flat Plot

We have five columns, and real datasets often have hundreds. k-means doesn't mind, since its distance formula works for any number of columns (square the difference in *each*, add them all up). But *you* can't look at five columns at once, and if you can't look at your data, you can't check what an algorithm did with it.

## Shadows

Think of a 3-D object and its shadow on a wall. The shadow is flat, so some information is always lost, but *how much* depends on the angle of the light. Shine it down the length of a pencil and the shadow is a dot; shine it from the side and the shadow shows the whole pencil. The best angle is the one where the shadow is **as spread out as possible**.

**Principal Component Analysis (PCA)** finds that best angle automatically, for any number of columns:

- **PC1 (the first principal component):** the direction through the data along which the points are **most spread out**. Spread is measured by **variance** (the standard deviation, squared).
- **PC2:** the direction with the most spread *left over*, at a right angle to PC1.
- **PC3, PC4, …:** and so on, one per column.

Here's the idea with two related columns, late payments and credit utilization (both standardized):

![Scatter plot of late payments (scaled) versus credit utilization (scaled). Most applicants sit in a tight clump at low late payments and low-to-middle utilization; the rest spread up and to the right, where more late payments go with higher utilization. A long blue arrow labeled PC1 points along that diagonal; a short orange arrow labeled PC2 points across it, at a right angle.](images/pca_direction.png)

Applicants with more late payments also tend to use more of their available credit, so the cloud stretches along a diagonal. PC1 runs along it, PC2 across it. Describe each applicant by just their position along PC1, one number, and you keep **89%** of the variance of these two columns. That one number is basically "financial strain."

So PCA is a **rotation** of the data onto new axes, sorted from most spread to least, so you can keep the first few and drop the rest. (In linear-algebra terms, these directions are the **eigenvectors** of the data's covariance matrix, and the variance along each is its **eigenvalue**. You won't need to compute them by hand.)

## Scaling Matters Here Too

PCA chases *variance*, and variance depends on units. On the five raw columns:

```python
from sklearn.decomposition import PCA

columns = ["annual_income", "credit_history_years", "late_payments",
           "credit_utilization_pct", "open_accounts"]
components = ["PC1", "PC2", "PC3", "PC4", "PC5"]

pca_raw = PCA().fit(applicants[columns])
pd.Series(pca_raw.explained_variance_ratio_ * 100, index=components).round(3)
```

```text
PC1    100.0
PC2      0.0
PC3      0.0
PC4      0.0
PC5      0.0
dtype: float64
```

`explained_variance_ratio_` is the share of the total variance each component captures. PC1 takes essentially **100%**, and it is almost exactly `annual_income`. Income in dollars has a variance of about 669 million; late payments, about 9. Unscaled, PCA decides income is the whole story, just as unscaled k-means did. So we standardize first:

```python
applicants_scaled = StandardScaler().fit_transform(applicants[columns])

pca = PCA()
pca.fit(applicants_scaled)
pd.Series(pca.explained_variance_ratio_ * 100, index=components).round(1)
```

```text
PC1    51.5
PC2    31.7
PC3     7.8
PC4     4.7
PC5     4.2
dtype: float64
```

| Component | Share of the variance | Cumulative (first n together) |
|:---|---:|---:|
| PC1 | 51.5% | 51.5% |
| PC2 | 31.7% | 83.2% |
| PC3 | 7.8% | 91.1% |
| PC4 | 4.7% | 95.8% |
| PC5 | 4.2% | 100.0% |

**The first two components keep 83.2% of the variation in five columns.** Squeeze each applicant from five numbers to two, and we lose only about 17% of the variance. The cumulative column is how you decide how many components to keep: go down it until you reach a share you're comfortable with (say 80%, 90%, or 95%).

## What Does a Component Mean?

Each component is a *mix* of the original columns. `pca.components_` gives the weights:

| Column | PC1 | PC2 |
|:---|---:|---:|
| annual_income | 0.57 | 0.10 |
| credit_history_years | 0.42 | 0.44 |
| late_payments | −0.37 | 0.57 |
| credit_utilization_pct | −0.43 | 0.51 |
| open_accounts | 0.42 | 0.46 |

An applicant scores high on PC1 with a high income, a long credit history, and many accounts, and with *few* late payments and *low* utilization (those two have negative weights). PC1 looks like what a lender might call **"creditworthiness."** PC2 gives positive weights to history, accounts, late payments, *and* utilization: it grows with how much someone uses credit at all, good or bad. Call it **"credit activity."** These names are interpretation. PCA supplies the weights; the names come from us.

## Seeing All Five Columns at Once

Now we can do what we couldn't before. We cluster on all five scaled columns, then use two components to *look* at the result:

```python
kmeans5 = KMeans(n_clusters=4, n_init=10, random_state=42)
applicants["cluster5"] = kmeans5.fit_predict(applicants_scaled)

pca2 = PCA(n_components=2)
pc_scores = pca2.fit_transform(applicants_scaled)   # 300 rows x 2 columns
```

Describing the four clusters with a `groupby` suggests names for them:

| our name for the cluster | applicants | income | history (yrs) | late | utilization % | accounts |
|:---|---:|---:|---:|---:|---:|---:|
| struggling | 61 | 36,395 | 11.1 | 7.1 | 85.9 | 4.0 |
| new to credit | 71 | 39,866 | 2.2 | 0.3 | 27.4 | 1.7 |
| stretched | 79 | 57,524 | 10.0 | 3.4 | 67.1 | 6.2 |
| established | 89 | 91,164 | 18.7 | 0.3 | 17.9 | 7.3 |

![Scatter plot of the applicants in PCA space: PC1 (51.5% of the variance) across, PC2 (31.7%) up, colored by the four k-means clusters. "Established" applicants form a group on the right; "struggling" on the upper left; "stretched" in the upper middle; and "new to credit" form a separate group at the bottom, low on PC2.](images/pca_applicants.png)

Along PC1, "established" applicants sit far right and "struggling" ones far left. Along PC2 ("credit activity"), "new to credit" sits far below everyone else. PCA never saw the clusters, yet its two numbers show all four apart.

Still, this is a **shadow**: it holds 83.2% of the variance, not all of it, and points that overlap here may be apart in five dimensions. PCA gives you the most informative flat view there is. It's still one view.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What does the first principal component (PC1) represent?**

- [x] The direction through the data along which the points are most spread out (have the most variance).
- [ ] The original column with the largest average value.
- [ ] The cluster with the most points in it.
- [ ] The column that best predicts a label.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

A PCA on standardized data gives explained variance ratios of 50%, 30%, 15%, and 5%. Keeping only the first two components keeps **[80]**% of the variance. To keep at least 90%, you need the first **[3]** components.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

A 2-D plot of the first two principal components shows all of the information in the original data, so points that overlap in the plot must also be close in the original columns.

<!-- END QUESTION -->

# From Groups to a Score

## Squeezing an Applicant Into One Number

The credit union's manager now asks for something simpler than four groups: *one number per applicant*, so they can be put in order. PC1 already is one number per applicant, and it already rewards high income and long history and penalizes late payments. Stretch it onto a familiar-looking range, 300 to 850, and it looks exactly like a credit score:

```python
pc1 = pca2.transform(applicants_scaled)[:, 0]          # each applicant's position along PC1
applicants["score"] = (300 + 550 * (pc1 - pc1.min()) / (pc1.max() - pc1.min())).round()
```

The lowest PC1 becomes 300, the highest becomes 850, and everyone else lands in between.

Real credit scores are *not* built this way. Credit bureaus build them from records of who actually repaid, and the exact formulas are kept secret. But the basic move is the same one we just made: many columns about a person go in, one number comes out, and that number puts everyone in order. As sociologists Marion Fourcade and Kieran Healy note, the secrecy means that "information about how to manage and improve one's score tends to take on the aspect of lore."

## Naming and Ranking

In the chapter "Classification Situations" of their book *The Ordinal Society* (2024), Fourcade and Healy distinguish two ways of sorting. **Nominal** judgments put things into named types, saying *what kind* something is. Our clusters are nominal, with no built-in order; in their words, this kind of naming "finds its formal representation in clustering and classification methods." **Ordinal** judgments line things up:

> "Ordinal classifications, meanwhile, are explicitly organized by measures of position, priority, or value along some countable dimension."

Our score is ordinal: it ranks all 300 applicants on one line. And the two kinds of sorting keep turning into each other:

> "A continuous measure may be simplified to a numerical rank, or binned into some number of ordered categories, or dichotomized into a binary classification."

Cut the score into bands (under 500 "poor," 500–599 "fair," 600–699 "good," 700 and up "excellent") and the ranking becomes a set of named types again. Cut it once ("approve" above 600, "deny" below) and it becomes a yes-or-no decision.

## Who Ends Up Low?

Here is every applicant's score, one row per cluster:

![Strip chart of the 300 applicants' scores from 300 to 850, one row per cluster, with dashed lines marking the poor, fair, good, and excellent bands. Established applicants average 744, all in the good or excellent bands. Stretched applicants average 546. New-to-credit applicants average 501, spread across the poor and fair bands. Struggling applicants average 429, almost all poor.](images/pca_score_by_group.png)

| cluster | average score | average late payments | poor | fair | good | excellent |
|:---|---:|---:|---:|---:|---:|---:|
| struggling | 429 | 7.1 | 58 | 3 | 0 | 0 |
| new to credit | 501 | 0.3 | 34 | 37 | 0 | 0 |
| stretched | 546 | 3.4 | 14 | 57 | 8 | 0 |
| established | 744 | 0.3 | 0 | 0 | 15 | 74 |

Look at the middle two rows. The "new to credit" applicants average *0.3* late payments, the same as the "established" ones, and 56 of the 71 never paid late at all. The "stretched" applicants average 3.4 late payments and use two-thirds of their available credit. Yet the new-to-credit group scores *lower*, and almost half of it lands in "poor." Of the 56 who never paid late, 23 score "poor."

Nothing about their behavior earns that. Look back at PC1's weights: it rewards credit *history*, open *accounts*, and income. A young person, a recent immigrant, or anyone who has avoided debt has little of the first two, so the score counts their *invisibility* against them. Fourcade and Healy describe exactly this trap:

> "Invisibility is as much a trap as visibility. Simply avoiding debt will not do: you'll just end up with a bad score, which you can only hope to improve by subjecting yourself to more intrusive data inquiries."

## What One Number Keeps, and What It Loses

Our score is built from PC1 alone, which kept **51.5%** of the variance. The rest, including PC2's "credit activity" (the very direction that set the new-to-credit group apart), is gone from the ranking. Fourcade and Healy make the same point about scores like these:

> "The resulting one-dimensional measure will contain much less information than its multidimensional parent."

Nothing in the number warns you about what's missing. A score of 501 looks just as precise as any other number.

## Scores Change the People They Score

A pixel or a star doesn't know how it was classified. People do, and classifications change them. Fourcade and Healy quote the philosopher Ian Hacking: classifications of people, when "known by people or those around them, and put to work in institutions, [they] change the ways in which individuals experience themselves—and may even lead people to evolve their feelings and behavior in part because they are so classified."

Follow a "poor" score forward. The applicant is denied, or offered credit at a higher interest rate. Higher payments make late payments more likely; being denied means no new history. Either way, next year's data looks worse, and next year's score confirms this year's. Hacking calls these **looping effects**: the label feeds back into the data that produced it.

When a category has real consequences for a person, Fourcade and Healy call it a **classification situation**. Classification situations, they write, are "positions in a generated system of categories that are consequential for one's life chances." The math is identical whether the rows are pixels or people. What changes is what the groups and scores are *used* for, and whether the people inside them can see, question, or contest where they've been placed.

## Questions Worth Asking About Any Grouping or Score

- **Which columns went in, and on what ruler?** Scaling decided whether late payments counted at all.
- **Who chose `k`, and the cutoffs between bands?** The metrics described the data; people drew the lines.
- **Who is invisible to it?** Missing history is not bad history, but a score can't tell them apart.
- **Could the people being sorted change because of the sorting?** Almost always.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**You score every row of a dataset on PC1 and sort from lowest to highest. What have you created, and what should you keep in mind?**

- [x] An ordinal ranking on a single number. It keeps only the share of variance PC1 captured, and everything the other components held is missing from the ranking.
- [ ] A nominal classification with no order, that keeps all of the original information.
- [ ] A set of clusters identical to what k-means would find.
- [ ] A supervised model, because the rows now have an order.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

A score built from PC1 can rank a person low even if they did nothing "wrong" on some columns, because every column with a weight in PC1 pulls the score — including columns that measure how visible the person is (like years of history), not how they behaved.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

Ian Hacking describes *[looping]* effects: when people know how they have been classified, and institutions act on that classification, their behavior can change in ways that reinforce the category. Fourcade and Healy call a category with real consequences for someone's life chances a *[classification]* situation. Sorting people into types is a *[nominal]* judgment; lining them up on a single score is an *[ordinal]* one.

<!-- END QUESTION -->
