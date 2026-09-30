"""
Build weeks/06/class_w06d2_handout.pdf -- the printed in-class activities for
Week 6 Wednesday (train/test split, confusion matrix, precision and recall) --
from its editable source, weeks/06/class_w06d2_handout.md. Text and layout live
in the .md; the shared engine is scripts/handout.py. The handout has no plots:
every part is a table in the .md, with numbers from the notebook (k = 5) --
part 1 from its five-split loop, parts 2-3 from its split random_state=24.

Usage:  python scripts/make_w06d2_handout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import handout

ROOT = Path(__file__).resolve().parent.parent
SOURCE_MD = ROOT / "weeks" / "06" / "class_w06d2_handout.md"
OUT_PDF = ROOT / "weeks" / "06" / "class_w06d2_handout.pdf"


def make_plots(outdir):
    return {}   # no plots: every part is text and tables


if __name__ == "__main__":
    handout.build(SOURCE_MD, OUT_PDF, make_plots)
