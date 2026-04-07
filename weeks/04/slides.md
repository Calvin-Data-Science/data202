---
marp: true
title: "Week 4: Linear Regression"
theme: default
paginate: true
---

# Linear Regression

### DATA 202 · Week 4

---

## The Regression Task

**Goal:** predict a continuous numeric output from input features.

$$\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p$$

---

## Fitting: Least Squares

Minimize the **residual sum of squares**:

$$\text{RSS} = \sum_{i=1}^n (y_i - \hat{y}_i)^2$$

---

## Interpreting Coefficients

- $\beta_j$: expected change in $y$ per unit increase in $x_j$, holding others constant
- Only meaningful when assumptions hold
- Magnitude depends on scale of features

---

## Model Evaluation

- **R²:** proportion of variance explained
- **RMSE:** root mean squared error (same units as target)
- **Residual plots:** check assumptions visually

---

## Regularization

| Method | Penalty | Effect |
|--------|---------|--------|
| Ridge | $\lambda \sum \beta_j^2$ | Shrinks all coefficients |
| Lasso | $\lambda \sum |\beta_j|$ | Sparse; zeros out some |

---

## When Linear Regression Fails

- Non-linear relationships
- Heavily skewed targets
- Many correlated features
- Non-constant variance (heteroscedasticity)

---

## Questions to Sit With

- "Statistical significance" — significant to whom?
- What does a model coefficient mean for a policy decision?

---

## This Week

- **Demo:** linear and ridge regression with scikit-learn
- **Lab 4:** regression on a housing/salary dataset
- **Reading:** TBD — Chapter 4
