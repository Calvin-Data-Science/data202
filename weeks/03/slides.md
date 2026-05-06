---
marp: true
title: "Week 3: Feature Engineering"
theme: default
paginate: true
---

# Feature Engineering

### DATA 202 · Week 3

---

## What is a Feature?

A **feature** is a measurable property of the thing you're modeling.

Raw data → features → model input

Feature engineering is the art of creating useful representations.

---

## Encoding Categorical Variables

- **One-hot encoding:** `get_dummies(df['color'])`
- **Ordinal encoding:** when order matters
- **Target encoding:** replace with outcome mean (careful: leakage risk)

---

## Scaling Numerical Features

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
```

- **StandardScaler:** mean 0, std 1
- **MinMaxScaler:** scale to [0, 1]

Why? Many models assume features are on comparable scales.

---

## Binning & Transformations

- Log transform for skewed distributions
- Binning continuous variables into categories
- Polynomial features for non-linear relationships

---

## Data Leakage

> Using information during training that won't be available at prediction time.

Common sources:
- Features computed on the full dataset before splitting
- Future data in time-series problems

---

## Questions to Sit With

- When you encode "gender" or "race," what are you doing?
- Who decides what counts as a useful feature?

---

## This Week

- **Demo:** feature transformation pipeline with scikit-learn
- **Practice 3:** feature engineering on a tabular dataset
- **Reading:** TBD — Chapter 3
