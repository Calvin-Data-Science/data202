"""Content for Quiz 3 (Week 6): covers Week 4's SLOs (04A/04B/04C) and Week
5's SLOs (05A/05B/05C), plus three questions retaking Quiz 2's SLOs
(03A/03B/03C) -- per the syllabus's repeat-questions-between-quizzes policy.
Week 6 material (kNN) is NOT covered (same one-quiz lag as Quiz 2).

Sized for a 30-minute sitting: nine questions, each ONE short task (no
(a)/(b)/(c) parts), about 3 minutes apiece.

Dataset: one simulated campus-gym dataset used by EVERY question -- three
related tables (`members`, `checkins`, `plans`) for the relational/tidy
questions, and a per-member `profile` built from them for the clustering/PCA
questions. There is no CSV on the site; the printed outputs in Q5-Q6
(inertia/silhouette, PCA shares, 213 profile rows) come
from a real run of scripts/quiz_content/quiz03_gym_data.py (seed 3) --
re-run it and update the numbers here if that script changes. The sample
rows are real rows of that data, except for `plan`, whose messy raw
spellings are hand-written for Q7.

Q2 merges checkins (one row per member per month) LEFT with members, so each
check-in row picks up its member's details. Row counts use ONLY the sample
rows shown: A inner 5 / left 6 / right 7 / outer 8; B inner 5 / left 7 /
right 7 / outer 9.
"""

import re

from build_quiz import (
    QuizContent, QuizVersion, Question,
    blank_table, code_box, blank_line, sketch_box, sample_table, tex_escape, raw_latex,
)

TITLE = "DATA 202 --- Quiz 3"
SUBTITLE = "Week 6 --- Covering Weeks 4--5: Joins, Tidy Data, Clustering & PCA"

DATASET_INTRO_MD = r"""
## The Dataset: Campus Gym

The campus gym keeps three related tables (simulated data). Every question
on this quiz uses them.

- `members` --- one row per gym member: `member_id`, the `plan` they signed
  up for (typed by hand at the front desk, so the **raw** text is messy), and
  their habits per visit: `avg_minutes` (minutes per visit), `cardio_pct`
  (\% of that time on cardio machines) and `calories` (calories burned per
  visit).
- `checkins` --- how many times a member came to the gym in each week
  (`week_1`--`week_4`) of a `month`.
- `plans` --- the gym's membership plans and their `monthly_fee` (dollars).

Question 7 works with the raw `plan` text. All other questions assume `plan`
has already been cleaned to `"basic"`, `"premium"` or `"student-monthly"`.

**First few rows of `members` (raw):**
"""

SAMPLE_COLUMNS = ["member_id", "plan", "avg_minutes", "cardio_pct", "calories"]
SAMPLE_COL_WIDTHS_CM = [2.4, 4.0, 2.6, 2.6, 2.6]

ROWS_A = [
    dict(zip(SAMPLE_COLUMNS, ["M001", "Basic", 44, 70, 390])),
    dict(zip(SAMPLE_COLUMNS, ["M002", "BASIC", 51, 71, 420])),
    dict(zip(SAMPLE_COLUMNS, ["M003", "Prem", 34, 43, 290])),
    dict(zip(SAMPLE_COLUMNS, ["M004", "basic", 82, 12, 440])),
    dict(zip(SAMPLE_COLUMNS, ["M005", "Student - Monthly", 45, 98, 440])),
]
ROWS_B = [
    dict(zip(SAMPLE_COLUMNS, ["M006", "PREMIUM", 81, 24, 500])),
    dict(zip(SAMPLE_COLUMNS, ["M007", "Student-Monthly", 103, 16, 610])),
    dict(zip(SAMPLE_COLUMNS, ["M008", "prem", 46, 85, 400])),
    dict(zip(SAMPLE_COLUMNS, ["M009", "Basic", 49, 49, 370])),
    dict(zip(SAMPLE_COLUMNS, ["M010", "student - monthly", 38, 74, 340])),
]

