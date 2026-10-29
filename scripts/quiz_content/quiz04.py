"""Content for Quiz 4 (Week 9): covers Week 6's SLOs (06A/06B/06C) and Week
7's SLOs (07A/07B/07C), plus three questions retaking Quiz 3's join/tidy SLOs
(04A/04B/04C) -- per the syllabus's repeat-questions-between-quizzes policy.
Week 9 material (scaling, encoding, missing data) is NOT covered: same
one-quiz lag as before, so it goes on Quiz 5.

Sized for a 30-minute sitting: nine questions, each ONE short task, about 3
minutes apiece; 4 pages (dataset + Q1 | Q2-4 | Q5-7 | Q8-9).

Dataset: one simulated campus-library dataset used by EVERY question --
`loans`, `students`, `books` and the wide `monthly_loans`. The printed
outputs in Q2, Q4, Q5 and Q6 (confusion matrices, depth-2 tree, depth table,
grid-search numbers) come from a real run of
scripts/quiz_content/quiz04_library_data.py (seed 8) -- re-run it and update
the numbers here if that script changes. The page-1 sample rows and the Q1
grid are hand-made (small, so they can be worked by hand).

Q8 (04B) is the redesigned join question: instead of counting rows, students
see four result tables of pd.merge(loans, students, how=?) and name the join
type of each. The tables are computed here with pandas from the page-1 rows,
so they are correct by construction.
"""

import re

import pandas as pd

from build_quiz import (
    QuizContent, QuizVersion, Question,
    blank_table, code_box, blank_line, sketch_box, sample_table, tex_escape, raw_latex,
)

TITLE = "DATA 202 --- Quiz 4"
SUBTITLE = "Week 9 --- Covering Weeks 6--7: kNN, Metrics, Trees & Cross-Validation"

DATASET_INTRO_MD = r"""
## The Dataset: Campus Library

The campus library keeps four related tables (simulated data). Every question
on this quiz uses them.

- `loans` --- one row per book loan: `loan_id`, the `student_id` who borrowed
  it, the `book_id` borrowed, and `late` (**the label**: 1 = returned late,
  0 = on time). There are 800 loans.
- `students` --- one row per student: `student_id`, `class_year` (1--4) and
  `prior_late` (how many books they returned late last year).
- `books` --- one row per book: `book_id`, `genre` and `pages`.
- `monthly_loans` --- one row per student: how many books they borrowed in
  each month (`sep`, `oct`, `nov`).

The models in Questions 1--6 predict `late` from `pages`, `prior_late` and
`class_year` (found by joining `loans` to `students` and `books`).

**A few rows of `loans`:**
"""

LOAN_COLUMNS = ["loan_id", "student_id", "book_id", "late"]
STUDENT_COLUMNS = ["student_id", "class_year", "prior_late"]

# Page-1 sample rows. One loan's student is missing from `students` and one
# student has no loans, so inner/left/right/outer all differ (Q8).
LOANS = {
    "A": [("L101", "S011", "B204", 0), ("L102", "S012", "B087", 1),
          ("L103", "S012", "B150", 0), ("L104", "S015", "B204", 1)],
    "B": [("L201", "S021", "B033", 1), ("L202", "S023", "B118", 0),
          ("L203", "S024", "B033", 0), ("L204", "S024", "B301", 1)],
}
STUDENTS = {
    "A": [("S011", 2, 0), ("S012", 4, 3), ("S013", 1, 1)],
    "B": [("S022", 3, 0), ("S023", 1, 2), ("S024", 2, 4)],
}


def _rows(columns, tuples):
    return [dict(zip(columns, t)) for t in tuples]


def _extra_tables(letter):
    return [dict(title_md="**A few rows of `students`:**", columns=STUDENT_COLUMNS,
                 rows=_rows(STUDENT_COLUMNS, STUDENTS[letter]), col_widths_cm=[2.4, 2.4, 2.4])]


# ---------------------------------------------------------------------------
# Helpers (same as quiz03)
# ---------------------------------------------------------------------------

