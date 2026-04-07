---
marp: true
title: "Week 10: Dimensionality Reduction"
theme: default
paginate: true
---

# Dimensionality Reduction

### DATA 202 · Week 10

---

## The Curse of Dimensionality

As dimensions increase:
- Data becomes sparse
- Distance metrics break down
- Models overfit more easily
- Visualization becomes impossible

---

## Two Goals of Dimensionality Reduction

1. **Compression:** represent data in fewer dimensions with minimal information loss
2. **Visualization:** project to 2D or 3D for human inspection

---

## Principal Component Analysis (PCA)

Find the directions of **maximum variance** in the data.

Project data onto the top *k* components.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit_transform(X)
```

---

## Interpreting PCA

- Components are **linear combinations** of original features
- Explained variance ratio: how much each component captures
- Loading plot: which features drive each component

---

## t-SNE

Non-linear method optimized for **2D/3D visualization**.

Preserves local structure well; global structure less reliable.

Not suitable for general compression — only visualization.

---

## UMAP

Faster than t-SNE, preserves more global structure.

Good for large datasets.

```python
import umap
embedding = umap.UMAP().fit_transform(X)
```

---

## Questions to Sit With

- PCA centers the data — whose variation is treated as signal vs. noise?
- What do 2D visualizations of high-dimensional data hide?

---

## This Week

- **Demo:** PCA and t-SNE on image/text data
- **Lab 10:** dimensionality reduction pipeline
- **Reading:** TBD — Chapter 9
