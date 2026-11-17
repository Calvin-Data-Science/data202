"""Build datasets/songs.csv for Practice 09 (logistic regression, random forests and AdaBoost).

Source: TidyTuesday, 21 January 2020, "Spotify Songs" (CC0 1.0).
    https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21
    Collected by Kaylin Pavlik through Spotify's API with the spotifyr package
    (https://www.kaylinpavlik.com/classifying-songs-genres/).

The raw file has 32,833 rows: one per song *per playlist*. The genre is the playlist's genre, so the
same song can appear under several genres (Despacito is in pop, latin and edm playlists). This script:
  1. drops every song (same name and artist, ignoring case) found under more than one genre;
  2. drops songs whose title or artist has profanity or sexual words (for a classroom);
  3. keeps one row per song;
  4. draws 1,000 songs per genre (random_state=1): 6,000 songs, then shuffles them.
The year is the album's release year. Duration is converted from milliseconds to minutes.

Usage:  python scripts/make_songs.py [path/to/spotify_songs.csv]
        (without a path, the file is downloaded)
"""
import sys
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "songs.csv"
URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-01-21/spotify_songs.csv"
AUDIO = ["danceability", "energy", "loudness", "speechiness", "acousticness",
         "instrumentalness", "liveness", "valence", "tempo"]

raw = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else URL)
raw = raw.dropna(subset=["track_name", "track_artist"])

key = raw["track_name"].str.lower().str.strip() + " | " + raw["track_artist"].str.lower().str.strip()
genres_per_song = raw.groupby(key)["playlist_genre"].nunique()
one_genre = raw[key.map(genres_per_song).eq(1)]
words = r"f[u*][c*]k|sh[i*]t|b[i*]tch|n[i*]gg|\bpuss(?:y|ies)\b|\bhoes?\b|\bslut|\bwhore|motherf|\bsex"
clean = ~(one_genre["track_name"].str.contains(words, case=False, regex=True)
          | one_genre["track_artist"].str.contains(words, case=False, regex=True))
one_genre = one_genre[clean]
songs = one_genre.loc[~key[one_genre.index].duplicated()].copy()

songs["year"] = songs["track_album_release_date"].str[:4].astype(int)
songs["duration_min"] = (songs["duration_ms"] / 60_000).round(2)
songs = songs.rename(columns={"track_name": "song", "track_artist": "artist", "playlist_genre": "genre"})
songs = songs[["song", "artist", "year"] + AUDIO + ["duration_min", "genre"]]

songs = songs.groupby("genre", group_keys=False).sample(1000, random_state=1)
songs = songs.sample(frac=1, random_state=1).reset_index(drop=True)      # shuffle, so the genres are mixed

songs.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(songs)} songs")
print(songs["genre"].value_counts().to_string())
