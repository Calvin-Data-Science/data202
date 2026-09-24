"""Content for Quiz 2 (Week 4): covers Week 3's SLOs (03A/03B/03C), plus
three review questions retaking Quiz 1's SLOs (02A/02B/02C) on this quiz's
dataset -- per the syllabus's repeat-questions-between-quizzes policy.

Note: this quiz deliberately does NOT cover Week 4 material -- students get
a full week to study before it's tested (same lag for future quizzes).

Dataset: a simulated esports `players` table. It is NOT the class's
homeless.csv (or Quiz 1's product_sales.csv), so the quiz tests whether the
Week 3 skills transfer to new data; there is no CSV behind it, only the
sample rows below. The Q1 cleaning patterns deliberately mirror the ones
practiced in class_w03d1 (anchored `^...$` replace; `\\s*,\\s*` spacing).
The sample table at the top shows RAW (uncleaned) rows, because Q1 asks what
cleaning code does to them; Q2-Q6 assume the data has been cleaned.
"""

from build_quiz import (
    QuizContent, QuizVersion, Question,
    blank_table, code_box, blank_line, sketch_box, tex_escape, raw_latex,
)

TITLE = "DATA 202 --- Quiz 2"
SUBTITLE = "Week 4 --- Covering Week 3: Cleaning, Grouping & Plots"

DATASET_INTRO_MD = r"""
## The Dataset: Esports Players

`players` contains simulated records of competitive video game players, one
row per player. The rows below are the **raw** data, exactly as loaded from
the CSV. Question 1 works with this raw data; Questions 2--6 assume `players`
has already been cleaned (standardized city names, ladder status, and skill
levels).

**Columns:** `id`, `years_playing`, `sponsors`, `monthly_earnings_usd`
(numerical) \textperiodcentered\ `handle`, `city`, `ladder_status`,
`skill_level` (categorical/text)

**First few rows (raw --- before any cleaning):**
"""

SAMPLE_COLUMNS = [
    "id", "handle", "city", "ladder_status", "years_playing",
    "sponsors", "monthly_earnings_usd", "skill_level",
]

# Raw rows (uncleaned: mixed case, inconsistent city names, stray spacing).
# Picked so Q1's code visibly does something different to each ladder_status
# variant.
ROWS_A = [
    dict(zip(SAMPLE_COLUMNS, [3, "NOVA", "toronto", "unranked", 10, 4, 422, "ADVANCED"])),
    dict(zip(SAMPLE_COLUMNS, [4, "blaze", "SEOUL.", "CASUAL", 14, 3, 37, "novice"])),
    dict(zip(SAMPLE_COLUMNS, [6, "viper", "L.A.", "ranked , pending", 9, 5, 552, "ADVANCED"])),
    dict(zip(SAMPLE_COLUMNS, [9, "pixel.", "berlin", "Ranked", 13, 1, 74, "expert"])),
    dict(zip(SAMPLE_COLUMNS, [44, "ghost", "NEW-YORK", "RANK", 13, 1, 171, "amateur"])),
]

ROWS_B = [
    dict(zip(SAMPLE_COLUMNS, [15, "kiRA", "NEW-YORK", "Ranked", 14, 4, 579, "ADVANCED"])),
    dict(zip(SAMPLE_COLUMNS, [16, "ZEPHYR", "SEOUL.", "ranked , pending", 10, 4, 286, "AMATEUR"])),
    dict(zip(SAMPLE_COLUMNS, [35, "echo", "berlin", "unranked", 9, 4, 375, "EXPERT"])),
    dict(zip(SAMPLE_COLUMNS, [45, "mochi.", "los Angeles", "RANK", 5, 2, 90, "novice"])),
    dict(zip(SAMPLE_COLUMNS, [49, "NEO", "toronto", "CASUAL", 10, 1, 399, "ADVANCED"])),
]

# Wider than the even split: raw values like "ranked , pending" / "los
# Angeles" don't fit in ~1.8cm. Order follows SAMPLE_COLUMNS: id, handle,
# city, ladder_status, years_playing, sponsors, monthly_earnings_usd,
# skill_level. Sums to 14.4cm + column padding.
SAMPLE_COL_WIDTHS_CM = [0.6, 1.5, 2.1, 2.7, 1.6, 1.5, 2.0, 2.4]


# ---------------------------------------------------------------------------
# Question 1 (SLO 03A) -- reading regex cleaning code (predict what it does)
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 03A)"