def _code_lines(code):
    """Plain code -> code_box() lines. Each 4 leading spaces become a 1.5em
    indent; «width» becomes a fill-in blank of that width; everything else is
    tex_escape'd."""
    lines = []
    for line in code.split("\n"):
        indent = len(line) - len(line.lstrip(" "))
        prefix = r"\hspace*{%.1fem}" % (1.5 * indent / 4) if indent else ""
        parts = re.split(r"«([^»]*)»", line.lstrip(" "))
        out = "".join(blank_line(p) if i % 2 else tex_escape(p) for i, p in enumerate(parts))
        lines.append(prefix + out or r"\mbox{}")
    return lines


def _code(code):
    return code_box(_code_lines(code))


def _md_code(code):
    return "```python\n" + code + "\n```"


def _space(height):
    return sketch_box(height)


def _unfence(raw):
    """Strip the ```{=latex} fence so the LaTeX can be nested in a minipage."""
    return raw.strip().removeprefix("```{=latex}").removesuffix("```").strip()


# ---------------------------------------------------------------------------
# Question 1 (SLO 06A) -- kNN by hand
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 06A)"
# x = pages (hundreds), y = prior_late. Distances from the new loan (checked):
#   1 (late), 1.41, 2, 2.24 (on time x3), 2.83 (late), 3 (on time), 4.24 (late)
#   -> k = 1: late; k = 5: 3 on time vs 2 late -> on time. No ties at either k.
Q1_POINTS = {
    "A": dict(new=(4, 3), late=[(5, 3), (6, 5), (7, 6)], ontime=[(3, 2), (4, 5), (2, 4), (1, 3)]),
    "B": dict(new=(4, 4), late=[(4, 5), (6, 6), (7, 7)], ontime=[(3, 3), (6, 4), (2, 5), (1, 4)]),
}


def _q1_grid(p):
    lines = [r"\begin{tikzpicture}[scale=0.6]",
             r"\draw[gray!40, very thin] (0,0) grid (8,8);",
             r"\draw[->] (0,0) -- (8.4,0);", r"\draw[->] (0,0) -- (0,8.4);",
             r"\node at (4,-1.0) {\small pages (hundreds)};",
             r"\node[rotate=90] at (-1.0,4) {\small prior\_late};"]
    for i in range(1, 9):
        lines.append(r"\node[below] at (%d,0) {\scriptsize %d};" % (i, i))
        lines.append(r"\node[left] at (0,%d) {\scriptsize %d};" % (i, i))
    for x, y in p["ontime"]:
        lines.append(r"\draw[thick] (%d,%d) circle (5pt);" % (x, y))
    for x, y in p["late"]:
        lines.append(r"\fill (%d-0.17,%d-0.17) rectangle (%d+0.17,%d+0.17);" % (x, y, x, y))
    x, y = p["new"]
    lines.append(r"\node[font=\LARGE, inner sep=0pt] at (%d,%d) {$\star$};" % (x, y))
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def _q1_question(letter):
    p = Q1_POINTS[letter]
    intro = (
        "Seven training loans are plotted by `pages` (in hundreds) and the "
        "student's `prior_late`: a **filled square** was returned **late**, an "
        "**open circle** on time. The **star** is a new loan. Use the straight-"
        "line distance (count the grid squares; you don't need the formula)."
    )
    legend = (r"\small $\blacksquare$ late \quad $\circ$ on time \quad $\star$ new loan")
    right = (
        r"\textbf{kNN with k = 1} predicts:\\[4pt]" + blank_line("4.5cm") + r"\\[14pt]"
        + r"\textbf{kNN with k = 5} predicts:\\[4pt]" + blank_line("4.5cm") + r"\\[14pt]"
        + r"Which of the two k values is more likely to \textbf{overfit}? Why?\\[6pt]"
        + blank_line("\\linewidth") + r"\\[10pt]" + blank_line("\\linewidth")
    )
    body = raw_latex(
        r"\noindent\begin{minipage}[c]{0.46\linewidth}\centering" + "\n" + _q1_grid(p) + "\n\n"
        + legend + "\n" + r"\end{minipage}\hfill\begin{minipage}[c]{0.5\linewidth}" + "\n"
        + right + "\n" + r"\end{minipage}"
    )
    answer = (
        "Distances from the new loan: 1 (late), 1.41, 2, 2.24 (three on time), "
        "2.83 (late), 3 (on time), 4.24 (late).\n\n"
        "- **k = 1: late** (the single nearest loan was late).\n"
        "- **k = 5: on time** (the 5 nearest: 3 on time, 2 late).\n"
        "- **k = 1 is more likely to overfit**: it follows single training points "
        "(noise), so it is perfect on the data it learned from but less reliable on new loans."
    )
    return Question(Q1_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 2 (SLO 06B) -- confusion matrix and metrics
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 06B)"
# Real run, 200 test loans (53 late, 147 on time): kNN k=5 (A), k=15 (B).
Q2_CM = {"A": (5, 132, 15, 31, 22), "B": (15, 134, 13, 33, 20)}   # k, TN, FP, FN, TP


