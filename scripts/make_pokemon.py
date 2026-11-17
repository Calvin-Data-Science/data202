"""Build datasets/pokemon.csv for Practice 10 (Week 12: imbalanced data).

Source: A. Barradas, "Pokemon with Stats" (Kaggle, 2016), CC0: 800 Pokemon of generations 1-6,
    collected from pokemon.com, pokemondb and Bulbapedia. Mirrored as pokemon_data.csv in
    https://github.com/KeithGalli/pandas. Pokemon and Pokemon names are trademarks of Nintendo,
    Creatures and Game Freak; the stats are facts about the games.

The file has 800 rows because Mega Evolutions and other alternate forms share a Pokedex number with
their species (Mewtwo, Mega Mewtwo X, Mega Mewtwo Y...). Near-copies of one Pokemon on both sides of a
train/test split would leak, so this keeps ONE row per species (the first, the standard form):
721 Pokemon, 46 of them legendary (6.4%). Form names glued onto the species name
("DeoxysNormal Forme", "HoopaHoopa Confined") are cut back to the species ("Deoxys", "Hoopa").

Columns: name, type1, type2 (blank for single-type Pokemon), generation (1-6), the six base stats
hp, attack, defense, sp_attack, sp_defense, speed, and legendary (1 = legendary, 0 = not).
The label is the original file's: it is not always the games' own (Mew and Celebi, "mythical" in the
games, are 0; Jirachi and Arceus, also mythical, are 1). Practice 10 discusses this.

Usage:  python scripts/make_pokemon.py [path/to/pokemon_data.csv]
        (without a path, the file is downloaded from the GitHub mirror)
"""
import re
import sys
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "pokemon.csv"
URL = "https://raw.githubusercontent.com/KeithGalli/pandas/master/pokemon_data.csv"

raw = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else URL)
assert raw.shape == (800, 12)
species = raw.drop_duplicates("#", keep="first")

names = species["Name"].str.replace(r"^(.+?[a-z])[A-Z].*$", r"\1", regex=True)
changed = species["Name"] != names
print("form names cut back:", dict(zip(species.loc[changed, "Name"], names[changed])))

pokemon = pd.DataFrame({
    "name": names,
    "type1": species["Type 1"],
    "type2": species["Type 2"],
    "generation": species["Generation"],
    "hp": species["HP"],
    "attack": species["Attack"],
    "defense": species["Defense"],
    "sp_attack": species["Sp. Atk"],
    "sp_defense": species["Sp. Def"],
    "speed": species["Speed"],
    "legendary": species["Legendary"].astype(int),
})
assert len(pokemon) == 721 and pokemon["legendary"].sum() == 46 and pokemon["name"].is_unique

pokemon.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(pokemon)} Pokemon, {pokemon['legendary'].sum()} legendary)")
