"""Content for Quiz 2 (Week 4): covers Week 3's SLOs (03A/03B/03C), plus
three review questions retaking Quiz 1's SLOs (02A/02B/02C) on the same
dataset -- per the syllabus's repeat-questions-between-quizzes policy.

Note: this quiz deliberately does NOT cover Week 4 material -- students get
a full week to study before it's tested (same lag for future quizzes).

Dataset: homeless.csv (the `homeless` DataFrame from class_w03d1/class_w03d2,
already cleaned the same way as in class).
"""

from build_quiz import QuizContent, QuizVersion, Question, blank_table, code_box, blank_line, sketch_box

TITLE = "DATA 202 --- Quiz 2"
SUBTITLE = "Week 4 --- Covering Week 3: Cleaning, Grouping & Plots"

DATASET_INTRO_MD = r"""
## The Dataset: People Experiencing Homelessness

`homeless` contains 100 simulated records of people experiencing
homelessness, cleaned the same way as in Monday's class: standardized city
names, shelter status, and education levels.

**Columns:** `id`, `years_homeless`, `family_size`, `monthly_support_usd`
(numerical) \textperiodcentered\ `name`, `city`, `shelter_status`,
`education_level` (categorical/text)

**First few rows (already cleaned):**
"""

SAMPLE_COLUMNS = [
    "id", "name", "city", "shelter_status", "years_homeless",
    "family_size", "monthly_support_usd", "education_level",
]

ROWS_A = [
    dict(zip(SAMPLE_COLUMNS, [1, "Peter", "New York", "shelter", 6, 1, 186, "None"])),
    dict(zip(SAMPLE_COLUMNS, [5, "Joseph", "San Francisco", "shelter", 2, 5, 37, "Higher"])),
    dict(zip(SAMPLE_COLUMNS, [11, "Miguel", "Chicago", "unsheltered", 9, 5, 195, "Higher"])),
    dict(zip(SAMPLE_COLUMNS, [17, "Joseph", "Los Angeles", "unsheltered", 12, 1, 273, "Higher"])),
    dict(zip(SAMPLE_COLUMNS, [27, "John", "San Francisco", "shelter", 9, 2, 464, "None"])),
]

ROWS_B = [
    dict(zip(SAMPLE_COLUMNS, [2, "Joseph", "Boston", "street", 10, 2, 366, "None"])),
    dict(zip(SAMPLE_COLUMNS, [8, "Lucas", "San Francisco", "shelter temporary", 8, 2, 25, "Primary"])),
    dict(zip(SAMPLE_COLUMNS, [21, "Lucas", "Boston", "unsheltered", 9, 5, 84, "None"])),
    dict(zip(SAMPLE_COLUMNS, [39, "Anna", "Los Angeles", "shelter", 12, 5, 556, "Primary"])),
    dict(zip(SAMPLE_COLUMNS, [59, "David", "San Francisco", "shelter", 11, 2, 264, "Secondary"])),
]


# ---------------------------------------------------------------------------
# Question 1 (SLO 03A) -- cleaning messy text with regex
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 03A)"

Q1_INTRO_A = (
    r"""The raw (uncleaned) `shelter_status` column contains values like
`"SHELTERED"` and `"sheltered"` --- the same status, just different
capitalization. Complete the code below to standardize all of these into
`"shelter"`."""
)
Q1_CODE_A = [
    r'homeless["shelter\_status"] = (',
    r'\hspace*{1.5em}homeless["shelter\_status"]',
    r'\hspace*{1.5em}.str.strip()',
    r'\hspace*{1.5em}.str.' + blank_line("1.6cm") + "()",
    r'\hspace*{1.5em}.str.replace(r"' + blank_line("3.2cm") + '", "shelter", regex=True)',
    ")",
]
Q1_ANSWER_A = (
    'homeless["shelter_status"] = (\n'
    '    homeless["shelter_status"]\n'
    "    .str.strip()\n"
    "    .str.lower()\n"
    '    .str.replace(r"^sheltered$", "shelter", regex=True)\n'
    ")"
)

Q1_INTRO_B = (
    r"""The raw (uncleaned) `shelter_status` column also has spacing
variants like `"shelter , pending"`, `"shelter,pending"`, and
`"shelter  ,  pending"` --- the same status, just spaced differently.
Complete the code below (which already lowercases the text) to standardize
all of these into `"shelter pending"`."""
)
Q1_CODE_B = [
    r'homeless["shelter\_status"] = (',
    r'\hspace*{1.5em}homeless["shelter\_status"]',
    r'\hspace*{1.5em}.str.strip()',
    r'\hspace*{1.5em}.str.lower()',
    r'\hspace*{1.5em}.str.replace(r"' + blank_line("4.0cm") + '", "shelter pending", regex=True)',
    ")",
]
Q1_ANSWER_B = (
    'homeless["shelter_status"] = (\n'
    '    homeless["shelter_status"]\n'
    "    .str.strip()\n"
    "    .str.lower()\n"
    r'    .str.replace(r"shelter\s*,\s*pending", "shelter pending", regex=True)' "\n"
    ")"
)