CHECKIN_COLUMNS = ["member_id", "month", "week_1", "week_2", "week_3", "week_4"]
CHECKIN_COL_WIDTHS_CM = [2.4, 1.8, 1.8, 1.8, 1.8, 1.8]


def _checkins(rows):
    return [dict(zip(CHECKIN_COLUMNS, r)) for r in rows]


CHECKINS_A = _checkins([
    ("M002", "Sep", 6, 5, 6, 2),
    ("M002", "Oct", 6, 1, 2, 4),
    ("M003", "Sep", 2, 1, 0, 0),
    ("M003", "Oct", 0, 0, 0, 1),
    ("M004", "Sep", 5, 2, 1, 4),
    ("M006", "Sep", 4, 3, 3, 4),
])
CHECKINS_B = _checkins([
    ("M006", "Sep", 4, 3, 3, 4),
    ("M006", "Oct", 5, 0, 4, 5),
    ("M008", "Sep", 7, 2, 3, 4),
    ("M008", "Oct", 5, 3, 1, 3),
    ("M010", "Sep", 1, 4, 3, 2),
    ("M011", "Sep", 5, 3, 4, 4),
    ("M011", "Oct", 3, 5, 4, 4),
])

PLAN_COLUMNS = ["plan", "monthly_fee"]
PLANS = [
    dict(plan="basic", monthly_fee=25),
    dict(plan="premium", monthly_fee=45),
    dict(plan="student-monthly", monthly_fee=15),
]


def _extra_tables(checkin_rows):
    return [
        dict(title_md="**First few rows of `checkins`:**", columns=CHECKIN_COLUMNS,
             rows=checkin_rows, col_widths_cm=CHECKIN_COL_WIDTHS_CM),
        dict(title_md="**All of `plans`:**", columns=PLAN_COLUMNS, rows=PLANS,
             col_widths_cm=[3.5, 2.6]),
    ]


# ---------------------------------------------------------------------------
# Code-box helpers
# ---------------------------------------------------------------------------

def _code_lines(code):
    """Plain code -> code_box() lines. Each 4 leading spaces become a 1.5em
    indent; «width» (e.g. «2.2cm») becomes a fill-in blank of that width;
    everything else is tex_escape'd."""
    lines = []
    for line in code.split("\n"):
        indent = len(line) - len(line.lstrip(" "))
        prefix = r"\hspace*{%.1fem}" % (1.5 * indent / 4) if indent else ""
        parts = re.split(r"«([^»]*)»", line.lstrip(" "))
        out = "".join(
            blank_line(p) if i % 2 else tex_escape(p) for i, p in enumerate(parts)
        )
        lines.append(prefix + out or r"\mbox{}")  # an empty line can't end with \\
    return lines


def _code(code):
    return code_box(_code_lines(code))


def _md_code(code):
    return "```python\n" + code + "\n```"


def _space(height):
    return sketch_box(height)



# ---------------------------------------------------------------------------
# Question 1 (SLO 04A) -- keys and relationships
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 04A)"
Q1_INTRO = (
    "For each column below, say whether it is a **primary key**, a "
    "**foreign key**, or **neither** in that table. For a foreign key, name "
    "the table it points to."
)
Q1_ROWS = {
    "A": [
        ("members", "member_id", "Primary key"),
        ("members", "plan", "Foreign key -> plans"),
        ("plans", "plan", "Primary key"),
        ("checkins", "member_id", "Foreign key -> members (it repeats: one row per member per month)"),
        ("checkins", "week_1", "Neither (a measurement, not an identifier)"),
    ],
    "B": [
        ("checkins", "member_id", "Foreign key -> members (it repeats: one row per member per month)"),
        ("plans", "plan", "Primary key"),
        ("members", "calories", "Neither (a measurement, not an identifier)"),
        ("members", "plan", "Foreign key -> plans"),
        ("members", "member_id", "Primary key"),
    ],
}


