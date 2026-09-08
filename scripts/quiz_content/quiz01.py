"""Content for Quiz 1 (Week 2): DataFrame Basics & Visual Encodings.
Dataset: product_sales.csv (the `sales` DataFrame from class_w02d2).
SLOs covered: 02A (access/add/delete rows+cols), 02B (filter+sort), 02C
(visual encodings).
"""

from build_quiz import QuizContent, QuizVersion, Question, blank_table, code_box, blank_line, sketch_box

TITLE = "DATA 202 --- Quiz 1"
SUBTITLE = "Week 2 --- DataFrame Basics & Visual Encodings"

DATASET_INTRO_MD = r"""
## The Dataset: Product Sales

`sales` contains 50 simulated products. Each row describes one product's
performance: how much it sold, how it was advertised, and how profitable
it was.

**Columns:** `Product ID`, `Sales`, `Units Sold`, `Profit`, `Advertising Spend`
(numerical) \textperiodcentered\ `Category`, `Season`, `Supplier` (categorical)

**First few rows:**
"""

SAMPLE_COLUMNS = [
    "Product ID", "Sales", "Units Sold", "Profit", "Advertising Spend",
    "Category", "Season", "Supplier",
]

ROWS_A = [
    dict(zip(SAMPLE_COLUMNS, ["P001", 99268, 684, 17337, 5581, "Electronics", "Summer", "Supplier A"])),
    dict(zip(SAMPLE_COLUMNS, ["P003", 71613, 924, 3832, 2788, "Furniture", "Winter", "Supplier A"])),
    dict(zip(SAMPLE_COLUMNS, ["P006", 72993, 1239, 10683, 6070, "Clothing", "Summer", "Supplier A"])),
    dict(zip(SAMPLE_COLUMNS, ["P011", 46589, 743, 1109, 6384, "Furniture", "Fall", "Supplier B"])),
    dict(zip(SAMPLE_COLUMNS, ["P026", 98755, 1206, 18346, 3195, "Electronics", "Spring", "Supplier C"])),
]

ROWS_B = [
    dict(zip(SAMPLE_COLUMNS, ["P014", 36921, 1391, 8582, 5925, "Electronics", "Spring", "Supplier B"])),
    dict(zip(SAMPLE_COLUMNS, ["P020", 33496, 1181, -4775, 8432, "Furniture", "Summer", "Supplier A"])),
    dict(zip(SAMPLE_COLUMNS, ["P036", 32560, 968, 9691, 4040, "Clothing", "Winter", "Supplier B"])),
    dict(zip(SAMPLE_COLUMNS, ["P041", 58147, 1155, 7637, 3282, "Furniture", "Fall", "Supplier B"])),
    dict(zip(SAMPLE_COLUMNS, ["P047", 82811, 698, 8838, 4530, "Clothing", "Summer", "Supplier C"])),
]


# ---------------------------------------------------------------------------
# Question 1 (SLO 02A) -- identify Access / Add / Delete, Row / Column
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 02A)"
Q1_INTRO = (
    "For each command below, identify whether it **Accesses**, **Adds**, or "
    "**Deletes** data, and whether it operates on a **Row** or a **Column**."
)

Q1_ITEMS_A = [
    ('sales["Advertising Spend"]', "Access -- Column"),
    ('sales["Discount"] = sales["Sales"] * 0.1', "Add -- Column"),
    ('sales = pd.concat([sales, pd.DataFrame([new_row])], ignore_index=True)', "Add -- Row"),
    ('sales = sales[sales["Category"] != "Furniture"]', "Delete -- Row(s)"),
    ('sales = sales.drop(columns=["Returns"])', "Delete -- Column"),
]

Q1_ITEMS_B = [
    ('sales["Units Sold"]', "Access -- Column"),
    ('sales["Margin"] = sales["Profit"] / sales["Sales"]', "Add -- Column"),
    ('sales = pd.concat([sales, pd.DataFrame([new_row])], ignore_index=True)', "Add -- Row"),
    ('sales = sales[sales["Category"] != "Electronics"]', "Delete -- Row(s)"),
    ('sales = sales.drop(columns=["Supplier"])', "Delete -- Column"),
]


def _q1_question(items):
    rows = [[str(i), cmd] for i, (cmd, _ans) in enumerate(items, start=1)]
    body = blank_table(
        given_cols=[("#", None, False), ("Command", "8.3cm", True)],
        blank_cols=[("Access / Add / Delete?", "2.6cm"), ("Row(s) or Column?", "2.6cm")],
        rows=rows,
    )
    answer_lines = ["| # | Command | Answer |", "|---|---|---|"]
    for i, (cmd, ans) in enumerate(items, start=1):
        answer_lines.append(f"| {i} | `{cmd}` | {ans} |")
    return Question(Q1_HEADING, Q1_INTRO, body, "\n".join(answer_lines))


# ---------------------------------------------------------------------------
# Question 2 (SLO 02B) -- complete the filter + sort
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 02B)"

Q2_INTRO_A = (
    r"""Complete the code below to select all products in the **Electronics**
category with **Advertising Spend over \$5,000**, sorted by Advertising
Spend from highest to lowest.

*Remember: the filter condition still goes inside the square brackets and
must reference* `sales` *again, e.g.* `sales[sales["Column"] ...]`."""
)
Q2_ANSWER_A = (
    'result = sales[(sales["Category"] == "Electronics") & (sales["Advertising Spend"] > 5000)]\n'
    'result = result.sort_values("Advertising Spend", ascending=False)'
)