def _q2_question(letter):
    k, tn, fp, fn, tp = Q2_CM[letter]
    intro = (
        f"A kNN model (k = {k}) is scored on the **200 test loans**. "
        "Its confusion matrix, with **late** as the positive class:"
    )
    matrix = raw_latex(
        r"\begin{center}\begin{tabular}{|l|c|c|}\hline" + "\n"
        r" & \textbf{predicted on time} & \textbf{predicted late} \\ \hline" + "\n"
        rf"\textbf{{actually on time}} & {tn} & {fp} \\ \hline" + "\n"
        rf"\textbf{{actually late}} & {fn} & {tp} \\ \hline" + "\n"
        r"\end{tabular}\end{center}"
    )
    table = blank_table(
        given_cols=[("Metric", "6.2cm", False)],
        blank_cols=[("Show the fraction", "4.2cm"), ("Value", "2.4cm")],
        rows=[["Accuracy"], ["Precision (for late)"], ["Recall (for late)"],
              ["Accuracy of the lazy model that always says on time"]],
    )
    acc = (tn + tp) / 200
    prec, rec = tp / (tp + fp), tp / (tp + fn)
    answer = (
        f"| Metric | Fraction | Value |\n|---|---|---|\n"
        f"| Accuracy | ({tn} + {tp}) / 200 | {acc:.3f} |\n"
        f"| Precision (late) | {tp} / ({tp} + {fp}) = {tp}/{tp + fp} | {prec:.3f} |\n"
        f"| Recall (late) | {tp} / ({tp} + {fn}) = {tp}/{tp + fn} | {rec:.3f} |\n"
        f"| Lazy model | {tn + fp} / 200 | {(tn + fp) / 200:.3f} |\n\n"
        f"Accuracy {acc:.1%} beats the lazy model's {(tn + fp) / 200:.1%} only a little, and "
        f"recall shows the model catches fewer than half of the late loans."
    )
    return Question(Q2_HEADING, intro, matrix + "\n" + table, answer)


# ---------------------------------------------------------------------------
# Question 3 (SLO 06C) -- train/test split
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 06C)"
Q3_TEST_SIZE = {"A": ("0.25", 200), "B": ("0.2", 160)}


def _q3_diagram(test_size):
    """The machine-learning flow: data -> split -> four pieces (word bank), then
    1. fit, 2. predict, 3. score, each with blanks for the pieces it uses."""
    b = r"\rule{1.4cm}{0.5pt}"
    return "\n".join([
        r"\begin{tikzpicture}[>=stealth, box/.style={draw, thick, rounded corners=3pt, align=center,"
        r" inner sep=6pt, font=\small}]",
        r"\node[box] (data) at (0,0) {\textbf{data}: 800 loans\\features \texttt{X}, label \texttt{y}};",
        r"\node[box] (split) at (5.9,0) {\texttt{train\_test\_split(X, y,}\\\texttt{test\_size=%s)}};" % test_size,
        r"\node[box, dashed] (bank) at (12.3,0) {\textbf{four pieces}\\\texttt{X\_train} \quad \texttt{X\_test}"
        r"\\\texttt{y\_train} \quad \texttt{y\_test}};",
        r"\draw[->, thick] (data) -- (split);",
        r"\draw[->, thick] (split) -- (bank);",
        r"\node[box] (fit) at (0,-2.3) {\textbf{1. learn}\\[3pt]\texttt{model.fit(}%s\texttt{,} %s\texttt{)}};" % (b, b),
        r"\node[box] (pred) at (7.0,-2.3) {\textbf{2. predict}\\[3pt]\texttt{model.predict(}%s\texttt{)}};" % b,
        r"\node[box] (score) at (13.0,-2.3) {\textbf{3. score}\\[3pt]compare the predictions\\with %s"
        r" $\rightarrow$ accuracy};" % b,
        r"\draw[->, thick] (fit) -- node[above, font=\scriptsize] {trained model} (pred);",
        r"\draw[->, thick] (pred) -- node[above, font=\scriptsize] {predictions} (score);",
        r"\end{tikzpicture}",
    ])


