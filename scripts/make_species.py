"""Simulate datasets/species.csv for Practice 06 (decision trees, cross-validation, grid search).

Same columns as the old Practice 07's species_habitat.csv, but re-simulated so that tree
depth shows clear underfitting and overfitting:

* Each site's organism follows simple rectangle rules (the kind a tree can learn):
    rainfall < 600 mm:            temperature > 18 °C → Reptile, else Mammal
    else elevation > 1500 m:      Bird
    else rainfall > 1800 mm:      Plant
    else temperature > 20 °C:     Insect, else Mammal
* 25% of sightings are replaced by a random organism (out-of-place sightings), so the best
  possible accuracy is about 0.75 + 0.25 / 5 = 0.80. Deeper trees memorize these.
* Temperature falls with elevation (6.5 °C per km, plus noise); rainfall is log-normal.
* habitat is a coarse summary of rainfall; soil is random.

Usage: python scripts/make_species.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "species.csv"
N, SEED, FLIP = 1000, 2026, 0.25
ORGANISMS = np.array(["Bird", "Insect", "Mammal", "Plant", "Reptile"])

rng = np.random.default_rng(SEED)
elev = rng.gamma(2.0, 550, N).clip(5, 4200)
temp = 27 - 6.5 * elev / 1000 + rng.normal(0, 5, N)
rain = rng.lognormal(np.log(1100), 0.8, N).clip(60, 4800)

organism = np.where(rain < 600, np.where(temp > 18, "Reptile", "Mammal"),
           np.where(elev > 1500, "Bird",
           np.where(rain > 1800, "Plant",
           np.where(temp > 20, "Insect", "Mammal"))))
out_of_place = rng.random(N) < FLIP
organism[out_of_place] = rng.choice(ORGANISMS, out_of_place.sum())

habitat = np.where(rain < 350, "Desert", np.where(rain > 2500, "Wetland", np.where(rain > 1200, "Forest", "Grassland")))
soil = rng.choice(["Sandy", "Clay", "Loamy", "Peaty", "Chalky"], N)

df = pd.DataFrame({"elevation_m": elev.round(1), "temperature_c": temp.round(1), "precipitation_mm": rain.round(1),
                   "soil": soil, "habitat": habitat, "organism": organism})
df.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(df)} rows)")
print(df["organism"].value_counts().to_string())
