---
marp: true
title: "Week 2: Data Wrangling & Exploration"
theme: default
paginate: true
---

# Data Wrangling & Exploration

### DATA 202 · Week 2

---

## What is "Data Wrangling"?

The process of transforming raw data into a form suitable for analysis.

Often called: *data cleaning*, *data munging*, *ETL*

It takes **50–80% of a data scientist's time** in practice.

---

## The pandas Toolkit

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.head()
df.info()
df.describe()
```

---

## Common Issues in Raw Data

- Missing values (`NaN`)
- Duplicate rows
- Inconsistent types or formats
- Outliers
- Encoding errors

---

## Handling Missing Values

```python
df.isnull().sum()          # count missing per column
df.dropna()                # drop rows with any missing value
df.fillna(df.mean())       # fill with column mean
```

> Every strategy is a choice with consequences.

---

## Exploratory Data Analysis

- Distribution plots (histograms, box plots)
- Correlation heatmaps
- Scatter plots for pairwise relationships
- Target variable analysis

---

## Data Provenance

- Where did the data come from?
- Who collected it, when, and how?
- What was included or excluded?

---

## Questions to Sit With

- Whose decisions are baked into a "cleaned" dataset?
- What does it mean to call something an outlier?

---

## This Week

- **Demo:** pandas data cleaning walkthrough
- **Lab 2:** explore a real-world messy dataset
- **Reading:** TBD — Chapter 2
