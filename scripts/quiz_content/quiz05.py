"""Content for Quiz 5 (Week 11): six NEW questions on Week 9's SLOs (09A/09B/09C)
and Week 10's SLOs (10A/10B/10C), then six questions retaking Quiz 4's SLOs
(06A-07C), per the syllabus's repeat-questions-between-quizzes policy.

The retakes use NEW formats (the user, 2026-11-10): not the Quiz 4 formats (kNN by
hand, metrics from a confusion matrix, the fit/predict/score flow, follow a tree,
pick a depth from a CV table, count grid-search fits), and a little harder in
understanding, not longer or more arithmetic.

Two questions depend on having done the practices: Q3 (09C, what Practice 07 did
about the blank ages and behavior scores) and Q9 (06C, Practice 05's
train_test_split line).

Simplified at the user's request (2026-11-10, same day): Q2 asks only why to choose a
pipeline over line-by-line steps; Q3 asks only mechanism + what Practice 07 did
(options: drop / SimpleImputer / KNNImputer / add indicator); Q5 has no alpha
follow-up; Q6 has no R^2 (negative R^2 wasn't taught); Q8 asks only "precision or
recall"; Q9 is about the split, not the vectorizer; Q11 keeps only "how many rows
per round".

Dataset: a simulated campus coffee shop, used by every question except Q3, Q8 and
Q9. The printed numbers in Q4, Q5 and Q7 come from a real run of
scripts/quiz_content/quiz05_coffee_data.py: re-run it and update the numbers here
if that script changes. Q6's MAE/RMSE are made up. Q10's points and Q11's fold
scores are hand-made.

Layout: 12 questions on 5 pages (dataset + Q1 | Q2-Q4 | Q5-Q7 | Q8-Q9 | Q10-Q12).
"""

from build_quiz import (
    QuizContent, QuizVersion, Question,
    blank_table, code_box, blank_line, sketch_box, sample_table, tex_escape, raw_latex,
)
from quiz_content.quiz05_coffee_data import make_orders

TITLE = "DATA 202 --- Quiz 5"
SUBTITLE = "Week 11 --- Preprocessing, Missing Data & Regression, plus Retakes of Weeks 6--7"

DATASET_INTRO_MD = r"""
## The Dataset: The Campus Coffee Shop

The campus coffee shop promises: *your drink in 5 minutes, or a free cookie.* It
recorded 800 orders (simulated data), split into **600 training** and **200 test**
orders. Most questions use them.

- `minutes_since_open`: when the order was placed (0 = 7 am, 780 = 8 pm)
- `queue_length`: people ahead in line; `baristas`: baristas working (1--3)
- `drink` (latte, drip, tea or smoothie), `size` (S, M or L), `items`: drinks in the order
- `wait_minutes`: how long the customer waited (**the label** for regression)
- `late`: 1 = waited more than 5 minutes (**the label** for classification)

**A few rows of `orders`:**
"""

ORDER_COLUMNS = ["order_id", "minutes_since_open", "queue_length", "baristas", "drink", "size", "items",
                 "wait_minutes", "late"]
SAMPLE_IDS = {"A": ["C001", "C005", "C006", "C009", "C012"], "B": ["C002", "C008", "C011", "C013", "C014"]}


def _sample_rows(letter):
    orders = make_orders().set_index("order_id")
    rows = []
    for oid in SAMPLE_IDS[letter]:
        r = orders.loc[oid]
        rows.append({"order_id": oid, **{c: str(r[c]) for c in ORDER_COLUMNS[1:]}})
    return rows


# ---------------------------------------------------------------------------
# Helpers (as in quiz04)
# ---------------------------------------------------------------------------

def _code_lines(code):
    """Plain code -> code_box() lines. Each 4 leading spaces become a 1.5em indent;
    everything else is tex_escape'd."""
    lines = []
    for line in code.split("\n"):
        indent = len(line) - len(line.lstrip(" "))
        prefix = r"\hspace*{%.1fem}" % (1.5 * indent / 4) if indent else ""
        lines.append(prefix + tex_escape(line.lstrip(" ")) or r"\mbox{}")
    return lines


def _code(code):
    return code_box(_code_lines(code))


def _md_code(code):
    return "```python\n" + code + "\n```"


def _space(height):
    return sketch_box(height)


# ---------------------------------------------------------------------------
# Question 1 (SLO 09A) -- choose a preprocessing step per column
# ---------------------------------------------------------------------------

