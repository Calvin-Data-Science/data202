---
marp: true
title: "Week 12: Fairness & Bias in ML"
theme: default
paginate: true
---

# Fairness & Bias in ML

### DATA 202 · Week 12

---

## What Is Algorithmic Bias?

A system produces outcomes that are systematically less accurate or equitable for some groups than others.

This is not an edge case. It is the default when data reflects historical inequity.

---

## Sources of Bias

- **Data bias:** who was included/excluded in training data
- **Label bias:** human annotators bring their own biases
- **Feedback loops:** predictions shape future data
- **Proxy features:** "neutral" features encode protected attributes

---

## Formal Fairness Criteria

| Criterion | Definition |
|---|---|
| Demographic parity | Same positive rate across groups |
| Equal opportunity | Same TPR across groups |
| Calibration | Predicted probabilities are accurate per group |

---

## The Impossibility Result

Several fairness criteria are **mathematically incompatible** when base rates differ across groups.

> You cannot satisfy all of them at once. Every choice is a value judgment.

---

## Measuring Disparity

```python
# Evaluate metrics per group
for group in df['race'].unique():
    subset = df[df['race'] == group]
    print(group, accuracy_score(subset.y, subset.pred))
```

---

## Interventions

- **Pre-processing:** rebalance or reweight training data
- **In-processing:** fairness constraints during training
- **Post-processing:** adjust thresholds per group

Each has tradeoffs.

---

## Beyond Metrics

Technical fairness is not the same as justice.

- Who participates in defining fairness?
- Who bears the burden of an "acceptable" error rate?

---

## This Week

- **Demo:** measuring group disparities with a real dataset
- **Lab 12:** fairness audit of a classifier
- **Reading:** TBD — Barocas et al. or similar