def _q1_question(intro, code_lines, answer_code):
    body = code_box(code_lines)
    answer_md = "Answer:\n```python\n" + answer_code + "\n```"
    return Question(Q1_HEADING, intro, body, answer_md)


# ---------------------------------------------------------------------------
# Question 2 (SLO 03B) -- grouping and aggregating
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 03B)"

Q2_INTRO_A = (
    "Complete the code below to compute the average `monthly_support_usd` "
    "for each `city`, sorted from highest to lowest.\n\n"
    "Then answer: if you set `ascending=True` instead, what would change "
    "about the output?"
)
Q2_CODE_A = [
    "result = (",
    r'\hspace*{1.5em}homeless.groupby("' + blank_line("2.2cm") + '")["monthly\\_support\\_usd"]',
    r"\hspace*{1.5em}." + blank_line("1.6cm") + "()",
    r"\hspace*{1.5em}.reset\_index()",
    r'\hspace*{1.5em}.sort\_values("monthly\_support\_usd", ascending=' + blank_line("1.4cm") + ")",
    ")",
]
Q2_CODE_ANSWER_A = (
    'result = (\n'
    '    homeless.groupby("city")["monthly_support_usd"]\n'
    "    .mean()\n"
    "    .reset_index()\n"
    '    .sort_values("monthly_support_usd", ascending=False)\n'
    ")"
)
Q2_TEXT_ANSWER_A = (
    "With `ascending=True`, cities would be sorted from LOWEST average to "
    "HIGHEST instead of highest to lowest."
)

Q2_INTRO_B = (
    "Complete the code below to compute, for each `education_level`, both "
    "the number of people and the average `years_homeless`, using named "
    "aggregation.\n\n"
    'Then answer: if you used `"median"` instead of `"mean"` for '
    "`avg_years`, would the result be more or less sensitive to one "
    "extremely high outlier in `years_homeless`?"
)
Q2_CODE_B = [
    r'result = homeless.groupby("' + blank_line("3.0cm") + '").agg(',
    r'\hspace*{1.5em}n\_people=("id", "count"),',
    r'\hspace*{1.5em}avg\_years=("' + blank_line("2.6cm") + '", "' + blank_line("1.3cm") + '"),',
    ")",
]
Q2_CODE_ANSWER_B = (
    'result = homeless.groupby("education_level").agg(\n'
    '    n_people=("id", "count"),\n'
    '    avg_years=("years_homeless", "mean"),\n'
    ")"
)
Q2_TEXT_ANSWER_B = (
    "Median would be LESS sensitive to the outlier (it resists extreme "
    "values); mean would be pulled toward the outlier."
)


def _q2_question(intro, code_lines, code_answer, text_answer):
    body = code_box(code_lines)
    answer_md = "Answer:\n```python\n" + code_answer + "\n```\n\n" + text_answer
    return Question(Q2_HEADING, intro, body, answer_md)


# ---------------------------------------------------------------------------
# Question 3 (SLO 03C) -- matching a question to a plot type
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 03C)"
Q3_INTRO = (
    "For each question below about the `homeless` data, name the best plot "
    "type (Histogram / Scatter / Line / Bar) and which column(s) you'd map "
    "to x (and y, if relevant)."
)

Q3_ROWS_A = [
    ("What's the distribution of `monthly_support_usd` across all people?",
     "Histogram -- x=monthly_support_usd"),
    ("How do `years_homeless` and `monthly_support_usd` relate to each other?",
     "Scatter -- x=years_homeless, y=monthly_support_usd"),
    ("How does average `monthly_support_usd` change as `years_homeless` increases?",
     "Line -- x=years_homeless, y=avg(monthly_support_usd)"),
    ("How does average `monthly_support_usd` compare across `city` values?",
     "Bar -- x=city, y=avg(monthly_support_usd)"),
]

Q3_ROWS_B = [
    ("What's the distribution of `years_homeless` across all people?",
     "Histogram -- x=years_homeless"),
    ("How do `family_size` and `monthly_support_usd` relate to each other?",
     "Scatter -- x=family_size, y=monthly_support_usd"),
    ("How does average `family_size` change as `years_homeless` increases?",
     "Line -- x=years_homeless, y=avg(family_size)"),
    ("How does average `years_homeless` compare across `shelter_status` values?",
     "Bar -- x=shelter_status, y=avg(years_homeless)"),
]