Q1_HEADING = "Question 1 (SLO 09A)"
Q1_ROWS = {
    "A": [("minutes_since_open", "0 to 780"), ("drink", "latte, drip, tea, smoothie"),
          ("queue_length", "0 to 16"), ("size", "S, M, L")],
    "B": [("size", "S, M, L"), ("queue_length", "0 to 16"),
          ("drink", "latte, drip, tea, smoothie"), ("minutes_since_open", "0 to 780")],
}
Q1_WHY = {
    "minutes_since_open": ("**StandardScaler**: a number on a much bigger ruler (0--780) than the others. "
                           "Unscaled, it would decide almost every distance kNN measures."),
    "queue_length": ("**StandardScaler**: a number. Scaling puts it on the same ruler as the other numbers, "
                     "so each column counts about the same."),
    "drink": ("**OneHotEncoder**: words with no order. Numbering them 1--4 would invent distances "
              "(tea \"closer\" to drip than to smoothie); one 0/1 column per drink keeps every drink equally far apart."),
    "size": ("**OrdinalEncoder** (S < M < L): the order is real, so codes 0, 1, 2 keep it. "
             "(OneHotEncoder also works, but it throws the order away.)"),
}


def _q1_question(letter):
    rows = Q1_ROWS[letter]
    intro = ("A kNN model will predict `late` from the four columns below. For each column, choose the "
             "preprocessing step it needs, **StandardScaler**, **OneHotEncoder** or **OrdinalEncoder**, "
             "and say why in a few words.")
    # Like blank_table, but with taller rows so there is room to write the reason.
    lines = [r"\begin{tabular}{|>{\ttfamily\raggedright\arraybackslash}p{3.3cm}|>{\raggedright\arraybackslash}p{3.4cm}"
             r"|p{3.0cm}|p{6.4cm}|}\hline",
             r"Column & Values & Step & Why? \\ \hline"]
    lines += [rf"{tex_escape(c)} & {tex_escape(v)} & \rule[-0.6cm]{{0pt}}{{0.95cm}} & \\ \hline" for c, v in rows]
    lines.append(r"\end{tabular}")
    body = raw_latex("\n".join(lines))
    answer = ["| Column | Step and why |", "|---|---|"]
    answer += [f"| `{c}` | {Q1_WHY[c]} |" for c, _v in rows]
    answer += ["", "Every number column gets scaled, not only the biggest one: kNN adds up the "
               "differences in every column, so each needs the same ruler."]
    return Question(Q1_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 2 (SLO 09B) -- why choose a pipeline over line-by-line steps
# ---------------------------------------------------------------------------

Q2_HEADING = "Question 2 (SLO 09B)"
BY_HAND = ("scaler = StandardScaler().fit(X_train)\n"
           "knn = KNeighborsClassifier(n_neighbors=25).fit(scaler.transform(X_train), y_train)\n"
           "predictions = knn.predict(scaler.transform(X_test))")
PIPE = ("model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=25))\n"
        "model.fit(X_train, y_train)\n"
        "predictions = model.predict(X_test)")
Q2_ORDER = {"A": (BY_HAND, PIPE), "B": (PIPE, BY_HAND)}


def _q2_question(letter):
    first, second = Q2_ORDER[letter]
    pipe_label = "Code 2" if letter == "A" else "Code 1"
    intro = ("Two classmates scale the four number columns and train kNN. Both cells give exactly the same "
             "predictions.")
    body = (
        "**Code 1**\n\n" + _code(first) + "\n**Code 2**\n\n" + _code(second) + "\n"
        f"Why would you choose the pipeline ({pipe_label}) over doing the steps line by line? Explain.\n\n"
        + _space("1.0in")
    )
    answer = (
        f"Any sound reason (one well explained is enough):\n\n"
        "- **One object holds every step, in order.** `fit` and `predict` run them all, so new or test orders "
        "always get exactly the same preprocessing as the training orders: you can't forget to scale them, or "
        "scale them the wrong way.\n"
        "- **It works with `cross_val_score` and `GridSearchCV`**: they redo every step in each fold, and can "
        "tune the steps' knobs (e.g. `kneighborsclassifier__n_neighbors`).\n"
        "- **Less code, fewer mistakes, reproducible**: the whole workflow is one object you can save, share and "
        "rerun."
    )
    return Question(Q2_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 3 (SLO 09C) -- Practice 07: mechanism and fix for age and behavior
# ---------------------------------------------------------------------------

Q3_HEADING = "Question 3 (SLO 09C) --- From Practice 07"
Q3_NOTES = {
    "age_years": "\"Strays usually come with no records\" (and most animals with no age are strays).",
    "behavior_score": ("\"Staff skip the temperament assessment when an animal is too stressed or reactive "
                       "to assess safely.\""),
}
Q3_ANSWER = {
    "age_years": ("**MAR**: the blanks depend on something we can see (strays are 40% blank, other animals "
                  "3–10%), not on the age itself.",
                  "**KNNImputer** (after scaling): each blank age is filled from the 5 most similar animals "
                  "(fix C)."),
    "behavior_score": ("**MNAR**: the blanks depend on the missing score itself (the stressed or reactive "
                       "animals would have scored low).",
                       "**SimpleImputer** (median) **+ add an indicator variable** (`add_indicator=True`), so "
                       "the model can still see \"not assessed\" (fix D)."),
}
Q3_ORDER = {"A": ["age_years", "behavior_score"], "B": ["behavior_score", "age_years"]}


def _q3_question(letter):
    order = Q3_ORDER[letter]
    intro = (
        "In Practice 07 (animal shelter), two columns had blanks. What the staff said about them is in the "
        "table. For each column, write the **mechanism** (MCAR, MAR or MNAR) and **what you did about it in "
        "Practice 07**: **drop** the rows, **SimpleImputer** (one median), **KNNImputer** (similar animals), "
        "**add an indicator variable**, or a mix."
    )
    lines = [r"\begin{tabular}{|>{\ttfamily\raggedright\arraybackslash}p{2.6cm}|>{\raggedright\arraybackslash}p{5.2cm}"
             r"|p{2.4cm}|p{5.6cm}|}\hline",
             r"Column & The staff said & Mechanism & What you did in Practice 07 \\ \hline"]
    lines += [rf"{tex_escape(c)} & {tex_escape(Q3_NOTES[c])} & \rule[-0.9cm]{{0pt}}{{1.2cm}} & \\ \hline"
              for c in order]
    lines.append(r"\end{tabular}")
    body = raw_latex("\n".join(lines))
    answer = ["| Column | Mechanism | What Practice 07 did |", "|---|---|---|"]
    answer += [f"| `{c}` | {Q3_ANSWER[c][0]} | {Q3_ANSWER[c][1]} |" for c in order]
    return Question(Q3_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 4 (SLO 10A) -- interpret slopes; the baristas sign flip
# ---------------------------------------------------------------------------

Q4_HEADING = "Question 4 (SLO 10A)"
# Real run (600 training orders): alone 3.46 + 0.36 x baristas; both 3.26 + 0.76 x queue - 1.41 x baristas.
# Mean queue_length by baristas: 2.67 (1), 4.60 (2), 8.21 (3).
Q4_LINES = (r"\begin{center}\begin{tabular}{ll}" + "\n"
            r"two columns: & predicted wait $= 3.26 + 0.76 \times{}$ \texttt{queue\_length} ${} - 1.41 \times{}$ "
            r"\texttt{baristas} \\" + "\n"
            r"\texttt{baristas} alone: & predicted wait $= 3.46 + 0.36 \times{}$ \texttt{baristas} \\" + "\n"
            r"\end{tabular}\end{center}")
Q4_TASK = {
    "A": ("**(a)** Explain the **0.76** in one sentence, with units. **(b)** Alone, more baristas go with "
          "*longer* waits (+0.36); next to `queue_length`, with *shorter* waits (−1.41). Why?"),
    "B": ("**(a)** Explain the **−1.41** in one sentence, with units. **(b)** Why is the slope of `baristas` "
          "*positive* (+0.36) when it is the only column?"),
}
Q4_A = {
    "A": ("**(a)** Each extra person ahead in line adds about **0.76 minutes** (45 seconds) to the predicted "
          "wait, **for orders with the same number of baristas**."),
    "B": ("**(a)** Each extra barista cuts about **1.41 minutes** from the predicted wait, **for orders with "
          "the same queue length**."),
}
Q4_B = ("**(b)** The extra baristas work the rush hours, when the lines are long (training orders: 2.7 people "
        "ahead with 1 barista, 8.2 with 3). Alone, the `baristas` slope also carries those long rush-hour "
        "lines, so more baristas *go with* longer waits. With `queue_length` in the model, each slope means "
        "\"holding the other column fixed\": at the same queue, more baristas mean a shorter wait.")


def _q4_question(letter):
    intro = ("Two lines were fit on the 600 training orders to predict `wait_minutes`. The shop puts extra "
             "baristas on shift at the morning and lunch rush.")
    body = raw_latex(Q4_LINES) + "\n" + Q4_TASK[letter] + "\n\n" + _space("1.1in")
    return Question(Q4_HEADING, intro, body, Q4_A[letter] + "\n\n" + Q4_B)


# ---------------------------------------------------------------------------
# Question 5 (SLO 10B) -- tell plain / Ridge / Lasso apart from their slopes
# ---------------------------------------------------------------------------

Q5_HEADING = "Question 5 (SLO 10B)"
# Real run: 12 orders (seed 348), scaled columns; Ridge alpha=2, Lasso alpha=0.3.
Q5_SLOPES = {
    "plain": ["+13.91", "−11.96", "−2.33", "+1.30", "−1.00", "+0.40"],
    "Ridge": ["+1.45", "+0.80", "−1.67", "+0.19", "−0.47", "−0.06"],
    "Lasso": ["+2.31", "0", "−1.47", "0", "−0.06", "0"],
}
Q5_COLUMNS = ["queue_length", "people_inside", "baristas", "items", "minutes_since_open", "outdoor_temp"]
Q5_ORDER = {"A": ["Ridge", "plain", "Lasso"], "B": ["Lasso", "Ridge", "plain"]}
Q5_CLUE = {
    "plain": ("**plain `LinearRegression`**: huge slopes with opposite signs on the near-copies "
              "(+13.91 and −11.96 minutes per SD, on 12 orders that average 3.8 minutes): a tug of war that "
              "cancels on these 12 orders only. It even gives `outdoor_temp` a slope. Overfitting."),
    "Ridge": ("**Ridge**: every slope is smaller, the near-copies *share* the effect (+1.45 and +0.80), "
              "and no slope is exactly 0."),
    "Lasso": ("**Lasso**: some slopes are **exactly 0** (`people_inside`, `items`, `outdoor_temp`): it keeps "
              "one of the two near-copies and drops the unrelated column."),
}


def _q5_question(letter):
    order = Q5_ORDER[letter]
    names = ["Model X", "Model Y", "Model Z"]
    intro = (
        "Suppose the shop had recorded only **12 orders**. Three models were fit on them, on scaled columns: "
        "a plain `LinearRegression`, a `Ridge` and a `Lasso`. Two columns are new: `people_inside` (almost "
        "a copy of `queue_length`: correlation 0.99) and `outdoor_temp` (it has nothing to do with waits). "
        "The slopes, in minutes per standard deviation:"
    )
    columns = ["column"] + names
    rows = [dict(zip(columns, [c] + [Q5_SLOPES[m][i] for m in order])) for i, c in enumerate(Q5_COLUMNS)]
    body = (
        "\\footnotesize\n\n" + sample_table(columns, rows, col_widths_cm=[3.6, 2.2, 2.2, 2.2])
        + "\n\n\\normalsize\n\n"
        "Name each model (plain, Ridge or Lasso), and give one clue from its slopes.\n\n"
        + raw_latex(r"Model X: " + blank_line("3cm") + r" \quad Model Y: " + blank_line("3cm")
                    + r" \quad Model Z: " + blank_line("3cm"))
        + _space("0.9in")
    )
    answer = ["| | model | clue |", "|---|---|---|"]
    answer += [f"| {n} | {m} | {Q5_CLUE[m]} |" for n, m in zip(names, order)]
    return Question(Q5_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 6 (SLO 10C) -- MAE vs RMSE: which model makes a few big misses?
# ---------------------------------------------------------------------------

Q6_HEADING = "Question 6 (SLO 10C)"
# Made-up MAE/RMSE (minutes).
Q6_TABLE = {
    "A": [("Model 1", "1.1", "1.4"), ("Model 2", "0.9", "2.2")],
    "B": [("Model 1", "1.0", "2.3"), ("Model 2", "1.2", "1.5")],
}
Q6_BIG = {"A": ("Model 2", "0.9", "2.2", "Model 1", "1.1", "1.4"), "B": ("Model 1", "1.0", "2.3", "Model 2", "1.2", "1.5")}
Q6_COLUMNS = ["model", "MAE (minutes)", "RMSE (minutes)"]


def _q6_question(letter):
    rows = [dict(zip(Q6_COLUMNS, r)) for r in Q6_TABLE[letter]]
    intro = "Two models predict `wait_minutes` for the 200 test orders:"
    body = (
        "\\footnotesize\n\n" + sample_table(Q6_COLUMNS, rows, col_widths_cm=[2.4, 3.0, 3.0])
        + "\n\n\\normalsize\n\n"
        "Which model makes a **few very large** misses? How do the numbers show it?\n\n"
        + _space("0.9in")
    )
    big, b_mae, b_rmse, even, e_mae, e_rmse = Q6_BIG[letter]
    answer = (
        f"**{big}.** Its typical miss is the smaller one (MAE {b_mae} min), but RMSE squares each miss "
        f"before averaging, so a few big misses blow it up ({b_rmse} min, far above its MAE). {even}'s misses "
        f"are more even: its RMSE ({e_rmse}) is close to its MAE ({e_mae})."
    )
    return Question(Q6_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 7 (SLO 06A) -- RETAKE: match k to its scores
# ---------------------------------------------------------------------------

Q7_HEADING = "Question 7 (SLO 06A) --- Retake from Quiz 4"
# Real run: kNN on scaled minutes_since_open, queue_length, baristas, items.
# k=1 0.998/0.785, k=25 0.845/0.830, k=51 0.843/0.825, k=600 0.693/0.750 (= on-time shares).
Q7_SCORES = {1: ("0.998", "0.785"), 25: ("0.845", "0.830"), 51: ("0.843", "0.825"), 600: ("0.693", "0.750")}
Q7_KS = {"A": [1, 25, 600], "B": [1, 51, 600]}
Q7_PAIRS = {"A": {"P": 600, "Q": 1, "R": 25}, "B": {"P": 51, "Q": 600, "R": 1}}


def _q7_question(letter):
    ks, pairs = Q7_KS[letter], Q7_PAIRS[letter]
    intro = (
        f"Three kNN models (k = {ks[0]}, {ks[1]} and {ks[2]}, on scaled `minutes_since_open`, `queue_length`, "
        "`baristas` and `items`) predict `late`. Each was scored on the **600 training orders it learned "
        "from** and on the **200 test orders**. The pairs of scores are shuffled:"
    )
    columns = ["pair", "accuracy on training orders", "accuracy on test orders"]
    rows = [dict(zip(columns, [p, *Q7_SCORES[k]])) for p, k in pairs.items()]
    body = (
        "\\footnotesize\n\n" + sample_table(columns, rows, col_widths_cm=[1.6, 5.0, 5.0]) + "\n\n\\normalsize\n\n"
        + raw_latex(" \\qquad ".join(rf"k = {k}: pair " + blank_line("1.4cm") for k in ks))
        + "\nThen explain: why is k = 1 almost perfect on the training orders? What does k = 600 predict "
        "for **every** order?\n\n" + _space("0.9in")
    )
    match = ", ".join(f"k = {k} → **pair {p}**" for k in ks for p, kk in pairs.items() if kk == k)
    answer = (
        f"{match}.\n\n"
        "- **k = 1**: each training order's nearest neighbor is *itself*, so it just repeats its own label: "
        "it has memorized the training orders (0.998, not 1, because two identical orders had different "
        "labels). On new orders it drops to 0.785: **overfitting**.\n"
        "- **k = 600**: every training order is a neighbor, so the vote is always the majority, **on time**: "
        "the lazy model. Its scores are just the share of on-time orders (0.693 and 0.750): **underfitting**.\n"
        f"- k = {ks[1]} is in between, and best on the test orders."
    )
    return Question(Q7_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 8 (SLO 06B) -- RETAKE: precision or recall?
# ---------------------------------------------------------------------------

Q8_HEADING = "Question 8 (SLO 06B) --- Retake from Quiz 4"
Q8_SITUATIONS = {
    "A": [
        ("A spam filter that deletes every message it flags, with no junk folder to check (positive = spam).",
         "Precision", "A false positive deletes a real message (a job offer?) forever; a missed spam is "
         "only an annoyance."),
        ("A quick screening test for a serious disease that is treatable if caught early; everyone flagged "
         "gets a cheap follow-up test (positive = has the disease).",
         "Recall", "A false negative sends a sick person home untreated; a false positive costs only a "
         "follow-up test."),
        ("A foraging app that tells hikers which wild mushrooms are safe to eat (positive = safe).",
         "Precision", "A false positive calls a poisonous mushroom safe, and someone eats it; a false "
         "negative only leaves a good mushroom in the woods."),
    ],
    "B": [
        ("A smoke detector (positive = fire).",
         "Recall", "A false negative is a fire with no alarm; a false positive is a noisy kitchen."),
        ("A video app's filter that picks which videos may play on the kids' channel (positive = safe for kids).",
         "Precision", "A false positive shows an unsafe video to a child; a false negative only keeps a "
         "fine video off the channel."),
        ("A drone photographs a bridge and flags beams that may be cracked; an engineer then checks every "
         "flagged beam (positive = cracked).",
         "Recall", "A false negative leaves a cracked beam unchecked; a false positive costs an engineer "
         "a few minutes."),
    ],
}
Q8_FORMULAS = (r"\begin{center}"
               r"precision $= \dfrac{TP}{TP + FP}$ \qquad\qquad recall $= \dfrac{TP}{TP + FN}$\\[4pt]"
               r"\small TP = true positives, FP = false positives, FN = false negatives"
               r"\end{center}")


def _q8_question(letter):
    situations = Q8_SITUATIONS[letter]
    intro = "For each model below, which matters more: **precision** or **recall**?"
    body = raw_latex(Q8_FORMULAS) + "\n" + blank_table(
        given_cols=[("Model", "11.4cm", False)],
        blank_cols=[("Precision or recall?", "4.0cm")],
        rows=[[s] for s, _a, _w in situations],
    )
    answer = ["| Model | Answer | Why (for reference) |", "|---|---|---|"]
    answer += [f"| {s} | **{a}** | {w} |" for s, a, w in situations]
    answer += ["", "Precision has FP in its denominator, so it drops with every false alarm; recall has FN, so "
               "it drops with every miss. The metric that matters more is the one whose mistake costs more."]
    return Question(Q8_HEADING, intro, body, "\n".join(answer))


# ---------------------------------------------------------------------------
# Question 9 (SLO 06C) -- RETAKE: explain Practice 05's train/test split
# ---------------------------------------------------------------------------

Q9_HEADING = "Question 9 (SLO 06C) --- Retake from Quiz 4, Code from Practice 05"
Q9_CODE = (
    "text_train, text_test, y_train, y_test = train_test_split(sms[\"text\"], y, test_size=0.2,\n"
    "                                                          stratify=y, random_state=42)\n"
    'print(len(text_train), "training messages |", len(text_test), "test messages")'
)
Q9_TASK = {
    "A": ("In your own words: **(a)** what does the first line do? Include what `test_size=0.2` and "
          "`stratify=y` are for. **(b)** Why must the model never learn from `text_test`?"),
    "B": ("In your own words: **(a)** what do `text_train` and `y_train` hold, and what is `stratify=y` for? "
          "**(b)** The practice scored the model on `text_test`. Why not score it on the training messages?"),
}
Q9_ANSWER = {
    "A": ("**(a)** It shuffles the messages and splits them, with their labels, into **80% for training** "
          "(`text_train`, `y_train`) and **20% for testing** (`text_test`, `y_test`): that's `test_size=0.2`, "
          "1,032 of 5,160 messages. `stratify=y` keeps the **same share of spam** (about 1 in 8) in both parts, "
          "so the test set can't end up short of spam by chance. (`random_state=42` gives the same split every "
          "run.)\n\n"
          "**(b)** The test messages play the part of **new messages the model has never seen**. If the model "
          "learned from them, the test score would measure memory, not how well it works on new messages: "
          "too optimistic."),
    "B": ("**(a)** `text_train` holds 80% of the messages (the ones the model learns from); `y_train` holds their "
          "labels, spam or not, in the same order. `stratify=y` keeps the **same share of spam** (about 1 in 8) "
          "in the training and test parts, so neither ends up short of spam by chance.\n\n"
          "**(b)** On the messages it learned from, a model can score well just by **memorizing** them (kNN "
          "with k = 1 is almost perfect there). The test messages play the part of **new messages**, so their "
          "score shows how the filter will do on messages it has never seen."),
}


def _q9_question(letter):
    intro = ("This code is from Practice 05 (SMS spam). `sms` holds 5,160 text messages; `y` is True for spam "
             "(about 1 message in 8).")
    body = _code(Q9_CODE) + "\n" + Q9_TASK[letter] + "\n\n" + _space("1.3in")
    return Question(Q9_HEADING, intro, body, _md_code(Q9_CODE) + "\n\n" + Q9_ANSWER[letter])


# ---------------------------------------------------------------------------
# Question 10 (SLO 07A) -- RETAKE: draw the tree from its cuts
# ---------------------------------------------------------------------------

Q10_HEADING = "Question 10 (SLO 07A) --- Retake from Quiz 4"
# Hand-made training orders: (queue_length, baristas, late?). The cuts are the ones
# DecisionTreeClassifier(max_leaf_nodes=3) actually finds on these points (checked 2026-11-10).
Q10_POINTS = {
    "A": dict(late=[(4, 1), (7, 1), (9, 1), (11, 1), (10, 2)],
              ontime=[(1, 1), (3, 1), (2, 2), (5, 2), (4, 3), (7, 2), (9, 3), (11, 3), (8, 3)],
              vertical=(3.5, 0.5, 1.5), horizontal=(1.5, 0, 12.5)),
    "B": dict(late=[(5, 1), (7, 1), (9, 1), (11, 1), (9, 2)],
              ontime=[(1, 1), (2, 1), (3, 1), (6, 1), (2, 2), (5, 3), (6, 2), (8, 3), (11, 2), (12, 3)],
              vertical=(6.5, 0.5, 3.5), horizontal=(1.5, 6.5, 12.5)),
}
Q10_ANSWER = {
    "A": ("- **baristas <= 1.5?** yes → **queue_length <= 3.5?** yes → **on time** (2 on time); "
          "no → **late** (4 late)\n"
          "- no → **on time** (7 on time, 1 late)"),
    "B": ("- **queue_length <= 6.5?** yes → **on time** (7 on time, 1 late)\n"
          "- no → **baristas <= 1.5?** yes → **late** (3 late); no → **on time** (3 on time, 1 late)"),
}


def _q10_plot(p):
    ys = 0.85  # y units per barista
    lines = [r"\begin{tikzpicture}[x=0.62cm, y=1cm]",
             r"\draw[->] (0,0) -- (13.4,0);", r"\draw[->] (0,0) -- (0,%.2f);" % (3.7 * ys),
             r"\node at (6.5,-0.8) {\small queue\_length};",
             r"\node[rotate=90] at (-1.0,%.2f) {\small baristas};" % (2 * ys)]
    for i in range(0, 13):
        lines.append(r"\draw[gray!30, very thin] (%d,0) -- (%d,%.2f);" % (i, i, 3.4 * ys))
        lines.append(r"\node[below] at (%d,0) {\scriptsize %d};" % (i, i))
    for b in (1, 2, 3):
        lines.append(r"\draw[gray!30, very thin] (0,%.2f) -- (13,%.2f);" % (b * ys, b * ys))
        lines.append(r"\node[left] at (0,%.2f) {\scriptsize %d};" % (b * ys, b))
    for x, b in p["ontime"]:
        lines.append(r"\draw[thick] (%d,%.2f) circle (4pt);" % (x, b * ys))
    for x, b in p["late"]:
        lines.append(r"\fill (%d,%.2f) +(-0.14cm,-0.14cm) rectangle +(0.14cm,0.14cm);" % (x, b * ys))
    vx, vy0, vy1 = p["vertical"]
    hy, hx0, hx1 = p["horizontal"]
    lines.append(r"\draw[very thick, dashed] (%.1f,%.2f) -- (%.1f,%.2f);" % (vx, vy0 * ys, vx, vy1 * ys))
    lines.append(r"\draw[very thick, dashed] (%.1f,%.2f) -- (%.1f,%.2f);" % (hx0, hy * ys, hx1, hy * ys))
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def _q10_question(letter):
    p = Q10_POINTS[letter]
    intro = (
        "A small decision tree (two questions, three leaves) was fit on the training orders below (a "
        "**filled square** was **late**, an **open circle** on time). Its two cuts are the dashed lines. "
        "**Draw the tree**: the question at each split and the prediction at each leaf. Then answer the "
        "question below the drawing space."
    )
    body = (
        raw_latex(r"\begin{center}" + _q10_plot(p) + r"\\[2pt]\small $\blacksquare$ late \quad $\circ$ on time"
                  r"\end{center}")
        + _space("1.25in")
        + "**Then:** a tree with **no depth limit** would keep cutting until every leaf is pure. Compared with "
        "this tree, would it score higher or lower on these training orders? On new orders? Why?\n\n"
        + _space("0.55in")
    )
    answer = (
        Q10_ANSWER[letter] + "\n\n"
        "Each leaf predicts the majority of the training orders in its region. (The cut values don't have "
        "to be exact: any number between the two nearest points is right.)\n\n"
        "**No depth limit:** higher on the training orders (100%: it adds cuts around the odd orders), but "
        "probably **lower on new orders**, because those extra cuts chase noise: **overfitting**. A tree that "
        "is too shallow (depth 1) would underfit."
    )
    return Question(Q10_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 11 (SLO 07B) -- RETAKE: same mean, different spread
# ---------------------------------------------------------------------------

Q11_HEADING = "Question 11 (SLO 07B) --- Retake from Quiz 4"
# Hand-made fold scores; each pair of rows has the same mean.
Q11_FOLDS = {
    "A": dict(cv=5, learn=480, score=120, scores=["0.79", "0.80", "0.78", "0.81", "0.79"]),
    "B": dict(cv=4, learn=450, score=150, scores=["0.76", "0.74", "0.75", "0.75"]),
}


def _q11_question(letter):
    f = Q11_FOLDS[letter]
    intro = (f"A tree was scored with **{f['cv']}-fold cross-validation on the 600 training orders**. "
             "Its scores, one per round:")
    columns = [f"round {i}" for i in range(1, f["cv"] + 1)]
    rows = [dict(zip(columns, f["scores"]))]
    body = (
        "\\footnotesize\n\n" + sample_table(columns, rows, col_widths_cm=[1.6] * f["cv"])
        + "\n\n\\normalsize\n\n"
        "In each round, how many orders does the tree learn from, and how many is it scored on?\n\n"
        + raw_latex(r"learns from: " + blank_line("2cm") + r" \qquad scored on: " + blank_line("2cm"))
    )
    answer = (
        f"Learns from **{f['learn']}**, scored on **{f['score']}** (600 / {f['cv']} = {f['score']} held out). "
        f"Over the {f['cv']} rounds, each training order is held out exactly once."
    )
    return Question(Q11_HEADING, intro, body, answer)


# ---------------------------------------------------------------------------
# Question 12 (SLO 07C) -- RETAKE: choosing on the test set
# ---------------------------------------------------------------------------

Q12_HEADING = "Question 12 (SLO 07C) --- Retake from Quiz 4"
Q12_GRID = {
    "A": ("[2, 4, 6, 8, None]", "[1, 10, 30]", 15, "(4, 10) 0.84", "0.84"),
    "B": ("[2, 3, 5, 10]", "[5, 20]", 8, "(5, 20) 0.86", "0.86"),
}


def _q12_code(depths, leaves, printed):
    return (
        "best = 0\n"
        f"for depth in {depths}:\n"
        f"    for leaf in {leaves}:\n"
        "        tree = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=leaf)\n"
        "        tree.fit(X_train, y_train)\n"
        "        score = tree.score(X_test, y_test)\n"
        "        if score > best:\n"
        "            best, best_params = score, (depth, leaf)\n"
        f"print(best_params, best)     # {printed}"
    )


def _q12_question(letter):
    depths, leaves, n, printed, best = Q12_GRID[letter]
    code = _q12_code(depths, leaves, printed)
    intro = (f"A classmate tunes a tree with this loop, and reports **{best}** as the accuracy to expect "
             "on new orders:")
    body = (
        _code(code) + "\n"
        f"**(a)** Why is {best} too optimistic? **(b)** `GridSearchCV(DecisionTreeClassifier(), grid, cv=5)` "
        "runs the same search. What does it use, instead of `X_test`, to compare the combinations? When "
        "should `X_test` be used?\n\n" + _space("1.0in")
    )
    answer = (
        _md_code(code) + "\n\n"
        f"**(a)** The test set **chose** the winner: of {n} trees, it kept the one that happened to do best "
        f"on these 200 test orders, partly by luck. The best of {n} is optimistic, and the test set is no "
        "longer new data.\n\n"
        "**(b)** **Cross-validation on the training orders only**: each combination is scored on held-out "
        "folds of `X_train`. `X_test` is used **once, at the end**, to score the chosen model (refit on all "
        "the training orders)."
    )
    return Question(Q12_HEADING, intro, body, answer)


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
        _new_page(_q5_question(letter)),      # page 3: Q5-Q7 (retakes start at Q7)
        _q6_question(letter),
        _q7_question(letter),
        _new_page(_q8_question(letter)),      # page 4: Q8-Q9
        _q9_question(letter),
        _new_page(_q10_question(letter)),     # page 5: Q10-Q12
        _q11_question(letter),
        _q12_question(letter),
    ]


CONTENT = QuizContent(
    title=TITLE,
    subtitle=SUBTITLE,
    dataset_intro_md=DATASET_INTRO_MD,
    sample_columns=ORDER_COLUMNS,
    sample_col_widths_cm=[1.5, 2.9, 2.3, 1.7, 1.6, 1.0, 1.2, 2.2, 1.0],
    margin="0.7in",
    fontsize="10pt",
    versions={
        letter: QuizVersion(rows=_sample_rows(letter), questions=_questions(letter))
        for letter in ("A", "B")
    },
)