Q1_INTRO = (
    "The code below is run on the `ladder_status` column of the **raw** "
    "data shown above."
)

Q1_PROMPT = (
    "What will this code do to the `ladder_status` column? Explain what "
    "each step does, and say what the `ladder_status` values in the rows "
    "above will look like afterward."
)

Q1_CODE_A = (
    'players["ladder_status"] = (\n'
    '    players["ladder_status"]\n'
    "    .str.strip()\n"
    "    .str.lower()\n"
    '    .str.replace(r"^rank$", "ranked", regex=True)\n'
    ")"
)
Q1_ANSWER_A = [
    "`.str.strip()` removes leading/trailing whitespace.",
    '`.str.lower()` lowercases everything (`"Ranked"` → `"ranked"`, '
    '`"CASUAL"` → `"casual"`, `"RANK"` → `"rank"`).',
    '`.str.replace(r"^rank$", "ranked", regex=True)` rewrites values that '
    'are *exactly* `"rank"` to `"ranked"`. The `^` and `$` anchors matter: '
    '`"ranked"` and `"unranked"` both contain `"rank"`, so without them '
    'they would be mangled into `"rankeded"` and `"unrankeded"`.',
    "The result is assigned back to the column.",
]
Q1_AFTER_A = ["unranked", "casual", "ranked , pending", "ranked", "ranked"]

Q1_CODE_B = (
    'players["ladder_status"] = (\n'
    '    players["ladder_status"]\n'
    "    .str.strip()\n"
    "    .str.lower()\n"
    r'    .str.replace(r"ranked\s*,\s*pending", "ranked pending", regex=True)' "\n"
    ")"
)
Q1_ANSWER_B = [
    "`.str.strip()` removes leading/trailing whitespace.",
    '`.str.lower()` lowercases everything (`"Ranked"` → `"ranked"`, '
    '`"CASUAL"` → `"casual"`, `"RANK"` → `"rank"`).',
    r'`.str.replace(r"ranked\s*,\s*pending", "ranked pending", regex=True)` '
    'matches `"ranked"`, then any spaces, a comma, any spaces, then '
    '`"pending"`, and rewrites it as `"ranked pending"` (so '
    '`"ranked , pending"` → `"ranked pending"`).',
    'Nothing here turns `"rank"` into `"ranked"`, so `"RANK"` ends up as '
    '`"rank"`; `"unranked"` is untouched.',
]
Q1_AFTER_B = ["ranked", "ranked pending", "unranked", "rank", "casual"]


def _plain_code_to_latex_lines(code):
    """Turn a plain-text code block into code_box() lines: each 4 leading
    spaces become a 1.5em indent, and the rest is tex_escape'd."""
    lines = []
    for line in code.split("\n"):
        indent = len(line) - len(line.lstrip(" "))
        prefix = r"\hspace*{%.1fem}" % (1.5 * indent / 4) if indent else ""
        lines.append(prefix + tex_escape(line.lstrip(" ")))
    return lines


def _q1_question(raw_rows, code, answer_points, after_values):
    body = (
        code_box(_plain_code_to_latex_lines(code))
        + raw_latex(r"\vspace{2pt}")
        + Q1_PROMPT
        + "\n\n"
        + sketch_box("2.0in")
    )

    answer_lines = ["```python", code, "```", ""]
    answer_lines += [f"- {pt}" for pt in answer_points]
    answer_lines += ["", "| id | ladder_status (raw) | ladder_status (after) |", "|---|---|---|"]
    for row, after in zip(raw_rows, after_values):
        answer_lines.append(f'| {row["id"]} | `{row["ladder_status"]}` | `{after}` |')
    return Question(Q1_HEADING, Q1_INTRO, body, "\n".join(answer_lines))


# ---------------------------------------------------------------------------
# Question 2 (SLO 03B) -- grouping and aggregating
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 03B)"