def _q3_question(letter):
    test_size, n_test = Q3_TEST_SIZE[letter]
    intro = (
        "`data` holds all 800 loans. After the split, a model goes through three steps. Fill each "
        "blank with one of the four pieces, **`X_train`, `X_test`, `y_train` or `y_test`**, so that "
        "the accuracy tells how well the model will do on **new** loans. Each piece is used once. "
        "Then say how many loans end up in the test set."
    )
    body = raw_latex(
        r"\begin{center}" + "\n" + _q3_diagram(test_size) + "\n" + r"\end{center}" + "\n"
        + r"\noindent Number of loans in the test set: " + blank_line("2.5cm")
    )
    answer = (
        "1. **learn:** `model.fit(X_train, y_train)`\n"
        "2. **predict:** `model.predict(X_test)`\n"
        "3. **score:** compare the predictions with **`y_test`** → accuracy\n\n"
        f"Test set: **{n_test}** loans (800 × {test_size}).\n\n"
        "The model learns from the training rows only. The test rows play the part of new loans: "
        "the model sees X_test only to predict, and y_test only to check its answers."
    )
    return Question(Q3_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 4 (SLO 07A) -- follow a decision tree
# ---------------------------------------------------------------------------

Q4_HEADING = "Question 4 (SLO 07A)"
# Real depth-2 tree (600 training loans):
#   prior_late <= 1.5 & pages <= 550  -> on time [314, 40]
#   prior_late <= 1.5 & pages >  550  -> late    [13, 14]
#   prior_late >  1.5 & pages <= 305  -> on time [65, 23]
#   prior_late >  1.5 & pages >  305  -> late    [49, 82]
Q4_LOANS = {
    "A": [(0, 600, 2), (3, 200, 1), (2, 400, 4)],
    "B": [(1, 300, 3), (4, 320, 2), (2, 250, 1)],
}


def _predict(prior, pages):
    if prior <= 1.5:
        return "on time" if pages <= 550 else "late"
    return "on time" if pages <= 305 else "late"


TREE_TIKZ = r"""
\begin{tikzpicture}[
  q/.style={draw, rounded corners, fill=gray!12, font=\small, inner sep=4pt},
  leaf/.style={draw, font=\small, inner sep=3pt, align=center},
  level distance=1.5cm,
  level 1/.style={sibling distance=8.4cm},
  level 2/.style={sibling distance=4.1cm},
  edge from parent/.style={draw, -latex}]
\node[q] {prior\_late $\le$ 1.5 ?}
  child {node[q] {pages $\le$ 550 ?}
    child {node[leaf] {\textbf{on time}\\314 on time, 40 late} edge from parent node[left, font=\scriptsize] {yes}}
    child {node[leaf] {\textbf{late}\\13 on time, 14 late} edge from parent node[right, font=\scriptsize] {no}}
    edge from parent node[left, font=\scriptsize] {yes}}
  child {node[q] {pages $\le$ 305 ?}
    child {node[leaf] {\textbf{on time}\\65 on time, 23 late} edge from parent node[left, font=\scriptsize] {yes}}
    child {node[leaf] {\textbf{late}\\49 on time, 82 late} edge from parent node[right, font=\scriptsize] {no}}
    edge from parent node[right, font=\scriptsize] {no}};
\end{tikzpicture}
"""


def _q4_question(letter):
    loans = Q4_LOANS[letter]
    intro = (
        "A decision tree (`max_depth=2`) was fit on the 600 training loans. "
        "Each leaf shows its prediction and the training loans that reached it. "
        "Follow the tree for each new loan below."
    )
    tree = raw_latex(r"\begin{center}\resizebox{\linewidth}{!}{" + TREE_TIKZ.strip() + r"}\end{center}")
    table = blank_table(
        given_cols=[("prior_late", "2.2cm", False), ("pages", "1.8cm", False), ("class_year", "2.2cm", False)],
        blank_cols=[("Prediction (late / on time)", "4.6cm")],
        rows=[[str(a), str(b), str(c)] for a, b, c in loans],
    )
    answer = ["| prior_late | pages | class_year | prediction |", "|---|---|---|---|"]
    answer += [f"| {a} | {b} | {c} | **{_predict(a, b)}** |" for a, b, c in loans]
    answer += ["", "`class_year` is never asked by this tree, so it doesn't matter. "
               "Each loan follows one path from the top question to a leaf."]
    return Question(Q4_HEADING, intro, tree + "\n" + table, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 5 (SLO 07B) -- cross-validation picks the depth
# ---------------------------------------------------------------------------

Q5_HEADING = "Question 5 (SLO 07B)"
DEPTH_COLUMNS = ["max_depth", "1", "2", "3", "4", "6", "8", "no limit"]
DEPTH_ROWS = [
    dict(zip(DEPTH_COLUMNS, ["training folds", "0.735", "0.795", "0.802", "0.820", "0.856", "0.897", "0.935"])),
    dict(zip(DEPTH_COLUMNS, ["5-fold CV (held-out folds)", "0.718", "0.770", "0.765", "0.758", "0.747", "0.728", "0.710"])),
]
Q5_INTRO = (
    "Trees of different depths were scored with **5-fold cross-validation on "
    "the 600 training loans** (the test set was not used). The table shows the "
    "mean accuracy on the folds each tree was fit on, and on the held-out folds."
)
Q5_TASK = {
    "A": ("Which `max_depth` would you choose, and why? Name one depth that "
          "**underfits** and one that **overfits**, using both rows."),
    "B": ("Which `max_depth` would you choose, and why not the depth with the best "
          "**training** score? Name one depth that **underfits**, using both rows."),
}
Q5_ANSWER = {
    "A": ("**max_depth = 2** (best CV score, 0.770; depth 3 is about the same). "
          "**Underfits:** depth 1 (poor on both rows, 0.735 / 0.718). **Overfits:** "
          "no limit (0.935 on the folds it learned from but only 0.710 held out; "
          "depths 6 and 8 too). The growing gap between the rows is the sign of overfitting."),
    "B": ("**max_depth = 2** (best CV score, 0.770). The training score keeps rising "
          "to 0.935 with no limit because a deep tree memorizes the folds it was fit on; "
          "on held-out folds it falls to 0.710 (overfitting). **Underfits:** depth 1 "
          "(poor on both rows)."),
}


def _q5_question(letter):
    body = (
        "\\footnotesize\n\n"
        + sample_table(DEPTH_COLUMNS, DEPTH_ROWS, col_widths_cm=[4.2] + [1.45] * 7)
        + "\n\n\\normalsize\n\n" + Q5_TASK[letter] + "\n\n" + _space("1.0in")
    )
    return Question(Q5_HEADING, Q5_INTRO, body, Q5_ANSWER[letter])


# ---------------------------------------------------------------------------
# Question 6 (SLO 07C) -- grid search
# ---------------------------------------------------------------------------

Q6_HEADING = "Question 6 (SLO 07C)"
Q6_GRID = {
    "A": ('{"max_depth": [2, 4, 6, None],\n "min_samples_leaf": [1, 10, 30]}',
          4 * 3, "{'max_depth': 4, 'min_samples_leaf': 30}", 0.782, 0.740),
    "B": ('{"max_depth": [2, 3, 5],\n "min_samples_leaf": [5, 20, 40]}',
          3 * 3, "{'max_depth': 5, 'min_samples_leaf': 20}", 0.783, 0.760),
}


def _q6_code(grid, best, cv, test):
    return (
        f"grid = {grid}\n"
        "search = GridSearchCV(DecisionTreeClassifier(), grid, cv=5)\n"
        "search.fit(X_train, y_train)\n"
        f"search.best_params_   # {best}\n"
        f"search.best_score_    # {cv}\n"
        f"search.score(X_test, y_test)   # {test}"
    )


def _q6_question(letter):
    grid, n_comb, best, cv, test = Q6_GRID[letter]
    code = _q6_code(grid.replace("\n", "\n    "), best, cv, test)
    intro = "A grid search tunes two hyperparameters of the tree:"
    body = (
        _code(code) + "\n"
        "How many hyperparameter **combinations** does it try, and how many **trees** "
        "does it fit during cross-validation? Then: why is the test score lower than "
        "`best_score_`?\n\n" + _space("1.0in")
    )
    answer = (
        _md_code(_q6_code(grid, best, cv, test)) + "\n\n"
        f"**{n_comb} combinations** × 5 folds = **{n_comb * 5} trees** (plus one final refit "
        "of the winner on all the training loans).\n\n"
        f"Why {test} < {cv}: `best_score_` is the **best of {n_comb}** cross-validation scores, "
        "so the winner was partly lucky on these folds (the best of many is optimistic). "
        "The test set is new data that played no part in choosing, so its score is the "
        "honest one (and it is one split)."
    )
    return Question(Q6_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 7 (SLO 04A) -- RETAKE: keys
# ---------------------------------------------------------------------------

Q7_HEADING = "Question 7 (SLO 04A) --- Retake from Quiz 3"
Q7_INTRO = (
    "For each column below, say whether it is a **primary key**, a "
    "**foreign key**, or **neither** in that table. For a foreign key, name "
    "the table it points to."
)
Q7_ROWS = {
    "A": [
        ("loans", "loan_id", "Primary key"),
        ("loans", "student_id", "Foreign key -> students (it repeats: a student can borrow many books)"),
        ("students", "student_id", "Primary key"),
        ("loans", "book_id", "Foreign key -> books"),
        ("books", "pages", "Neither (a measurement, not an identifier)"),
    ],
    "B": [
        ("loans", "book_id", "Foreign key -> books"),
        ("books", "book_id", "Primary key"),
        ("students", "prior_late", "Neither (a measurement, not an identifier)"),
        ("loans", "student_id", "Foreign key -> students (it repeats: a student can borrow many books)"),
        ("loans", "loan_id", "Primary key"),
    ],
}


def _q7_question(letter):
    rows = Q7_ROWS[letter]
    body = blank_table(
        given_cols=[("Table", "2.2cm", True), ("Column", "2.4cm", True)],
        blank_cols=[("Primary key / Foreign key / Neither", "4.6cm"),
                    ("If foreign key: points to which table?", "4.6cm")],
        rows=[[t, c] for t, c, _a in rows],
    )
    answer = ["| Table | Column | Answer |", "|---|---|---|"]
    answer += [f"| `{t}` | `{c}` | {a} |" for t, c, a in rows]
    return Question(Q7_HEADING, Q7_INTRO, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 8 (SLO 04B) -- RETAKE, redesigned: name the join from its result
# ---------------------------------------------------------------------------

Q8_HEADING = "Question 8 (SLO 04B) --- Retake from Quiz 3"
Q8_SHOW = ["loan_id", "student_id", "class_year"]
# Order the four results are shown in (labels 1-4), per version.
Q8_ORDER = {"A": ["right", "inner", "outer", "left"], "B": ["left", "outer", "inner", "right"]}


def _merge_results(letter):
    loans = pd.DataFrame(LOANS[letter], columns=LOAN_COLUMNS)
    students = pd.DataFrame(STUDENTS[letter], columns=STUDENT_COLUMNS)
    out = {}
    for how in ("inner", "left", "right", "outer"):
        m = pd.merge(loans, students, on="student_id", how=how)[Q8_SHOW]
        out[how] = [["NaN" if pd.isna(v) else str(int(v)) if isinstance(v, float) else str(v)
                     for v in row] for row in m.itertuples(index=False)]
    return out


def _small_table(rows):
    lines = [r"\begin{tabular}{|l|l|c|}\hline",
             r"\texttt{loan\_id} & \texttt{student\_id} & \texttt{class\_year} \\ \hline"]
    lines += [" & ".join(tex_escape(c) for c in r) + r" \\ \hline" for r in rows]
    lines.append(r"\end{tabular}")
    return "\n".join(lines)


def _q8_question(letter):
    results = _merge_results(letter)
    order = Q8_ORDER[letter]
    intro = (
        "Suppose `loans` and `students` contained **only the rows shown on page 1**. "
        "Each table below is the result of "
        '`pd.merge(loans, students, on="student_id", how=___)` (only three columns '
        "shown). Write which join made each one: **inner**, **left**, **right** or **outer**."
    )
    cells = []
    for i, how in enumerate(order, start=1):
        cells.append(
            r"\begin{minipage}[t]{0.48\linewidth}\centering"
            + rf"\textbf{{Result {i}}}\\[3pt]\small " + _small_table(results[how])
            + r"\\[5pt]\normalsize how = " + blank_line("2.6cm") + r"\end{minipage}"
        )
    body = raw_latex(
        r"\noindent" + cells[0] + r"\hfill" + cells[1] + r"\\[12pt]" + "\n"
        + r"\noindent" + cells[2] + r"\hfill" + cells[3]
    )
    why = {
        "A": ("S011 and S012 appear in both tables (3 loans): that's **inner**. **Left** keeps "
              "every loan, so L104 (student S015, not in `students`) appears with class_year NaN. "
              "**Right** keeps every student, so S013 (no loans) appears with loan_id NaN. "
              "**Outer** keeps both, so it has both NaN rows."),
        "B": ("S023 and S024 appear in both tables (3 loans): that's **inner**. **Left** keeps "
              "every loan, so L201 (student S021, not in `students`) appears with class_year NaN. "
              "**Right** keeps every student, so S022 (no loans) appears with loan_id NaN. "
              "**Outer** keeps both, so it has both NaN rows."),
    }
    answer = ["| Result | how= | rows |", "|---|---|---|"]
    answer += [f"| {i} | **{how}** | {len(results[how])} |" for i, how in enumerate(order, start=1)]
    answer += ["", why[letter], "",
               "Left and right both give 4 rows here, so the row count alone can't tell them "
               "apart: look at **which side has the NaN**."]
    return Question(Q8_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 9 (SLO 04C) -- RETAKE: wide -> long (sketch the melted table)
# ---------------------------------------------------------------------------

Q9_HEADING = "Question 9 (SLO 04C) --- Retake from Quiz 3"
MONTH_COLUMNS = ["student_id", "sep", "oct", "nov"]
# Real rows of monthly_loans (seed 8).
Q9_ROWS = {"A": [("S003", 0, 2, 1), ("S007", 2, 0, 2)], "B": [("S002", 0, 1, 1), ("S005", 1, 0, 1)]}
Q9_CODE = (
    "loans_long = pd.melt(\n"
    "    monthly_loans,\n"
    '    id_vars=["student_id"],\n'
    '    value_vars=["sep", "oct", "nov"],\n'
    '    var_name="month",\n'
    '    value_name="n_loans",\n'
    ")"
)


def _q9_question(letter):
    rows = Q9_ROWS[letter]
    intro = ("Here are two rows of the wide table `monthly_loans`. Sketch the part of "
             "`loans_long` that comes from these two rows: column names and every row.")
    body = (
        "\\footnotesize\n\n"
        + sample_table(MONTH_COLUMNS, _rows(MONTH_COLUMNS, rows), col_widths_cm=[2.4, 1.6, 1.6, 1.6])
        + "\n\n\\normalsize\n\n" + _code(Q9_CODE) + "\n" + _space("2.0in")
    )
    answer = [_md_code(Q9_CODE), "", "| student_id | month | n_loans |", "|---|---|---|"]
    for sid, *counts in rows:
        answer += [f"| {sid} | {m} | {c} |" for m, c in zip(["sep", "oct", "nov"], counts)]
    answer += ["", "6 rows: 2 wide rows × 3 month columns. Row order may differ "
               "(pd.melt lists all sep rows first, then oct, then nov); any order is fine."]
    return Question(Q9_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------

def _new_page(question):
    question.page_break_before = True
    return question


def _questions(letter):
    return [
        _q1_question(letter),                 # page 1: dataset + Q1
        _new_page(_q2_question(letter)),      # page 2: Q2-Q4
        _q3_question(letter),
        _q4_question(letter),
        _new_page(_q5_question(letter)),      # page 3: Q5-Q7
        _q6_question(letter),
        _q7_question(letter),
        _new_page(_q8_question(letter)),      # page 4: Q8-Q9
        _q9_question(letter),
    ]


CONTENT = QuizContent(
    title=TITLE,
    subtitle=SUBTITLE,
    dataset_intro_md=DATASET_INTRO_MD,
    sample_columns=LOAN_COLUMNS,
    sample_col_widths_cm=[2.4, 2.4, 2.4, 1.6],
    margin="0.7in",
    fontsize="10pt",
    versions={
        letter: QuizVersion(rows=_rows(LOAN_COLUMNS, LOANS[letter]), questions=_questions(letter),
                            extra_tables=_extra_tables(letter))
        for letter in ("A", "B")
    },
)
