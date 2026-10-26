"""Simulate datasets/shelter.csv (and shelter_hidden.csv) for Practice 07
(scaling, one-hot and ordinal encoding, pipelines, missing data).

2,000 animals that came into an animal shelter, and whether each was adopted within 30 days.
Simulated so that each Week 9 idea makes a visible difference:

* Different rulers: adoption_fee (dollars, sd ~$70) swamps age (years), weight (kg) and
  behavior_score (1-10) in an unscaled kNN.
* Words: species and intake_type (kinds, one-hot); size (a real rank, OrdinalEncoder).
* Adoption (logistic): better behavior and younger age help most; transfers (+), strays (-),
  rabbits (-), large and extra-large dogs (-).
* Three columns with blanks, one per mechanism:
    weight_kg       MCAR  7% of intake forms lost the weight box, at random
    age_years       MAR   blank for 40% of strays (no records), 3% of owner surrenders, 10% of transfers;
                          strays are younger, so a median fill is biased, but fee and weight hint at age
    behavior_score  MNAR  the assessment is skipped for stressed animals: blank for 85% of scores <= 3,
                          35% of 4s, 8% of 5s, 2% of the rest
* shelter_hidden.csv keeps the true age, weight and behavior of every animal (the Answer Key).

Usage: python scripts/make_shelter.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets"
N, SEED = 2000, 7

rng = np.random.default_rng(SEED)
species = rng.choice(["Dog", "Cat", "Rabbit"], N, p=[.55, .38, .07])
size = np.where(species == "Dog", rng.choice(["Small", "Medium", "Large", "Extra large"], N, p=[.25, .35, .3, .1]),
       np.where(species == "Cat", rng.choice(["Small", "Medium"], N, p=[.7, .3]), "Small"))
intake = rng.choice(["Stray", "Owner surrender", "Transfer"], N, p=[.45, .35, .20])
age = np.where(intake == "Stray", rng.gamma(1.3, 1.8, N), rng.gamma(1.8, 2.6, N)).clip(0.2, 17)

adult_kg = {("Dog", "Small"): 7, ("Dog", "Medium"): 18, ("Dog", "Large"): 32, ("Dog", "Extra large"): 45,
            ("Cat", "Small"): 4.2, ("Cat", "Medium"): 6, ("Rabbit", "Small"): 2}
growth = np.where(age < 1, 0.45 + 0.55 * age, 1.0)                     # young animals are still growing
weight = np.array([adult_kg[(s, z)] for s, z in zip(species, size)]) * growth * rng.lognormal(0, 0.15, N)

behavior = np.clip(np.round(rng.normal(6, 2, N)), 1, 10)
base_fee = np.select([species == "Dog", species == "Cat"], [150, 90], 45)
fee = base_fee * (0.6 + 1.6 * np.exp(-age / 2)) + rng.normal(0, 35, N)  # puppies and kittens cost more
fee = (np.round(fee.clip(0, 450) / 5) * 5).astype(int)

z = (0.4 + 0.9 * (behavior - 6) - 0.45 * (age - 3.5)
     + np.select([species == "Dog", species == "Rabbit"], [0.3, -1.0], 0)
     + np.select([size == "Large", size == "Extra large"], [-0.6, -1.2], 0)
     + np.select([intake == "Transfer", intake == "Stray"], [1.3, -0.5], 0))
adopted = (rng.random(N) < 1 / (1 + np.exp(-z))).astype(int)

df = pd.DataFrame({"animal_id": [f"A{i:04d}" for i in range(1, N + 1)], "species": species, "size": size,
                   "intake_type": intake, "age_years": age.round(1), "weight_kg": weight.round(1),
                   "behavior_score": behavior.astype(float), "adoption_fee": fee, "adopted": adopted})
hidden = df[["animal_id", "age_years", "weight_kg", "behavior_score"]].copy()

p_age = np.select([intake == "Stray", intake == "Owner surrender"], [.40, .03], .10)
p_behavior = np.select([behavior <= 3, behavior == 4, behavior == 5], [.85, .35, .08], .02)
df.loc[rng.random(N) < p_age, "age_years"] = np.nan
df.loc[rng.random(N) < .07, "weight_kg"] = np.nan
df.loc[rng.random(N) < p_behavior, "behavior_score"] = np.nan

df.to_csv(DATA / "shelter.csv", index=False)
hidden.to_csv(DATA / "shelter_hidden.csv", index=False)
print(f"wrote shelter.csv and shelter_hidden.csv ({len(df)} rows); adopted {df['adopted'].mean():.3f}")
print(df.isna().sum()[lambda s: s > 0].to_string())