Q2_INTRO_A = (
    "Complete the code below to compute the average `monthly_earnings_usd` "
    "for each `city`, sorted from highest to lowest."
)
Q2_CODE_A = [
    "result = (",
    r'\hspace*{1.5em}players.groupby("' + blank_line("2.2cm") + '")["monthly\\_earnings\\_usd"]',
    r"\hspace*{1.5em}." + blank_line("1.6cm") + "()",
    r"\hspace*{1.5em}.reset\_index()",
    r'\hspace*{1.5em}.sort\_values("monthly\_earnings\_usd", ascending=' + blank_line("1.4cm") + ")",
    ")",
]
Q2_CODE_ANSWER_A = (
    'result = (\n'
    '    players.groupby("city")["monthly_earnings_usd"]\n'
    "    .mean()\n"
    "    .reset_index()\n"
    '    .sort_values("monthly_earnings_usd", ascending=False)\n'
    ")"
)
Q2_INTRO_B = (
    "Complete the code below to compute, for each `skill_level`, both "
    "the number of players and the average `years_playing`, using named "
    "aggregation.\n\n"
    'Then answer: if you used `"median"` instead of `"mean"` for '
    "`avg_years`, would the result be more or less sensitive to one "
    "extremely high outlier in `years_playing`?"
)
Q2_CODE_B = [
    r'result = players.groupby("' + blank_line("3.0cm") + '").agg(',
    r'\hspace*{1.5em}n\_players=("id", "count"),',
    r'\hspace*{1.5em}avg\_years=("' + blank_line("2.6cm") + '", "' + blank_line("1.3cm") + '"),',
    ")",
]
Q2_CODE_ANSWER_B = (
    'result = players.groupby("skill_level").agg(\n'
    '    n_players=("id", "count"),\n'
    '    avg_years=("years_playing", "mean"),\n'
    ")"
)
Q2_TEXT_ANSWER_B = (
    "Median would be LESS sensitive to the outlier (it resists extreme "
    "values); mean would be pulled toward the outlier."
)


def _q2_question(intro, code_lines, code_answer, text_answer=None):
    body = code_box(code_lines)
    answer_md = "Answer:\n```python\n" + code_answer + "\n```"
    if text_answer:
        answer_md += "\n\n" + text_answer
    return Question(Q2_HEADING, intro, body, answer_md)


# ---------------------------------------------------------------------------
# Question 3 (SLO 03C) -- matching a question to a plot type
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 03C)"
Q3_INTRO = (
    "For each question below about the `players` data, name the best plot "
    "type (Histogram / Scatter / Line / Bar) and which column(s) you'd map "
    "to x (and y, if relevant)."
)

Q3_ROWS_A = [
    ("What's the distribution of `monthly_earnings_usd` across all players?",
     "Histogram -- x=monthly_earnings_usd"),
    ("How do `years_playing` and `monthly_earnings_usd` relate to each other?",
     "Scatter -- x=years_playing, y=monthly_earnings_usd"),
    ("How does average `monthly_earnings_usd` change as `years_playing` increases?",
     "Line -- x=years_playing, y=avg(monthly_earnings_usd)"),
    ("How does average `monthly_earnings_usd` compare across `city` values?",
     "Bar -- x=city, y=avg(monthly_earnings_usd)"),
]

Q3_ROWS_B = [
    ("What's the distribution of `years_playing` across all players?",
     "Histogram -- x=years_playing"),
    ("How do `sponsors` and `monthly_earnings_usd` relate to each other?",
     "Scatter -- x=sponsors, y=monthly_earnings_usd"),
    ("How does average `sponsors` change as `years_playing` increases?",
     "Line -- x=years_playing, y=avg(sponsors)"),
    ("How does average `years_playing` compare across `ladder_status` values?",
     "Bar -- x=ladder_status, y=avg(years_playing)"),
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
    ('players["monthly_earnings_usd"]', "Access -- Column"),
    ('players["high_earner"] = players["monthly_earnings_usd"] > 400', "Add -- Column"),
    ('players = pd.concat([players, pd.DataFrame([new_row])], ignore_index=True)', "Add -- Row"),
    ('players = players[players["ladder_status"] != "casual"]', "Delete -- Row(s)"),
    ('players = players.drop(columns=["skill_level"])', "Delete -- Column"),
]

Q4_ITEMS_B = [
    ('players["years_playing"]', "Access -- Column"),
    ('players["veteran"] = players["years_playing"] > 10', "Add -- Column"),
    ('players = pd.concat([players, pd.DataFrame([new_row])], ignore_index=True)', "Add -- Row"),
    ('players = players[players["city"] != "Berlin"]', "Delete -- Row(s)"),
    ('players = players.drop(columns=["sponsors"])', "Delete -- Column"),
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
    r"""Complete the code below to select all players with `ladder_status`
equal to **"casual"** and **more than 10 years playing**, sorted by
`years_playing` from highest to lowest.

*Remember: the filter condition still goes inside the square brackets and
must reference* `players` *again, e.g.* `players[players["Column"] ...]`."""
)
Q5_ANSWER_A = (
    'result = players[(players["ladder_status"] == "casual") & (players["years_playing"] > 10)]\n'
    'result = result.sort_values("years_playing", ascending=False)'
)