def _q3_question(rows):
    # blank_table is raw LaTeX, not pandoc markdown -- strip the markdown
    # backticks used in `rows` (kept for the plain-markdown answer key below)
    # since they'd otherwise show up as literal backtick characters.
    body = blank_table(
        given_cols=[("Question", "9cm", False)],
        blank_cols=[("Plot Type", "2.3cm"), ("Column(s)", "2.3cm")],
        rows=[[q.replace("`", "")] for q, _a in rows],
    )
    answer_lines = ["| Question | Answer |", "|---|---|"]
    for q, a in rows:
        answer_lines.append(f"| {q} | {a} |")
    return Question(Q3_HEADING, Q3_INTRO, body, "\n".join(answer_lines))


# ---------------------------------------------------------------------------
# Question 4 (SLO 02A) -- REVIEW from Quiz 1: Access / Add / Delete
# ---------------------------------------------------------------------------

Q4_HEADING = "Question 4 (SLO 02A) --- Review from Quiz 1"
Q4_INTRO = (
    "For each command below, identify whether it **Accesses**, **Adds**, or "
    "**Deletes** data, and whether it operates on a **Row** or a **Column**."
)

Q4_ITEMS_A = [
    ('homeless["monthly_support_usd"]', "Access -- Column"),
    ('homeless["high_support"] = homeless["monthly_support_usd"] > 400', "Add -- Column"),
    ('homeless = pd.concat([homeless, pd.DataFrame([new_row])], ignore_index=True)', "Add -- Row"),
    ('homeless = homeless[homeless["shelter_status"] != "street"]', "Delete -- Row(s)"),
    ('homeless = homeless.drop(columns=["notes"])', "Delete -- Column"),
]

Q4_ITEMS_B = [
    ('homeless["years_homeless"]', "Access -- Column"),
    ('homeless["long_term"] = homeless["years_homeless"] > 10', "Add -- Column"),
    ('homeless = pd.concat([homeless, pd.DataFrame([new_row])], ignore_index=True)', "Add -- Row"),
    ('homeless = homeless[homeless["city"] != "Boston"]', "Delete -- Row(s)"),
    ('homeless = homeless.drop(columns=["family_size"])', "Delete -- Column"),
]


def _q4_question(items):
    rows = [[str(i), cmd] for i, (cmd, _ans) in enumerate(items, start=1)]
    body = blank_table(
        given_cols=[("#", None, False), ("Command", "8.3cm", True)],
        blank_cols=[("Access / Add / Delete?", "2.6cm"), ("Row(s) or Column?", "2.6cm")],
        rows=rows,
    )
    answer_lines = ["| # | Command | Answer |", "|---|---|---|"]
    for i, (cmd, ans) in enumerate(items, start=1):
        answer_lines.append(f"| {i} | `{cmd}` | {ans} |")
    return Question(Q4_HEADING, Q4_INTRO, body, "\n".join(answer_lines))


# ---------------------------------------------------------------------------
# Question 5 (SLO 02B) -- REVIEW from Quiz 1: filter + sort
# ---------------------------------------------------------------------------

Q5_HEADING = "Question 5 (SLO 02B) --- Review from Quiz 1"

Q5_INTRO_A = (
    r"""Complete the code below to select all people with `shelter_status`
equal to **"street"** and **more than 10 years homeless**, sorted by
`years_homeless` from highest to lowest.

*Remember: the filter condition still goes inside the square brackets and
must reference* `homeless` *again, e.g.* `homeless[homeless["Column"] ...]`."""
)
Q5_ANSWER_A = (
    'result = homeless[(homeless["shelter_status"] == "street") & (homeless["years_homeless"] > 10)]\n'
    'result = result.sort_values("years_homeless", ascending=False)'
)

Q5_INTRO_B = (
    r"""Complete the code below to select all people in **"San Francisco"**
with `monthly_support_usd` **below 100**, sorted by `monthly_support_usd`
from lowest to highest.

*Remember: the filter condition still goes inside the square brackets and
must reference* `homeless` *again, e.g.* `homeless[homeless["Column"] ...]`."""
)
Q5_ANSWER_B = (
    'result = homeless[(homeless["city"] == "San Francisco") & (homeless["monthly_support_usd"] < 100)]\n'
    'result = result.sort_values("monthly_support_usd", ascending=True)'
)


def _q5_question(intro, answer_code):
    body = code_box([
        "result = homeless[",
        r"\hspace*{1.5em}" + blank_line("0.6\\linewidth"),
        "]",
        r'result = result.sort\_values("' + blank_line("2.6cm") + '", ascending=' + blank_line("1.6cm") + ")",
        "print(len(result))",
    ])
    answer_md = "Answer:\n```python\n" + answer_code + "\n```"
    return Question(Q5_HEADING, intro, body, answer_md)


# ---------------------------------------------------------------------------
# Question 6 (SLO 02C) -- REVIEW from Quiz 1: encoding table + sketch
# ---------------------------------------------------------------------------