def _q1_question(letter):
    rows = Q1_ROWS[letter]
    body = blank_table(
        given_cols=[("Table", "2.2cm", True), ("Column", "2.4cm", True)],
        blank_cols=[("Primary key / Foreign key / Neither", "4.6cm"),
                    ("If foreign key: points to which table?", "4.6cm")],
        rows=[[t, c] for t, c, _a in rows],
    )
    answer = ["| Table | Column | Answer |", "|---|---|---|"]
    answer += [f"| `{t}` | `{c}` | {a} |" for t, c, a in rows]
    return Question(Q1_HEADING, Q1_INTRO, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 2 (SLO 04B) -- join types
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 04B)"
Q2_INTRO = (
    "Suppose `members` and `checkins` contained **only the rows shown on "
    "page 1**. How many rows would each join below return?"
)
Q2_CODE = 'pd.merge(checkins, members, on="member_id", how=___)'
Q2_COUNTS = {
    "A": [("inner", 5), ("left", 6), ("right", 7), ("outer", 8)],
    "B": [("inner", 5), ("left", 7), ("right", 7), ("outer", 9)],
}
Q2_WHY = {
    "A": ("M002 and M003 have 2 check-in rows each and M004 has 1, all matching a member, "
          "so inner = 5. Left (keep all check-ins) adds M006 (no member row) -> 6. "
          "Right (keep all members) adds M001 and M005 (no check-ins) -> 7. "
          "Outer adds all three -> 8."),
    "B": ("M006 and M008 have 2 check-in rows each and M010 has 1, all matching a member, "
          "so inner = 5. Left (keep all check-ins) adds M011's two rows (no member row) -> 7. "
          "Right (keep all members) adds M007 and M009 (no check-ins) -> 7. "
          "Outer adds all four -> 9."),
}


def _q2_question(letter):
    counts = Q2_COUNTS[letter]
    body = (
        _code(Q2_CODE)
        + "\n"
        + blank_table(
            given_cols=[("how=", "3cm", True)],
            blank_cols=[("Number of rows", "3.5cm")],
            rows=[[f'"{h}"'] for h, _n in counts],
        )
    )
    answer = ["| how= | rows |", "|---|---|"]
    answer += [f'| `"{h}"` | {n} |' for h, n in counts]
    answer += ["", Q2_WHY[letter]]
    return Question(Q2_HEADING, Q2_INTRO, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 3 (SLO 04C) -- wide -> long (sketch the melted table)
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 04C)"
Q3_CODE = (
    "checkins_long = pd.melt(\n"
    "    checkins,\n"
    '    id_vars=["member_id", "month"],\n'
    '    value_vars=["week_1", "week_2", "week_3", "week_4"],\n'
    '    var_name="week",\n'
    '    value_name="visits",\n'
    ")"
)
# The checkins rows (page 1) students melt: one member, both months.
Q3_MEMBER = {
    "A": ("M002", [("Sep", [6, 5, 6, 2]), ("Oct", [6, 1, 2, 4])]),
    "B": ("M008", [("Sep", [7, 2, 3, 4]), ("Oct", [5, 3, 1, 3])]),
}


