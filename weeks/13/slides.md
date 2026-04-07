---
marp: true
title: "Week 13: Interpretability & Explainability"
theme: default
paginate: true
---

# Interpretability & Explainability

### DATA 202 · Week 13

---

## Why Does This Matter?

- Legal requirements (GDPR right to explanation)
- Debugging and trust
- Accountability when models affect people's lives
- Scientific insight

---

## Interpretability vs. Explainability

| | |
|---|---|
| **Interpretable model** | Transparent by design (linear model, shallow tree) |
| **Explainable model** | Post-hoc explanation of a black-box model |

---

## Intrinsically Interpretable Models

- Linear regression: coefficients tell the story
- Logistic regression: log-odds interpretation
- Shallow decision trees: visual flowchart

Cost: often less accurate.

---

## LIME

**Local Interpretable Model-agnostic Explanations**

Fit a simple model in the neighborhood of one prediction.

```python
import lime
explainer = lime.lime_tabular.LimeTabularExplainer(X_train)
explanation = explainer.explain_instance(x, model.predict_proba)
```

---

## SHAP

**SHapley Additive exPlanations**

Feature contributions based on cooperative game theory.

```python
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
```

---

## Limits of Explanations

- LIME explanations are **local and unstable**
- SHAP values aggregate — they can hide interactions
- An explanation can be technically correct and still misleading

---

## Questions to Sit With

- Who demands explanations, and who has the power to require them?
- Can a technically accurate explanation still be ethically inadequate?

---

## This Week

- **Demo:** SHAP on a gradient-boosted model
- **Lab 13:** explain and critique a model's decisions
- **Reading:** TBD — Molnar, *Interpretable Machine Learning*