Q6_HEADING = "Question 6 (SLO 02C) --- Review from Quiz 1"
Q6_INTRO = r"""Available visual channels: \texttt{x}, \texttt{y}, \texttt{color},
\texttt{size}, \texttt{symbol}, \texttt{facet\_col}.

As on Quiz 1: since this is a paper quiz, \texttt{color} isn't something you
can sketch in pencil --- the code below uses \texttt{symbol} instead,
mapping a categorical column to different \emph{marker shapes} (e.g.
$\times$, $\bigcirc$, $\triangle$) rather than colors.

For the code below, fill in the table: for each visual channel it uses,
name the column mapped to it and say whether that column is Numerical or
Categorical."""

Q6_SKETCH_PROMPT = (
    "In the space below, sketch what you expect this chart to look like. "
    "Label your axes. You don't need exact data --- just show the general "
    r"pattern (point cloud, marker shapes ($\times$/$\bigcirc$/$\triangle$) "
    "for groups, varying point sizes)."
)

Q6_CODE_A = [
    r'px.scatter(homeless, x="years\_homeless", y="monthly\_support\_usd",',
    r'\hspace*{1.5em}symbol="shelter\_status", size="family\_size",',
    r'\hspace*{1.5em}title="Years Homeless vs. Monthly Support")',
]
Q6_ANSWERS_A = [
    ("x-axis", "years_homeless -- Numerical"),
    ("y-axis", "monthly_support_usd -- Numerical"),
    ("symbol", "shelter_status -- Categorical"),
    ("size", "family_size -- Numerical"),
]
Q6_CODE_PLAIN_A = (
    'px.scatter(homeless, x="years_homeless", y="monthly_support_usd",\n'
    '           symbol="shelter_status", size="family_size",\n'
    '           title="Years Homeless vs. Monthly Support")'
)

Q6_CODE_B = [
    r'px.scatter(homeless, x="family\_size", y="monthly\_support\_usd",',
    r'\hspace*{1.5em}symbol="education\_level", size="years\_homeless",',
    r'\hspace*{1.5em}title="Family Size vs. Monthly Support")',
]
Q6_ANSWERS_B = [
    ("x-axis", "family_size -- Numerical"),
    ("y-axis", "monthly_support_usd -- Numerical"),
    ("symbol", "education_level -- Categorical"),
    ("size", "years_homeless -- Numerical"),
]
Q6_CODE_PLAIN_B = (
    'px.scatter(homeless, x="family_size", y="monthly_support_usd",\n'
    '           symbol="education_level", size="years_homeless",\n'
    '           title="Family Size vs. Monthly Support")'
)


def _q6_question(code_lines, answers, code_plain):
    body = (
        code_box(code_lines)
        + "\n"
        + blank_table(
            given_cols=[("Visual Channel", "3.5cm", False)],
            blank_cols=[("Column Used", "3.5cm"), ("Data Type (Numerical / Categorical)", "5cm")],
            rows=[[ch] for ch, _ans in answers],
        )
        + "\n\n"
        + Q6_SKETCH_PROMPT
        + "\n\n"
        + sketch_box()
    )
    answer_lines = ["```python", code_plain, "```", "", "| Channel | Answer |", "|---|---|"]
    for ch, ans in answers:
        answer_lines.append(f"| {ch} | {ans} |")
    answer_lines.append("")
    answer_lines.append("Plus a blank sketch box for the student to draw their prediction of the chart.")
    return Question(Q6_HEADING, Q6_INTRO, body, "\n".join(answer_lines))


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
                _q1_question(Q1_INTRO_A, Q1_CODE_A, Q1_ANSWER_A),
                _q2_question(Q2_INTRO_A, Q2_CODE_A, Q2_CODE_ANSWER_A, Q2_TEXT_ANSWER_A),
                _q3_question(Q3_ROWS_A),
                _q4_question(Q4_ITEMS_A),
                _q5_question(Q5_INTRO_A, Q5_ANSWER_A),
                _q6_question(Q6_CODE_A, Q6_ANSWERS_A, Q6_CODE_PLAIN_A),
            ],
        ),
        "B": QuizVersion(
            rows=ROWS_B,
            questions=[
                _q1_question(Q1_INTRO_B, Q1_CODE_B, Q1_ANSWER_B),
                _q2_question(Q2_INTRO_B, Q2_CODE_B, Q2_CODE_ANSWER_B, Q2_TEXT_ANSWER_B),
                _q3_question(Q3_ROWS_B),
                _q4_question(Q4_ITEMS_B),
                _q5_question(Q5_INTRO_B, Q5_ANSWER_B),
                _q6_question(Q6_CODE_B, Q6_ANSWERS_B, Q6_CODE_PLAIN_B),
            ],
        ),
    },
)