Q2_INTRO_B = (
    r"""Complete the code below to select all products in the **Furniture**
category that lost money (**Profit below \$0**), sorted by Profit from
lowest to highest.

*Remember: the filter condition still goes inside the square brackets and
must reference* `sales` *again, e.g.* `sales[sales["Column"] ...]`."""
)
Q2_ANSWER_B = (
    'result = sales[(sales["Category"] == "Furniture") & (sales["Profit"] < 0)]\n'
    'result = result.sort_values("Profit", ascending=True)'
)


def _q2_question(intro_md, answer_code):
    body = code_box([
        "result = sales[",
        r"\hspace*{1.5em}" + blank_line("0.6\\linewidth"),
        "]",
        r'result = result.sort\_values("' + blank_line("2.6cm") + '", ascending=' + blank_line("1.6cm") + ")",
        "print(len(result))",
    ])
    answer_md = "Answer:\n```python\n" + answer_code + "\n```"
    return Question(Q2_HEADING, intro_md, body, answer_md)


# ---------------------------------------------------------------------------
# Question 3 (SLO 02C) -- encoding table + sketch (symbol, not color -- paper quiz)
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 02C)"
Q3_INTRO = r"""Available visual channels: \texttt{x}, \texttt{y}, \texttt{color},
\texttt{size}, \texttt{symbol}, \texttt{facet\_col}.

Since this is a paper quiz, \texttt{color} isn't something you can sketch
in pencil --- the code below uses \texttt{symbol} instead, which maps a
categorical column to different \emph{marker shapes} (e.g. $\times$,
$\bigcirc$, $\triangle$) rather than colors.

For the code below, fill in the table: for each visual channel it uses,
name the column mapped to it and say whether that column is Numerical or
Categorical."""

SKETCH_PROMPT = (
    "In the space below, sketch what you expect this chart to look like. "
    "Label your axes. You don't need exact data --- just show the general "
    r"pattern (point cloud, marker shapes ($\times$/$\bigcirc$/$\triangle$) "
    "for groups, varying point sizes)."
)

Q3_CODE_A = [
    'px.scatter(sales, x="Advertising Spend", y="Profit",',
    r'\hspace*{1.5em}symbol="Category", size="Units Sold",',
    r'\hspace*{1.5em}title="Advertising Spend vs. Profit")',
]
Q3_ANSWERS_A = [
    ("x-axis", "Advertising Spend -- Numerical"),
    ("y-axis", "Profit -- Numerical"),
    ("symbol", "Category -- Categorical"),
    ("size", "Units Sold -- Numerical"),
]
Q3_CODE_PLAIN_A = (
    'px.scatter(sales, x="Advertising Spend", y="Profit",\n'
    '           symbol="Category", size="Units Sold",\n'
    '           title="Advertising Spend vs. Profit")'
)

Q3_CODE_B = [
    'px.scatter(sales, x="Advertising Spend", y="Sales",',
    r'\hspace*{1.5em}symbol="Season", size="Units Sold",',
    r'\hspace*{1.5em}title="Advertising Spend vs. Sales")',
]
Q3_ANSWERS_B = [
    ("x-axis", "Advertising Spend -- Numerical"),
    ("y-axis", "Sales -- Numerical"),
    ("symbol", "Season -- Categorical"),
    ("size", "Units Sold -- Numerical"),
]
Q3_CODE_PLAIN_B = (
    'px.scatter(sales, x="Advertising Spend", y="Sales",\n'
    '           symbol="Season", size="Units Sold",\n'
    '           title="Advertising Spend vs. Sales")'
)


def _q3_question(code_lines, answers, code_plain):
    body = (
        code_box(code_lines)
        + "\n"
        + blank_table(
            given_cols=[("Visual Channel", "3.5cm", False)],
            blank_cols=[("Column Used", "3.5cm"), ("Data Type (Numerical / Categorical)", "5cm")],
            rows=[[ch] for ch, _ans in answers],
        )
        + "\n\n"
        + SKETCH_PROMPT
        + "\n\n"
        + sketch_box()
    )
    answer_lines = ["```python", code_plain, "```", "", "| Channel | Answer |", "|---|---|"]
    for ch, ans in answers:
        answer_lines.append(f"| {ch} | {ans} |")
    answer_lines.append("")
    answer_lines.append("Plus a blank sketch box for the student to draw their prediction of the chart.")
    return Question(Q3_HEADING, Q3_INTRO, body, "\n".join(answer_lines))


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------

CONTENT = QuizContent(
    title=TITLE,
    subtitle=SUBTITLE,
    dataset_intro_md=DATASET_INTRO_MD,
    sample_columns=SAMPLE_COLUMNS,
    versions={
        "A": QuizVersion(
            rows=ROWS_A,
            questions=[
                _q1_question(Q1_ITEMS_A),
                _q2_question(Q2_INTRO_A, Q2_ANSWER_A),
                _q3_question(Q3_CODE_A, Q3_ANSWERS_A, Q3_CODE_PLAIN_A),
            ],
        ),
        "B": QuizVersion(
            rows=ROWS_B,
            questions=[
                _q1_question(Q1_ITEMS_B),
                _q2_question(Q2_INTRO_B, Q2_ANSWER_B),
                _q3_question(Q3_CODE_B, Q3_ANSWERS_B, Q3_CODE_PLAIN_B),
            ],
        ),
    },
)
