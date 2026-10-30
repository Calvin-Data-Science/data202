"""Content for the Week 5 retake quiz, given alongside Quiz 4 (Week 9): three
questions retaking Quiz 3's clustering/PCA SLOs (05A/05B/05C), which Quiz 4
left out. Same question formats as Quiz 3's Questions 4-6, on new data.

Build:  python scripts/build_quiz.py 4 --variant retake05
        python scripts/build_quiz.py 4 --variant retake05 --keys
Output: weeks/09/quiz04_retake05.md, _A.pdf, _B.pdf, _A_key.pdf, _B_key.pdf

About 10 minutes: three short tasks, 2 pages (dataset + Q1 | Q2-Q3).

Dataset: the campus library again (Quiz 4's setting), now a per-student
`readers` table. The page-1 sample rows, the elbow/silhouette table (Q2) and
the PCA shares (Q3) come from a real run of
scripts/quiz_content/quiz04_retake05_data.py (seed 5, 260 readers) -- re-run
it and update the numbers here if that script changes. Q1's six students are
hand-made on an integer grid; that script also checks them (no ties, whole-
number centroids).
"""

from build_quiz import (
    QuizContent, QuizVersion, Question,
    blank_table, code_box, blank_line, sketch_box, sample_table, tex_escape, raw_latex,
)
from quiz_content.quiz04_retake05_data import FEATURES, Q1_POINTS, Q1_START, make_readers

TITLE = "DATA 202 --- Quiz 4 Retake: Week 5"
SUBTITLE = "Retaking SLOs 05A--05C: Clustering & PCA"

DATASET_INTRO_MD = r"""
## The Dataset: Campus Library Readers

The campus library (simulated data, as in Quiz 4) built `readers`: one row
per student who used the library this fall (260 students), with four habits:

- `loans_per_month` --- how many books they borrow per month
- `avg_pages` --- the average length of the books they borrow (pages)
- `hours_per_week` --- hours they spend in the library per week
- `late_pct` --- the \% of their loans returned late

**A few rows of `readers`:**
"""

SAMPLE_COLUMNS = ["student_id"] + FEATURES
SAMPLE_COL_WIDTHS_CM = [2.4, 3.2, 2.4, 3.2, 2.4]

_READERS = make_readers()
ROWS = {
    "A": _READERS.head(4)[SAMPLE_COLUMNS].to_dict("records"),
    "B": _READERS.iloc[4:8][SAMPLE_COLUMNS].to_dict("records"),
}


def _md_code(code):
    return "```python\n" + code + "\n```"


def _unfence(raw):
    """Strip the ```{=latex} fence that raw_latex()/blank_table() add, so the
    LaTeX can be nested inside another raw block (e.g. a minipage)."""
    return raw.strip().removeprefix("```{=latex}").removesuffix("```").strip()


# ---------------------------------------------------------------------------
# Question 1 (SLO 05A) -- one round of k-means by hand
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 05A) --- Retake from Quiz 3"
# Checked by quiz04_retake05_data.check_q1():
#   A: start S35, S34 -> A {S31,S33,S35}, B {S32,S34,S36} -> new (2,5) and (6,2)
#   B: start S42, S45 -> A {S42,S44,S46}, B {S41,S43,S45} -> new (2,2) and (5,6)
Q1_ASSIGN = {"A": ["A", "B", "A", "B", "A", "B"], "B": ["B", "A", "B", "A", "B", "A"]}
Q1_NEW = {"A": ((2, 5), (6, 2)), "B": ((2, 2), (5, 6))}


