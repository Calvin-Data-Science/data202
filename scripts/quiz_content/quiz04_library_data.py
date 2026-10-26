"""Simulated campus-library data behind Quiz 4 (scripts/quiz_content/quiz04.py).

There is no CSV on the course site -- the quiz only shows sample rows and
printed outputs. This script exists so those printed outputs (confusion
matrix, depth-2 tree, depth curve, grid-search table) come from a real run
instead of being made up. Re-run it and paste the numbers into quiz04.py if
you change anything here:

    python scripts/quiz_content/quiz04_library_data.py

Tables (all keyed the way the quiz describes):
    students       -- student_id (PK), class_year (1-4), prior_late (late
                      returns last year)
    books          -- book_id (PK), genre, pages
    loans          -- loan_id (PK), student_id (FK -> students),
                      book_id (FK -> books), late (1 = returned late)
    monthly_loans  -- student_id (PK), sep, oct, nov (wide: loans per month)
    model data     -- loans joined to students and books: features pages,
                      prior_late, class_year; label late.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, cross_validate, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

SEED = 8
N_STUDENTS, N_BOOKS, N_LOANS = 300, 200, 800
FEATURES = ["pages", "prior_late", "class_year"]


def make_tables(seed=SEED):
    rng = np.random.default_rng(seed)
    students = pd.DataFrame({
        "student_id": [f"S{i:03d}" for i in range(1, N_STUDENTS + 1)],
        "class_year": rng.integers(1, 5, N_STUDENTS),
        "prior_late": rng.poisson(1.3, N_STUDENTS).clip(0, 8),
    })
    books = pd.DataFrame({
        "book_id": [f"B{i:03d}" for i in range(1, N_BOOKS + 1)],
        "genre": rng.choice(["fiction", "textbook", "history", "science"], N_BOOKS),
        "pages": (rng.normal(350, 160, N_BOOKS).clip(60, 1000) // 10 * 10).astype(int),
    })
    loans = pd.DataFrame({
        "loan_id": [f"L{i:03d}" for i in range(1, N_LOANS + 1)],
        "student_id": rng.choice(students["student_id"], N_LOANS),
        "book_id": rng.choice(books["book_id"], N_LOANS),
    })
    data = loans.merge(students, on="student_id").merge(books, on="book_id")
    logit = (-2.4 + 0.9 * data["prior_late"] + 0.006 * (data["pages"] - 350)
             - 0.35 * (data["class_year"] - 2.5))
    data["late"] = (rng.random(len(data)) < 1 / (1 + np.exp(-logit))).astype(int)
    loans = loans.merge(data[["loan_id", "late"]], on="loan_id")
    monthly = (loans.assign(month=rng.choice(["sep", "oct", "nov"], N_LOANS))
               .pivot_table(index="student_id", columns="month", values="loan_id",
                            aggfunc="count", fill_value=0)[["sep", "oct", "nov"]]
               .reset_index())
    return students, books, loans, monthly, data


def report(data):
    X, y = data[FEATURES], data["late"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
    print("late share:", round(y.mean(), 3), "| train", len(X_train), "test", len(X_test))

    for k in (5, 15):
        knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_train, y_train)
        cm = confusion_matrix(y_test, knn.predict(X_test))
        tn, fp, fn, tp = cm.ravel()
        print(f"\nkNN k={k} test confusion [[TN FP] [FN TP]]:\n{cm}")
        print(f"  accuracy {(tp + tn) / cm.sum():.3f} precision {tp / (tp + fp):.3f} recall {tp / (tp + fn):.3f}")

    tree2 = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
    print("\ndepth-2 tree:\n" + export_text(tree2, feature_names=FEATURES, show_weights=True))

    print("depth | train (mean of folds) | CV")
    for d in [1, 2, 3, 4, 6, 8, None]:
        cv = cross_validate(DecisionTreeClassifier(max_depth=d, random_state=0), X_train, y_train,
                            cv=5, return_train_score=True)
        print(d, round(cv["train_score"].mean(), 3), round(cv["test_score"].mean(), 3))

    for grid in ({"max_depth": [2, 4, 6, None], "min_samples_leaf": [1, 10, 30]},
                 {"max_depth": [2, 3, 5], "min_samples_leaf": [1, 5, 20, 40]}):
        search = GridSearchCV(DecisionTreeClassifier(random_state=0), grid, cv=5).fit(X_train, y_train)
        res = pd.DataFrame(search.cv_results_)[["param_max_depth", "param_min_samples_leaf", "mean_test_score"]]
        print("\n", res.sort_values("mean_test_score", ascending=False).round(3).to_string(index=False))
        print("best", search.best_params_, round(search.best_score_, 3),
              "test", round(search.score(X_test, y_test), 3))


if __name__ == "__main__":
    students, books, loans, monthly, data = make_tables()
    print("students", students.shape, "books", books.shape, "loans", loans.shape, "monthly", monthly.shape)
    report(data)
