# DATA 202 --- Quiz 1

Week 2 --- DataFrame Basics & Visual Encodings

*(Source content for the printed quiz. Both versions (A/B) are shown
below. Built via `python scripts/build_quiz.py 1`, which
generates `quiz01_A.pdf` and `quiz01_B.pdf`
for printing. This file is NOT published on the course site -- see
`_config.yml` exclude list.)*

## The Dataset: Product Sales

`sales` contains 50 simulated products. Each row describes one product's
performance: how much it sold, how it was advertised, and how profitable
it was.

**Columns:** `Product ID`, `Sales`, `Units Sold`, `Profit`, `Advertising Spend`
(numerical) \textperiodcentered\ `Category`, `Season`, `Supplier` (categorical)

**First few rows:**

**Version A sample rows:**

| Product ID | Sales | Units Sold | Profit | Advertising Spend | Category | Season | Supplier |
|---|---|---|---|---|---|---|---|
| P001 | 99268 | 684 | 17337 | 5581 | Electronics | Summer | Supplier A |
| P003 | 71613 | 924 | 3832 | 2788 | Furniture | Winter | Supplier A |
| P006 | 72993 | 1239 | 10683 | 6070 | Clothing | Summer | Supplier A |
| P011 | 46589 | 743 | 1109 | 6384 | Furniture | Fall | Supplier B |
| P026 | 98755 | 1206 | 18346 | 3195 | Electronics | Spring | Supplier C |

**Version B sample rows:**

| Product ID | Sales | Units Sold | Profit | Advertising Spend | Category | Season | Supplier |
|---|---|---|---|---|---|---|---|
| P014 | 36921 | 1391 | 8582 | 5925 | Electronics | Spring | Supplier B |
| P020 | 33496 | 1181 | -4775 | 8432 | Furniture | Summer | Supplier A |
| P036 | 32560 | 968 | 9691 | 4040 | Clothing | Winter | Supplier B |
| P041 | 58147 | 1155 | 7637 | 3282 | Furniture | Fall | Supplier B |
| P047 | 82811 | 698 | 8838 | 4530 | Clothing | Summer | Supplier C |

## Question 1 (SLO 02A)

**Version A:**

| # | Command | Answer |
|---|---|---|
| 1 | `sales["Advertising Spend"]` | Access -- Column |
| 2 | `sales["Discount"] = sales["Sales"] * 0.1` | Add -- Column |
| 3 | `sales = pd.concat([sales, pd.DataFrame([new_row])], ignore_index=True)` | Add -- Row |
| 4 | `sales = sales[sales["Category"] != "Furniture"]` | Delete -- Row(s) |
| 5 | `sales = sales.drop(columns=["Returns"])` | Delete -- Column |

**Version B:**

| # | Command | Answer |
|---|---|---|
| 1 | `sales["Units Sold"]` | Access -- Column |
| 2 | `sales["Margin"] = sales["Profit"] / sales["Sales"]` | Add -- Column |
| 3 | `sales = pd.concat([sales, pd.DataFrame([new_row])], ignore_index=True)` | Add -- Row |
| 4 | `sales = sales[sales["Category"] != "Electronics"]` | Delete -- Row(s) |
| 5 | `sales = sales.drop(columns=["Supplier"])` | Delete -- Column |

## Question 2 (SLO 02B)

**Version A:**

Answer:
```python
result = sales[(sales["Category"] == "Electronics") & (sales["Advertising Spend"] > 5000)]
result = result.sort_values("Advertising Spend", ascending=False)
```

**Version B:**

Answer:
```python
result = sales[(sales["Category"] == "Furniture") & (sales["Profit"] < 0)]
result = result.sort_values("Profit", ascending=True)
```

## Question 3 (SLO 02C)

**Version A:**

```python
px.scatter(sales, x="Advertising Spend", y="Profit",
           symbol="Category", size="Units Sold",
           title="Advertising Spend vs. Profit")
```

| Channel | Answer |
|---|---|
| x-axis | Advertising Spend -- Numerical |
| y-axis | Profit -- Numerical |
| symbol | Category -- Categorical |
| size | Units Sold -- Numerical |

Plus a blank sketch box for the student to draw their prediction of the chart.

**Version B:**

```python
px.scatter(sales, x="Advertising Spend", y="Sales",
           symbol="Season", size="Units Sold",
           title="Advertising Spend vs. Sales")
```

| Channel | Answer |
|---|---|
| x-axis | Advertising Spend -- Numerical |
| y-axis | Sales -- Numerical |
| symbol | Season -- Categorical |
| size | Units Sold -- Numerical |

Plus a blank sketch box for the student to draw their prediction of the chart.

