---
marp: true
title: "Week 5: Logistic Regression & Classification"
theme: default
paginate: true
---

# Logistic Regression & Classification

### DATA 202 · Week 5

---

## The Classification Task

**Goal:** predict a discrete category (class) from input features.

Examples: spam/not spam, fraud/not fraud, diagnosis positive/negative

---

## From Regression to Classification

Linear regression → unbounded output

Logistic regression → squash output to [0, 1] via the **sigmoid**:

$$P(y=1 \mid x) = \frac{1}{1 + e^{-(\beta_0 + \beta^T x)}}$$

---

## Thresholding

Output is a probability. We choose a **threshold** (default: 0.5):

$$\hat{y} = \begin{cases} 1 & \text{if } P \geq \theta \\ 0 & \text{otherwise} \end{cases}$$

Threshold is a **design decision**, not a fact.

---

## The Confusion Matrix

|  | Predicted + | Predicted − |
|--|--|--|
| **Actual +** | TP | FN |
| **Actual −** | FP | TN |

- **Precision:** TP / (TP + FP)
- **Recall:** TP / (TP + FN)
- **F1:** harmonic mean of precision and recall

---

## Precision vs. Recall Tradeoff

Lowering the threshold → more positives predicted → higher recall, lower precision

Which matters more depends on the **cost of each error type**.

---

## Multiclass Classification

- One-vs-Rest: train one classifier per class
- Softmax regression: generalize logistic to K classes

---

## Questions to Sit With

- Who bears the cost of a false positive? A false negative?
- What does it mean to predict a socially constructed category?

---

## This Week

- **Demo:** logistic regression + confusion matrix
- **Lab 5:** classification on a real-world dataset
- **Reading:** TBD — Chapter 5
