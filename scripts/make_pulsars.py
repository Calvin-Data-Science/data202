"""Build datasets/pulsars.csv for Week 12 Monday (imbalanced data).

Source: R. J. Lyon, "HTRU2" (2015), UCI Machine Learning Repository, doi:10.24432/C5DK6R, CC BY 4.0.
    Paper: R. J. Lyon, B. W. Stappers, S. Cooper, J. M. Brooke and J. D. Knowles (2016), "Fifty Years of
    Pulsar Candidate Selection: From simple filters to a new principled real-time classification approach,"
    Monthly Notices of the Royal Astronomical Society 459(1), 1104-1123.
    Raw observations: High Time Resolution Universe Survey (South), Parkes Observatory, CSIRO.

17,898 pulsar candidates, every one checked by a human: 1,639 real pulsars and 16,259 signals caused by
radio interference or noise. No missing values. Each candidate is described by 8 numbers:
    profile_*   mean, standard deviation, excess kurtosis and skewness of the integrated (folded) pulse
                profile: the signal averaged over many turns of the star. A pulsar gives a sharp, narrow
                spike once per turn; interference tends to look flat or messy.
    dmsnr_*     the same four statistics for the DM-SNR curve: signal strength across dispersion measures.
                A real pulsar's signal is smeared by its trip through interstellar space, so it peaks away
                from DM = 0; a signal made on Earth does not.
    pulsar      1 = real pulsar, 0 = interference/noise
Values are rounded to 3 decimals.

Usage:  python scripts/make_pulsars.py [path/to/HTRU_2.csv]
        (without a path, the UCI zip is downloaded)
"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "datasets" / "pulsars.csv"
URL = "https://archive.ics.uci.edu/static/public/372/htru2.zip"
NAMES = ["profile_mean", "profile_sd", "profile_kurtosis", "profile_skewness",
         "dmsnr_mean", "dmsnr_sd", "dmsnr_kurtosis", "dmsnr_skewness", "pulsar"]

if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read()))
    source = io.BytesIO(archive.read("HTRU_2.csv"))

pulsars = pd.read_csv(source, header=None, names=NAMES)
assert pulsars.shape == (17898, 9) and pulsars.notna().all().all()
pulsars = pulsars.round(3)
pulsars["pulsar"] = pulsars["pulsar"].astype(int)

pulsars.to_csv(OUT, index=False)
print(f"wrote {OUT} ({len(pulsars)} candidates)")
print(pulsars["pulsar"].value_counts().to_string())
