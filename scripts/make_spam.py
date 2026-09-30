"""
Build datasets/spam.csv -- the SMS spam dataset for Practice 05
(Week 6, kNN classification, weeks/06/practice05.ipynb).

Source: the SMS Spam Collection (Almeida & Gomez Hidalgo, 2011), UCI Machine
Learning Repository, CC BY 4.0: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
The old practice used a Kaggle copy of the same data; that copy was re-encoded
badly (the pound sign became "å£") and has some messages split across columns,
so we go back to the original UCI file.

Two changes from the original:
  - HTML entities (&lt; &gt; &amp;) are turned back into characters.
  - Exact duplicate messages are dropped (414 of 5,574, mostly repeated spam
    templates). A message that sits in both the training and the test set
    would let k = 1 "find" it by memorizing, inflating the test score.

Columns: label ("ham" or "spam"), text.

Usage:  python scripts/make_spam.py [path/to/SMSSpamCollection]
        (with no path, the UCI zip is downloaded)
"""

import csv
import html
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"


def main():
    if len(sys.argv) > 1:
        raw = Path(sys.argv[1]).read_bytes()
    else:
        with urllib.request.urlopen(URL) as resp:
            raw = zipfile.ZipFile(io.BytesIO(resp.read())).read("SMSSpamCollection")

    sms = pd.read_csv(io.BytesIO(raw), sep="\t", header=None, names=["label", "text"],
                      quoting=csv.QUOTE_NONE, encoding="utf-8")
    sms["text"] = sms["text"].map(html.unescape).str.strip()
    sms = sms.drop_duplicates("text").reset_index(drop=True)

    out = ROOT / "datasets" / "spam.csv"
    sms.to_csv(out, index=False)
    print(f"wrote {out}: {len(sms)} messages", sms["label"].value_counts().to_dict())


if __name__ == "__main__":
    main()
