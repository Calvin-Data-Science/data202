"""
Build datasets/birdsong.csv (and weeks/05/images/birdsong_spectrograms.png) for
Practice 04 (weeks/05/practice04.ipynb) from the old Practice 10 pickle.

Source: birdsong.pkl -- 5,422 short clips cut from 477 Xeno-canto recordings of
5 North American species (from the BirdCLEF 2021 competition data), each clip
with a 64 x 258 spectrogram (64 pitch bands, lowest first, x 258 time steps).
That pickle is 359 MB -- too big and too slow for students -- so this script
keeps one small, readable summary per clip (one row per clip, ~11 per recording):

    band_00 ... band_63   the spectrogram averaged over time: how loud each of
                          the 64 pitch bands is, on average, across the clip
    loudest_band          the band (0-63) with the highest average loudness

plus who/where/what: recording_id (the recording the clip was cut from),
common_name, scientific_name, country, recordist, source_url (listen to the whole
recording on xeno-canto), license.

Recordings under CC BY-NC-ND ("no derivatives") licenses are dropped (100
recordings, 1,154 clips), since the band averages are derived from the
recordings. The remaining 377 recordings (4,268 clips) are CC BY-NC-SA / BY-SA,
so this derived file is shared under CC BY-NC-SA 4.0 with each row's attribution.

Usage:  python scripts/make_birdsong.py [path/to/birdsong.pkl]
        (without a path, the pickle is downloaded from the old course URL)
"""

import sys
import tempfile
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PICKLE_URL = "https://cs.calvin.edu/courses/data/202/fsantos/datasets/birdsong.pkl"
OUT_CSV = ROOT / "datasets" / "birdsong.csv"
OUT_PNG = ROOT / "weeks" / "05" / "images" / "birdsong_spectrograms.png"


def load_pickle(path=None):
    if path:
        return pd.read_pickle(path)
    with tempfile.TemporaryDirectory() as tmp:
        local = Path(tmp) / "birdsong.pkl"
        print(f"downloading {PICKLE_URL} (359 MB) ...")
        urllib.request.urlretrieve(PICKLE_URL, local)
        return pd.read_pickle(local)


def main():
    raw = load_pickle(sys.argv[1] if len(sys.argv) > 1 else None)
    keep = ~raw["license"].str.contains("-nd", regex=False)
    raw = raw[keep].reset_index(drop=True)
    spec = np.stack(raw["spectrogram"].map(np.asarray).values)        # (n, 64 bands, 258 time steps)
    bands = spec.mean(axis=2)                                         # average over time -> 64 numbers

    birds = pd.DataFrame({
        "recording_id": raw["id"],
        "common_name": raw["name"],
        "scientific_name": raw["genus"] + " " + raw["species"],
        "country": raw["country"],
        "recordist": raw["recordist"],
        "source_url": "https:" + raw["source_url"],
        "license": "https:" + raw["license"],
        "loudest_band": bands.argmax(axis=1),
    })
    band_cols = pd.DataFrame(bands.round(4), columns=[f"band_{i:02d}" for i in range(bands.shape[1])])
    birds = pd.concat([birds, band_cols], axis=1)
    birds.to_csv(OUT_CSV, index=False, lineterminator="\n")
    print(f"Wrote {OUT_CSV}: {birds.shape[0]} clips from {birds['recording_id'].nunique()} recordings x "
          f"{birds.shape[1]} columns ({OUT_CSV.stat().st_size / 1e6:.1f} MB); dropped {int((~keep).sum())} "
          f"no-derivatives clips")

    # one example per species: its spectrogram (top) and the 64 numbers it becomes (bottom)
    species = sorted(birds["common_name"].unique())
    fig, axes = plt.subplots(2, len(species), figsize=(13, 5.2), gridspec_kw=dict(height_ratios=[1.6, 1]))
    for col, name in enumerate(species):
        i = birds.index[birds["common_name"] == name][0]
        axes[0, col].imshow(spec[i], aspect="auto", origin="lower", cmap="magma")
        axes[0, col].set_title(name, fontsize=11, fontweight="bold")
        axes[0, col].set_xticks([]); axes[0, col].set_yticks([0, 63])
        axes[1, col].plot(range(64), bands[i], color="#2a78d6", lw=1.8)
        axes[1, col].set_xlim(0, 63); axes[1, col].set_ylim(bands.min() - 0.02, bands.max() + 0.02)
        axes[1, col].set_xticks([0, 32, 63]); axes[1, col].grid(color="#e0e0e0", lw=0.6)
        for side in ("top", "right"):
            axes[1, col].spines[side].set_visible(False)
    axes[0, 0].set_ylabel("pitch band", fontsize=9)
    for ax in axes[0]:
        ax.set_xlabel("time →", fontsize=9)
    axes[1, 0].set_ylabel("average\nloudness", fontsize=9)
    for ax in axes[1]:
        ax.set_xlabel("pitch band", fontsize=9)
    fig.suptitle("Top: one clip's spectrogram (pitch × time).  "
                 "Bottom: the same clip averaged over time — the 64 numbers in the dataset.",
                 fontsize=10.5, y=0.995)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=110)
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