def _q1_grid(points, start):
    """TikZ grid with the six students; the two starting centroids are drawn
    as labelled crosses on top of their students. Returns bare LaTeX."""
    lines = [r"\begin{tikzpicture}[scale=0.68]",
             r"\draw[gray!40, very thin] (0,0) grid (7,7);",
             r"\draw[->] (0,0) -- (7.4,0);",
             r"\draw[->] (0,0) -- (0,7.4);",
             r"\node at (3.5,-1.0) {\small loans\_per\_month};",
             r"\node[rotate=90] at (-1.0,3.5) {\small hours\_per\_week};"]
    for i in range(1, 8):
        lines.append(r"\node[below] at (%d,0) {\scriptsize %d};" % (i, i))
        lines.append(r"\node[left] at (0,%d) {\scriptsize %d};" % (i, i))
    for name, x, y in points:
        lines.append(r"\fill (%d,%d) circle (3pt) node[below right=0pt] {\scriptsize %s};" % (x, y, name))
    for label, student in zip("AB", start):
        x, y = next((px, py) for n, px, py in points if n == student)
        lines.append(r"\draw[very thick] (%d-0.3,%d-0.3) -- (%d+0.3,%d+0.3) (%d-0.3,%d+0.3) -- (%d+0.3,%d-0.3);"
                     % (x, y, x, y, x, y, x, y))
        lines.append(r"\node[above right=1pt] at (%d,%d) {\textbf{%s}};" % (x, y, label))
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def _q1_question(letter):
    points, start = Q1_POINTS[letter], Q1_START[letter]
    intro = (
        "Run **one round of k-means by hand** (k = 2) on these six students. "
        f"The starting centroids are **A** = student {start[0]} and **B** = "
        f"student {start[1]} (the crosses). First write the closest centroid "
        "for each student, then compute the two new centroids."
    )
    table = blank_table(
        given_cols=[("student", "1.3cm", True), ("loans", "1.3cm", False),
                    ("hours", "1.3cm", False)],
        blank_cols=[("Closest centroid (A/B)", "2.3cm")],
        rows=[[n, str(x), str(y)] for n, x, y in points],
    )
    body = raw_latex(
        r"\noindent\begin{minipage}[c]{0.42\linewidth}\centering" + "\n"
        + _q1_grid(points, start) + "\n"
        + r"\end{minipage}\hfill\begin{minipage}[c]{0.55\linewidth}" + "\n"
        + _unfence(table) + "\n"
        + r"\end{minipage}" + "\n\n"
        + r"\vspace{8pt}New centroid A = ( " + blank_line("1.2cm") + " , "
        + blank_line("1.2cm") + r" )\hspace{1.5cm}New centroid B = ( "
        + blank_line("1.2cm") + " , " + blank_line("1.2cm") + " )"
    )
    (ax, ay), (bx, by) = Q1_NEW[letter]
    answer = ["| student | loans_per_month | hours_per_week | closest |", "|---|---|---|---|"]
    answer += [f"| {n} | {x} | {y} | {c} |" for (n, x, y), c in zip(points, Q1_ASSIGN[letter])]
    answer += ["", f"New centroid A = ({ax}, {ay}), new centroid B = ({bx}, {by}) -- the "
               "mean loans_per_month and mean hours_per_week of each centroid's students.",
               "", "Assign: each student goes to the centroid at the smallest straight-line "
               "distance. Update: each centroid moves to the average of its students."]
    return Question(Q1_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 2 (SLO 05B) -- elbow and silhouette
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 05B) --- Retake from Quiz 3"
Q2_INTRO = (
    "The library scaled the four columns of `readers` into `X_scaled` and ran "
    "k-means on it for k = 1 to 8, recording the inertia and the silhouette "
    "score of each run. **Which k would you choose?** Justify using both rows "
    "of the table."
)
ELBOW_COLUMNS = ["k", "1", "2", "3", "4", "5", "6", "7", "8"]
ELBOW_ROWS = [
    dict(zip(ELBOW_COLUMNS, ["inertia", 1040, 658, 379, 185, 164, 151, 139, 126])),
    dict(zip(ELBOW_COLUMNS, ["silhouette", "---", 0.38, 0.49, 0.59, 0.49, 0.45, 0.35, 0.26])),
]
Q2_ANSWER = (
    "**k = 4.** Inertia: the elbow is at 4 -- it falls steeply from k = 1 to 4 "
    "(1040 → 658 → 379 → 185), then only slowly (164, 151, 139, 126). Silhouette: "
    "highest at k = 4 (0.59). Both agree. (Choosing k = 8 just because its "
    "inertia is lowest is wrong: inertia always drops as k grows.)"
)


def _q2_question(letter):
    body = (
        "\\footnotesize\n\n"
        + sample_table(ELBOW_COLUMNS, ELBOW_ROWS, col_widths_cm=[2.2] + [1.4] * 8)
        + "\n\n\\normalsize\n\n"
        + sketch_box("1.3in")
    )
    return Question(Q2_HEADING, Q2_INTRO, body, Q2_ANSWER)


# ---------------------------------------------------------------------------
# Question 3 (SLO 05C) -- PCA explained variance
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 05C) --- Retake from Quiz 3"
Q3_CODE = (
    "PCA().fit(X_scaled).explained_variance_ratio_.round(3)\n"
    "# [0.456  0.306  0.195  0.043]"
)
Q3_TARGET = {"A": "75%", "B": "90%"}
Q3_ANSWER = {
    "A": "**2 components**: 0.456 + 0.306 = 0.762, so they keep **76.2%** (PC1 alone is only 45.6%).",
    "B": ("**3 components**: two keep 0.456 + 0.306 = 76.2% (< 90%); three keep "
          "0.456 + 0.306 + 0.195 = **95.7%**."),
}


def _q3_question(letter):
    intro = "The library ran PCA on the same four scaled columns (`X_scaled`):"
    body = (
        code_box([tex_escape(line) for line in Q3_CODE.split("\n")])
        + "\n"
        + f"How many components would you keep to retain at least "
        f"**{Q3_TARGET[letter]}** of the variance? What share of the variance "
        "do they keep?\n\n"
        + sketch_box("1.0in")
    )
    return Question(Q3_HEADING, intro, body, _md_code(Q3_CODE) + "\n\n" + Q3_ANSWER[letter])


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------

def _questions(letter):
    q2 = _q2_question(letter)
    q2.page_break_before = True          # page 1: dataset + Q1 | page 2: Q2-Q3
    return [_q1_question(letter), q2, _q3_question(letter)]


CONTENT = QuizContent(
    title=TITLE,
    subtitle=SUBTITLE,
    dataset_intro_md=DATASET_INTRO_MD,
    sample_columns=SAMPLE_COLUMNS,
    sample_col_widths_cm=SAMPLE_COL_WIDTHS_CM,
    margin="0.7in",
    fontsize="10pt",
    versions={
        letter: QuizVersion(rows=ROWS[letter], questions=_questions(letter))
        for letter in ("A", "B")
    },
)