def _q3_question(letter):
    member, months = Q3_MEMBER[letter]
    intro = (
        f"The code below reshapes `checkins` into a long table. Sketch the "
        f"part of `checkins_long` that comes from **{member}'s two rows** of "
        "`checkins` (page 1): column names and every row."
    )
    body = _code(Q3_CODE) + "\n" + _space("3.2in")
    answer = [_md_code(Q3_CODE), "",
              "| member_id | month | week | visits |", "|---|---|---|---|"]
    for month, visits in months:
        answer += [f"| {member} | {month} | week_{w} | {v} |" for w, v in enumerate(visits, start=1)]
    answer += ["", "8 rows: 2 wide rows x 4 week columns. Row order may differ "
               "(pd.melt actually lists all week_1 rows first, then week_2, ...); "
               "any order is fine."]
    return Question(Q3_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 4 (SLO 05A) -- one round of k-means by hand
# ---------------------------------------------------------------------------

Q4_HEADING = "Question 4 (SLO 05A)"
# Six members on a small integer grid (x = visits_per_week, y = calories in
# hundreds), k = 2, starting centroids = two of the members (as in class's
# run_kmeans(X, start_rows)). Points are chosen so every assignment is clear
# (no ties) and the new centroids are whole numbers -- verified with numpy:
#   A: start M12, M16 -> {M11,M12,M13} {M14,M15,M16} -> new (1,2) and (5,3)
#   B: start M21, M24 -> {M21,M22,M23} {M24,M25,M26} -> new (2,5) and (5,2)
Q4_POINTS = {
    "A": [("M11", 1, 1), ("M12", 1, 3), ("M13", 1, 2), ("M14", 4, 3), ("M15", 5, 4), ("M16", 6, 2)],
    "B": [("M21", 1, 4), ("M22", 2, 5), ("M23", 3, 6), ("M24", 4, 1), ("M25", 5, 2), ("M26", 6, 3)],
}
Q4_START = {"A": ("M12", "M16"), "B": ("M21", "M24")}
Q4_ASSIGN = {"A": ["A", "A", "A", "B", "B", "B"], "B": ["A", "A", "A", "B", "B", "B"]}
Q4_NEW = {"A": ((1, 2), (5, 3)), "B": ((2, 5), (5, 2))}


def _q4_grid(points, start):
    """TikZ grid with the six members; the two starting centroids are drawn
    as labelled crosses on top of their members. Returns bare LaTeX."""
    lines = [r"\begin{tikzpicture}[scale=0.68]",
             r"\draw[gray!40, very thin] (0,0) grid (7,7);",
             r"\draw[->] (0,0) -- (7.4,0);",
             r"\draw[->] (0,0) -- (0,7.4);",
             r"\node at (3.5,-1.0) {\small visits\_per\_week};",
             r"\node[rotate=90] at (-1.0,3.5) {\small calories (hundreds)};"]
    for i in range(1, 8):
        lines.append(r"\node[below] at (%d,0) {\scriptsize %d};" % (i, i))
        lines.append(r"\node[left] at (0,%d) {\scriptsize %d};" % (i, i))
    for name, x, y in points:
        lines.append(r"\fill (%d,%d) circle (3pt) node[below right=0pt] {\scriptsize %s};" % (x, y, name))
    for label, member in zip("AB", start):
        x, y = next((px, py) for n, px, py in points if n == member)
        lines.append(r"\draw[very thick] (%d-0.3,%d-0.3) -- (%d+0.3,%d+0.3) (%d-0.3,%d+0.3) -- (%d+0.3,%d-0.3);"
                     % (x, y, x, y, x, y, x, y))
        lines.append(r"\node[above right=1pt] at (%d,%d) {\textbf{%s}};" % (x, y, label))
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def _unfence(raw):
    """Strip the ```{=latex} fence that raw_latex()/blank_table() add, so the
    LaTeX can be nested inside another raw block (e.g. a minipage)."""
    return raw.strip().removeprefix("```{=latex}").removesuffix("```").strip()


def _q4_question(letter):
    points, start = Q4_POINTS[letter], Q4_START[letter]
    intro = (
        "Run **one round of k-means by hand** (k = 2) on these six members. "
        f"The starting centroids are **A** = member {start[0]} and **B** = "
        f"member {start[1]} (the crosses). First write the closest centroid "
        "for each member, then compute the two new centroids."
    )
    table = blank_table(
        given_cols=[("member", "1.3cm", True), ("visits", "1.3cm", False),
                    ("calories (100s)", "1.9cm", False)],
        blank_cols=[("Closest centroid (A/B)", "2.3cm")],
        rows=[[n, str(x), str(y)] for n, x, y in points],
    )
    body = raw_latex(
        r"\noindent\begin{minipage}[c]{0.42\linewidth}\centering" + "\n"
        + _q4_grid(points, start) + "\n"
        + r"\end{minipage}\hfill\begin{minipage}[c]{0.55\linewidth}" + "\n"
        + _unfence(table) + "\n"
        + r"\end{minipage}" + "\n\n"
        + r"\vspace{8pt}New centroid A = ( " + blank_line("1.2cm") + " , "
        + blank_line("1.2cm") + r" )\hspace{1.5cm}New centroid B = ( "
        + blank_line("1.2cm") + " , " + blank_line("1.2cm") + " )"
    )
    (ax, ay), (bx, by) = Q4_NEW[letter]
    answer = ["| member | visits_per_week | calories (hundreds) | closest |", "|---|---|---|---|"]
    answer += [f"| {n} | {x} | {y} | {c} |" for (n, x, y), c in zip(points, Q4_ASSIGN[letter])]
    answer += ["", f"New centroid A = ({ax}, {ay}), new centroid B = ({bx}, {by}) -- the "
               "mean visits_per_week and mean calories of each centroid's members.",
               "", "Assign: each member goes to the centroid at the smallest straight-line "
               "distance. Update: each centroid moves to the average of its members."]
    return Question(Q4_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 5 (SLO 05B) -- elbow and silhouette
# ---------------------------------------------------------------------------

Q5_HEADING = "Question 5 (SLO 05B)"
Q5_INTRO = (
    "For Questions 5--6, the gym built `profile`: one row per member (213 "
    "members) with `visits_per_week` (from `checkins`) plus `avg_minutes`, "
    "`cardio_pct` and `calories`, scaled into `X_scaled`. It ran k-means on "
    "`X_scaled` for k = 1 to 8 and recorded the inertia and the silhouette "
    "score of each run. **Which k would you choose?** Justify using both rows "
    "of the table."
)
ELBOW_COLUMNS = ["k", "1", "2", "3", "4", "5", "6", "7", "8"]
ELBOW_ROWS = [
    dict(zip(ELBOW_COLUMNS, ["inertia", 852, 436, 165, 139, 116, 96, 88, 82])),
    dict(zip(ELBOW_COLUMNS, ["silhouette", "---", 0.47, 0.61, 0.51, 0.44, 0.35, 0.32, 0.30])),
]
Q5_ANSWER = (
    "**k = 3.** Inertia: the elbow is at 3 -- it falls steeply from k = 1 to 3 "
    "(852 → 436 → 165), then only slowly (139, 116, 96, ...). Silhouette: "
    "highest at k = 3 (0.61). Both agree. (Choosing k = 8 just because its "
    "inertia is lowest is wrong: inertia always drops as k grows.)"
)


def _q5_question(letter):
    body = (
        "\\footnotesize\n\n"
        + sample_table(ELBOW_COLUMNS, ELBOW_ROWS, col_widths_cm=[2.2] + [1.4] * 8)
        + "\n\n\\normalsize\n\n"
        + _space("1.1in")
    )
    return Question(Q5_HEADING, Q5_INTRO, body, Q5_ANSWER)


# ---------------------------------------------------------------------------
# Question 6 (SLO 05C) -- PCA explained variance
# ---------------------------------------------------------------------------

Q6_HEADING = "Question 6 (SLO 05C)"
Q6_CODE = (
    "PCA().fit(X_scaled).explained_variance_ratio_.round(3)\n"
    "# [0.617  0.307  0.070  0.006]"
)
Q6_TARGET = {"A": "90%", "B": "95%"}
Q6_ANSWER = {
    "A": "**2 components**: 0.617 + 0.307 = 0.924, so they keep **92.4%** (PC1 alone is only 61.7%).",
    "B": ("**3 components**: two keep 0.617 + 0.307 = 92.4% (< 95%); three keep "
          "0.617 + 0.307 + 0.070 = **99.4%**."),
}


def _q6_question(letter):
    intro = (
        "The gym ran PCA on the same four scaled columns (`X_scaled`) of "
        "`profile`:"
    )
    body = (
        _code(Q6_CODE)
        + "\n"
        + f"How many components would you keep to retain at least "
        f"**{Q6_TARGET[letter]}** of the variance? What share of the variance "
        "do they keep?\n\n"
        + _space("0.8in")
    )
    return Question(Q6_HEADING, intro, body, _md_code(Q6_CODE) + "\n\n" + Q6_ANSWER[letter])


# ---------------------------------------------------------------------------
# Question 7 (SLO 03A) -- RETAKE: cleaning text (predict the result)
# ---------------------------------------------------------------------------

Q7_HEADING = "Question 7 (SLO 03A) --- Retake from Quiz 2"
Q7_INTRO = (
    "The code below is run on the **raw** `plan` column of `members` "
    "(page 1). Write what each `plan` value becomes."
)
Q7_CODE = {
    "A": (
        'members["plan"] = (\n'
        '    members["plan"]\n'
        "    .str.strip()\n"
        "    .str.lower()\n"
        '    .str.replace(r"^prem$", "premium", regex=True)\n'
        ")"
    ),
    "B": (
        'members["plan"] = (\n'
        '    members["plan"]\n'
        "    .str.strip()\n"
        "    .str.lower()\n"
        r'    .str.replace(r"\s*-\s*", "-", regex=True)' "\n"
        ")"
    ),
}
Q7_AFTER = {
    "A": ["basic", "basic", "premium", "basic", "student - monthly"],
    "B": ["premium", "student-monthly", "prem", "basic", "student-monthly"],
}
Q7_NOTE = {
    "A": ('The `^...$` anchors mean only an *exact* `"prem"` is replaced. Nothing fixes '
          'the spaces in `"student - monthly"`, so M005 would still not match `plans`.'),
    "B": (r'`\s*-\s*` replaces a hyphen and any spaces around it with a bare hyphen. '
          'Nothing turns `"prem"` into `"premium"`, so M008 would still not match `plans`.'),
}


def _q7_question(letter, rows):
    body = (
        _code(Q7_CODE[letter])
        + "\n"
        + blank_table(
            given_cols=[("member_id", "2.4cm", True), ("plan (raw)", "4.0cm", True)],
            blank_cols=[("plan (after the code)", "5.5cm")],
            rows=[[r["member_id"], r["plan"]] for r in rows],
        )
    )
    answer = [_md_code(Q7_CODE[letter]), "",
              "| member_id | plan (raw) | plan (after) |", "|---|---|---|"]
    answer += [f'| {r["member_id"]} | `{r["plan"]}` | `{a}` |' for r, a in zip(rows, Q7_AFTER[letter])]
    answer += ["", Q7_NOTE[letter]]
    return Question(Q7_HEADING, Q7_INTRO, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 8 (SLO 03B) -- RETAKE: grouping and aggregating
# ---------------------------------------------------------------------------

Q8_HEADING = "Question 8 (SLO 03B) --- Retake from Quiz 2"
Q8_INTRO = {
    "A": ("Complete the code to compute the average `calories` for each "
          "`plan` (cleaned), sorted from highest to lowest."),
    "B": ("Complete the code to compute, for each `plan` (cleaned), the "
          "number of members and the median `cardio_pct`."),
}
Q8_CODE = {
    "A": (
        "result = (\n"
        '    members.groupby("«2.6cm»")["«2.6cm»"]\n'
        "    .«1.8cm»()\n"
        "    .reset_index()\n"
        '    .sort_values("calories", ascending=«1.6cm»)\n'
        ")"
    ),
    "B": (
        'result = members.groupby("«2.6cm»").agg(\n'
        '    n_members=("member_id", "«2.0cm»"),\n'
        '    median_cardio=("«2.6cm»", "«2.0cm»"),\n'
        ")"
    ),
}
Q8_ANSWER = {
    "A": (
        "result = (\n"
        '    members.groupby("plan")["calories"]\n'
        "    .mean()\n"
        "    .reset_index()\n"
        '    .sort_values("calories", ascending=False)\n'
        ")"
    ),
    "B": (
        'result = members.groupby("plan").agg(\n'
        '    n_members=("member_id", "count"),\n'
        '    median_cardio=("cardio_pct", "median"),\n'
        ")"
    ),
}


def _q8_question(letter):
    return Question(Q8_HEADING, Q8_INTRO[letter], _code(Q8_CODE[letter]),
                    "Answer:\n" + _md_code(Q8_ANSWER[letter]))


# ---------------------------------------------------------------------------
# Question 9 (SLO 03C) -- RETAKE: matching a question to a plot type
# ---------------------------------------------------------------------------

Q9_HEADING = "Question 9 (SLO 03C) --- Retake from Quiz 2"
Q9_INTRO = (
    "For each question below, name the best plot type (Histogram / Scatter / "
    "Line / Bar) and the column(s) you'd map to x (and y, if relevant)."
)
Q9_ROWS = {
    "A": [
        ("What's the distribution of `calories` across all members?",
         "Histogram -- x=calories"),
        ("How do `avg_minutes` and `calories` relate to each other?",
         "Scatter -- x=avg_minutes, y=calories"),
        ("How does the total number of `visits` change from `week_1` to `week_4` (using `checkins_long`)?",
         "Line -- x=week, y=sum(visits)"),
        ("How does average `cardio_pct` compare across `plan` values?",
         "Bar -- x=plan, y=avg(cardio_pct)"),
    ],
    "B": [
        ("What's the distribution of `avg_minutes` across all members?",
         "Histogram -- x=avg_minutes"),
        ("How do `cardio_pct` and `calories` relate to each other?",
         "Scatter -- x=cardio_pct, y=calories"),
        ("How does the average number of `visits` change from `week_1` to `week_4` (using `checkins_long`)?",
         "Line -- x=week, y=avg(visits)"),
        ("How many members are in each `cluster` (after running k-means)?",
         "Bar -- x=cluster, y=count of members"),
    ],
}


def _q9_question(letter):
    rows = Q9_ROWS[letter]
    # blank_table is raw LaTeX: strip the markdown backticks kept for the answer key.
    body = blank_table(
        given_cols=[("Question", "9cm", False)],
        blank_cols=[("Plot Type", "2.3cm"), ("Column(s)", "2.3cm")],
        rows=[[q.replace("`", "")] for q, _a in rows],
    )
    answer = ["| Question | Answer |", "|---|---|"]
    answer += [f"| {q} | {a} |" for q, a in rows]
    return Question(Q9_HEADING, Q9_INTRO, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------

def _new_page(question):
    question.page_break_before = True
    return question


def _questions(letter, rows):
    return [
        _new_page(_q1_question(letter)),
        _q2_question(letter),
        _q3_question(letter),
        _new_page(_q4_question(letter)),
        _q5_question(letter),
        _q6_question(letter),
        _new_page(_q7_question(letter, rows)),
        _q8_question(letter),
        _q9_question(letter),
    ]


CONTENT = QuizContent(
    title=TITLE,
    subtitle=SUBTITLE,
    dataset_intro_md=DATASET_INTRO_MD,
    sample_columns=SAMPLE_COLUMNS,
    sample_col_widths_cm=SAMPLE_COL_WIDTHS_CM,
    margin="0.7in",
    fontsize="10pt",
    versions={
        "A": QuizVersion(rows=ROWS_A, questions=_questions("A", ROWS_A),
                         extra_tables=_extra_tables(CHECKINS_A)),
        "B": QuizVersion(rows=ROWS_B, questions=_questions("B", ROWS_B),
                         extra_tables=_extra_tables(CHECKINS_B)),
    },
)
