---
marp: true
title: "Week 6: Model Evaluation & Validation"
theme: default
paginate: true
---

# Model Evaluation & Validation

### DATA 202 · Week 6

---

## The Core Problem: Overfitting

A model that memorizes training data performs perfectly on it—then fails on new data.

> Good performance on training data ≠ good generalization.

---

## The Bias-Variance Tradeoff

- **Bias:** error from wrong assumptions → underfitting
- **Variance:** error from sensitivity to training data → overfitting
- **Goal:** find the sweet spot

---

## Train / Validation / Test Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

Never touch the test set until final evaluation.

---

## Cross-Validation

Split training data into *k* folds; rotate which fold is held out.

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X_train, y_train, cv=5)
```

Gives a more reliable estimate of generalization.

---

## Learning Curves

Plot training vs. validation error as training set size grows.

- High bias: both errors are high
- High variance: large gap between train and val error

---

## Model Selection

Use validation performance to choose:
- Hyperparameters (e.g., regularization strength)
- Model family
- Feature set

---

## Questions to Sit With

- "Generalization" to what population? Collected when?
- How are evaluation results selectively reported in practice?

---

## This Week

- **Demo:** cross-validation and learning curves
- **Lab 6:** model selection and hyperparameter tuning
- **Reading:** TBD — Chapter 6
