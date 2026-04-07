---
marp: true
title: "Week 7: Decision Trees & Ensembles"
theme: default
paginate: true
---

# Decision Trees & Ensembles

### DATA 202 · Week 7

---

## Decision Trees

A flowchart-like model that splits data based on feature thresholds.

```
Is age > 30?
├── Yes → Is income > 50k? → ...
└── No  → Predict: 0
```

Interpretable, but prone to overfitting.

---

## How a Tree is Built

At each node, find the split that most reduces impurity:

- **Gini impurity**
- **Information gain (entropy)**

Grows until a stopping criterion (max depth, min samples).

---

## The Overfitting Problem

A deep tree perfectly memorizes training data.

Solutions:
- Limit `max_depth`
- Require minimum samples per leaf
- **Build an ensemble**

---

## Random Forests

Train many trees on **bootstrap samples** of data + random feature subsets.

Aggregate predictions by majority vote or averaging.

Reduces variance without much increase in bias.

---

## Gradient Boosting

Train trees **sequentially**: each tree corrects the errors of the previous one.

`XGBoost`, `LightGBM`, `CatBoost` — state of the art on tabular data.

---

## Feature Importance

Tree models produce feature importances: how much each feature reduces impurity across all splits.

> Useful — but they aggregate complex interactions into a single number.

---

## Questions to Sit With

- Is a 50-node tree still "interpretable"? Interpretable to whom?
- When is accuracy worth trading away transparency?

---

## This Week

- **Demo:** random forest + feature importances
- **Lab 7:** ensemble methods on a classification task
- **Reading:** TBD — Chapter 7
