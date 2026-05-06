---
marp: true
title: "Week 9: Unsupervised Learning — Clustering"
theme: default
paginate: true
---

# Unsupervised Learning: Clustering

### DATA 202 · Week 9

---

## Supervised vs. Unsupervised

| Supervised | Unsupervised |
|---|---|
| Labeled examples | No labels |
| Learn input → output | Find structure in input |
| Clear evaluation | Evaluation is harder |

---

## What is Clustering?

Group data points so that points in the same cluster are more similar to each other than to points in other clusters.

No ground truth. Structure is *imposed*, not discovered.

---

## k-Means Clustering

1. Choose *k* centroids randomly
2. Assign each point to nearest centroid
3. Update centroids to cluster mean
4. Repeat until convergence

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3).fit(X)
```

---

## Choosing k

- **Elbow method:** plot inertia vs. k
- **Silhouette score:** measure cluster cohesion vs. separation
- Domain knowledge often matters most

---

## Hierarchical Clustering

Build a tree of clusters (dendrogram).

- **Agglomerative:** start with each point as its own cluster, merge up
- **Divisive:** start with one cluster, split down

---

## DBSCAN

Density-based: finds clusters of arbitrary shape, labels outliers as noise.

```python
from sklearn.cluster import DBSCAN
```

---

## Questions to Sit With

- When the clusters we find reflect historical inequities — what then?
- Who decides which grouping is "meaningful"?

---

## This Week

- **Demo:** k-means and hierarchical clustering
- **Practice 9:** clustering a real-world dataset
- **Reading:** TBD — Chapter 8
