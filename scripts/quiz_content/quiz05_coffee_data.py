"""Simulated campus coffee-shop data behind Quiz 5 (scripts/quiz_content/quiz05.py).

There is no CSV on the course site: the quiz only shows sample rows and printed
outputs. This script exists so those outputs come from a real run. Re-run it and
paste the numbers into quiz05.py if you change anything here:

    python scripts/quiz_content/quiz05_coffee_data.py

One table, `orders` (one row per order, 800 orders):
    order_id
    minutes_since_open  0-780 (the shop is open 7 am - 8 pm)
    queue_length        people ahead in line when the order was placed
    baristas            baristas on shift (1-3; more at rush hours)
    drink               latte / drip / tea / smoothie
    size                S / M / L
    items               drinks in the order (1-4)
    wait_minutes        the regression label
    late                1 = waited more than 5 minutes (the shop then gives a free cookie)

Used by: Q4 (two-column line + the baristas sign flip), Q5 (plain / Ridge / Lasso
slopes on 12 orders with a near-copy and an unrelated column, seed 348), Q7 (kNN,
k = 1 / 25 / 51 / all 600 training orders).
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 5
N = 800


def make_orders(seed=SEED):
    rng = np.random.default_rng(seed)
    minutes = rng.integers(0, 781, N)
    hour = 7 + minutes / 60
    rush = ((hour >= 7.75) & (hour < 9.25)) | ((hour >= 11.75) & (hour < 13.25))
    queue = rng.poisson(np.where(rush, 8, 2.5))
    baristas = np.clip(1 + rush + (rng.random(N) < 0.35) - (rng.random(N) < 0.15), 1, 3)
    drink = rng.choice(["latte", "drip", "tea", "smoothie"], N, p=[0.35, 0.3, 0.15, 0.2])
    size = rng.choice(["S", "M", "L"], N, p=[0.3, 0.45, 0.25])
    items = rng.choice([1, 2, 3, 4], N, p=[0.6, 0.25, 0.1, 0.05])
    drink_extra = pd.Series(drink).map({"latte": 0.8, "drip": 0.0, "tea": 0.2, "smoothie": 1.6}).to_numpy()
    wait = (1.5 + 0.8 * queue - 1.6 * baristas + 0.7 * items + drink_extra
            + 0.3 * (size == "L") + rng.normal(0, 1.4, N)).clip(0.5, None).round(1)
    return pd.DataFrame({
        "order_id": [f"C{i:03d}" for i in range(1, N + 1)],
        "minutes_since_open": minutes, "queue_length": queue, "baristas": baristas,
        "drink": drink, "size": size, "items": items,
        "wait_minutes": wait, "late": (wait > 5).astype(int),
    })


def report(orders):
    print(orders.head(8).to_string())
    print("late share:", round(orders["late"].mean(), 3), "| wait mean", round(orders["wait_minutes"].mean(), 2),
          "sd", round(orders["wait_minutes"].std(), 2))
    print("corr queue/baristas:", round(orders[["queue_length", "baristas"]].corr().iloc[0, 1], 3))

    train, test = train_test_split(orders, test_size=0.25, random_state=1)
    y_tr, y_te = train["wait_minutes"], test["wait_minutes"]

    # Q4: the baristas slope alone, then next to queue_length
    alone = LinearRegression().fit(train[["baristas"]], y_tr)
    both = LinearRegression().fit(train[["queue_length", "baristas"]], y_tr)
    print(f"\nQ4 alone: wait = {alone.intercept_:.2f} + {alone.coef_[0]:.2f} x baristas")
    print(f"Q4 both:  wait = {both.intercept_:.2f} + {both.coef_[0]:.2f} x queue + {both.coef_[1]:.2f} x baristas")
    print(train.groupby("baristas")[["queue_length", "wait_minutes"]].mean().round(2))

    # Q7: kNN on four scaled numbers, k = 1 / 25 / 51 / all
    cols = ["minutes_since_open", "queue_length", "baristas", "items"]
    print("\nQ7 kNN (train acc, test acc):")
    for k in (1, 25, 51, len(train)):
        knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(train[cols], train["late"])
        print(f"  k={k:3d}: {knn.score(train[cols], train['late']):.3f}, {knn.score(test[cols], test['late']):.3f}")
    print("  on-time share: train", round(1 - train["late"].mean(), 3), "test", round(1 - test["late"].mean(), 3))


def small_garage(orders, seed=348, n=12, ridge_alpha=2.0, lasso_alpha=0.3):
    """Q5: 12 orders, six columns: a near-copy of queue_length and an unrelated column.
    Seed 348 was picked from 400 for a clear pattern: plain = big opposite slopes on the
    near-copies, Ridge = both small and positive, Lasso = one near-copy and outdoor_temp at 0."""
    rng = np.random.default_rng(seed)
    few = orders.sample(n, random_state=seed).copy()
    few["people_inside"] = few["queue_length"] + rng.integers(0, 2, n)        # almost the same as the queue
    few["outdoor_temp"] = rng.integers(30, 80, n)                              # nothing to do with waits
    cols = ["queue_length", "people_inside", "baristas", "items", "minutes_since_open", "outdoor_temp"]
    out = {}
    for name, model in [("plain", LinearRegression()), ("ridge", Ridge(alpha=ridge_alpha)),
                        ("lasso", Lasso(alpha=lasso_alpha, max_iter=100_000))]:
        pipe = make_pipeline(StandardScaler(), model).fit(few[cols], few["wait_minutes"])
        out[name] = pipe[-1].coef_
    return pd.DataFrame(out, index=cols), few[cols].corr().loc["queue_length", "people_inside"]


if __name__ == "__main__":
    orders = make_orders()
    report(orders)
    slopes, corr = small_garage(orders)
    print(f"\nQ5 (seed 348): corr(queue, people_inside) = {corr:.2f}\n{slopes.round(2)}")