Q5_INTRO_B = (
    r"""Complete the code below to select all players in **"Seoul"**
with `monthly_earnings_usd` **below 100**, sorted by `monthly_earnings_usd`
from lowest to highest.

*Remember: the filter condition still goes inside the square brackets and
must reference* `players` *again, e.g.* `players[players["Column"] ...]`."""
)
Q5_ANSWER_B = (
    'result = players[(players["city"] == "Seoul") & (players["monthly_earnings_usd"] < 100)]\n'
    'result = result.sort_values("monthly_earnings_usd", ascending=True)'
)


def _q5_question(intro, answer_code):
    body = code_box([
        "result = players[",
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
    r'px.scatter(players, x="years\_playing", y="monthly\_earnings\_usd",',
    r'\hspace*{1.5em}symbol="ladder\_status", size="sponsors",',
    r'\hspace*{1.5em}title="Years Playing vs. Monthly Earnings")',
]
Q6_ANSWERS_A = [
    ("x-axis", "years_playing -- Numerical"),
    ("y-axis", "monthly_earnings_usd -- Numerical"),
    ("symbol", "ladder_status -- Categorical"),
    ("size", "sponsors -- Numerical"),
]
Q6_CODE_PLAIN_A = (
    'px.scatter(players, x="years_playing", y="monthly_earnings_usd",\n'
    '           symbol="ladder_status", size="sponsors",\n'
    '           title="Years Playing vs. Monthly Earnings")'
)

Q6_CODE_B = [
    r'px.scatter(players, x="sponsors", y="monthly\_earnings\_usd",',
    r'\hspace*{1.5em}symbol="skill\_level", size="years\_playing",',
    r'\hspace*{1.5em}title="Sponsors vs. Monthly Earnings")',
]
Q6_ANSWERS_B = [
    ("x-axis", "sponsors -- Numerical"),
    ("y-axis", "monthly_earnings_usd -- Numerical"),
    ("symbol", "skill_level -- Categorical"),
    ("size", "years_playing -- Numerical"),
]
Q6_CODE_PLAIN_B = (
    'px.scatter(players, x="sponsors", y="monthly_earnings_usd",\n'
    '           symbol="skill_level", size="years_playing",\n'
    '           title="Sponsors vs. Monthly Earnings")'
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

def _new_page(question):
    """Start `question` on a fresh page. Pagination is fixed so both versions
    match: p1 dataset + Q1, p2 Q2-Q3, p3 Q4-Q5, p4 Q6 (a tall table can't
    split across pages, so leaving it to LaTeX strands headings/sketch space)."""
    question.page_break_before = True
    return question


CONTENT = QuizContent(
    title=TITLE,
    subtitle=SUBTITLE,
    dataset_intro_md=DATASET_INTRO_MD,
    sample_columns=SAMPLE_COLUMNS,
    sample_col_widths_cm=SAMPLE_COL_WIDTHS_CM,
    versions={
        "A": QuizVersion(
            rows=ROWS_A,
            questions=[
                _q1_question(ROWS_A, Q1_CODE_A, Q1_ANSWER_A, Q1_AFTER_A),
                _new_page(_q2_question(Q2_INTRO_A, Q2_CODE_A, Q2_CODE_ANSWER_A)),
                _q3_question(Q3_ROWS_A),
                _new_page(_q4_question(Q4_ITEMS_A)),
                _q5_question(Q5_INTRO_A, Q5_ANSWER_A),
                _new_page(_q6_question(Q6_CODE_A, Q6_ANSWERS_A, Q6_CODE_PLAIN_A)),
            ],
        ),
        "B": QuizVersion(
            rows=ROWS_B,
            questions=[
                _q1_question(ROWS_B, Q1_CODE_B, Q1_ANSWER_B, Q1_AFTER_B),
                _new_page(_q2_question(Q2_INTRO_B, Q2_CODE_B, Q2_CODE_ANSWER_B, Q2_TEXT_ANSWER_B)),
                _q3_question(Q3_ROWS_B),
                _new_page(_q4_question(Q4_ITEMS_B)),
                _q5_question(Q5_INTRO_B, Q5_ANSWER_B),
                _new_page(_q6_question(Q6_CODE_B, Q6_ANSWERS_B, Q6_CODE_PLAIN_B)),
            ],
        ),
    },
)
