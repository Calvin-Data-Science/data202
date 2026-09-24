#!/usr/bin/env python3
"""
Turn a Gradescope quiz export (Quiz_NN_scores.csv) into mastery marks (A/P/N)
on the Marks sheet of grades.xlsx.

Each quiz CSV has one column per SLO, headed like "1: SLO 02A (2.0 pts)".
The score in each column is already a mastery level:

    0 -> N
    1 -> P
    2 -> A

and is written to the "<SLO>-Quiz" column (e.g. "02A-Quiz") of the matching
student's row, matched by First+Last name.

Only students with a graded submission are marked. Rows whose Status is
"Missing" (no submission, blank scores) are left blank rather than marked N,
same as the practice script leaves ungradable submissions for follow-up.
Any score that isn't exactly 0, 1 or 2 is reported and left blank.

Cells that already hold a value are left untouched, same policy as
update_attendance_from_quiz.py and assign_practice_grades.py — pass --force
to overwrite them with what the CSV says.

Usage:
    cd grades/
    python3 assign_quiz_grades.py                    # every Quiz_*_scores.csv found
    python3 assign_quiz_grades.py Quiz_01_scores.csv  # target specific file(s)
    python3 assign_quiz_grades.py --dry-run
    python3 assign_quiz_grades.py --force
"""

import csv
import glob
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime

import openpyxl

QUIZ_CSV_GLOB = "Quiz_*_scores.csv"
SLO_COL_RE = re.compile(r"SLO\s+(\d{2}[A-Z])\b")
LEVELS = {0: "N", 1: "P", 2: "A"}


def norm(s):
    """Case/accents/whitespace-insensitive name key ('Téa' == 'tea')."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(s.split()).lower()


def load_quiz_marks(csv_path):
    """Return ({name_key: {slo: mark or None}}, ordered SLO list, {name_key: status}, display names).

    A mark is None when the student has no graded submission or the score
    isn't one of 0/1/2.
    """
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"{csv_path}: no rows found")

    slo_cols = {}
    for col in rows[0].keys():
        m = SLO_COL_RE.search(col or "")
        if m:
            slo_cols[m.group(1)] = col
    if not slo_cols:
        sys.exit(f"{csv_path}: no columns matching 'SLO NNX' found (headers: {list(rows[0].keys())})")
    slos = sorted(slo_cols)

    marks, status_of, display, bad_scores = {}, {}, {}, []
    for row in rows:
        first, last = (row.get("First Name") or "").strip(), (row.get("Last Name") or "").strip()
        if not first and not last:
            continue
        key = norm(f"{first} {last}")
        display[key] = f"{first} {last}"
        status = (row.get("Status") or "").strip()
        status_of[key] = status

        per_slo = {}
        for slo, col in slo_cols.items():
            raw = (row.get(col) or "").strip()
            if status != "Graded" or raw == "":
                per_slo[slo] = None
                continue
            try:
                level = LEVELS.get(float(raw)) if float(raw).is_integer() else None
            except ValueError:
                level = None
            if level is None:
                bad_scores.append((display[key], slo, raw))
            per_slo[slo] = level
        marks[key] = per_slo

    return marks, slos, status_of, display, bad_scores


def process_csv(ws, header, csv_path, dry_run, force):
    marks, slos, status_of, display, bad_scores = load_quiz_marks(csv_path)
    print(f"{os.path.basename(csv_path)}: {len(slos)} SLO(s) found: {', '.join(slos)}")

    target_cols = {}
    for slo in slos:
        col_name = f"{slo}-Quiz"
        if col_name not in header:
            print(f"  SKIPPING SLO {slo}: no '{col_name}' column on the Marks sheet")
            continue
        target_cols[slo] = header.index(col_name) + 1  # openpyxl is 1-indexed
    if not target_cols:
        return False

    fn_col, ln_col = header.index("First Name") + 1, header.index("Last Name") + 1
    name_to_row = {}
    for r in range(2, ws.max_row + 1):
        fn, ln = ws.cell(r, fn_col).value, ws.cell(r, ln_col).value
        if fn is None and ln is None:
            continue
        name_to_row[norm(f"{fn or ''} {ln or ''}")] = r

    changes = []      # (row, name, slo, old, new)
    skipped = []      # (row, name, slo, existing, csv_value)
    no_submission = []
    unmatched = []

    for key, per_slo in marks.items():
        row_idx = name_to_row.get(key)
        if row_idx is None:
            unmatched.append(display[key])
            continue
        if status_of[key] != "Graded":
            no_submission.append((display[key], status_of[key] or "no status"))
            continue

        for slo, col_idx in target_cols.items():
            new_val = per_slo[slo]
            if new_val is None:
                continue
            cell = ws.cell(row_idx, col_idx)
            old_val = cell.value
            if old_val is not None and not force:
                if old_val != new_val:
                    skipped.append((row_idx, display[key], slo, old_val, new_val))
                continue
            if old_val != new_val:
                changes.append((row_idx, display[key], slo, old_val, new_val))
            if not dry_run:
                cell.value = new_val

    print(f"  {len(changes)} cell(s) {'would change' if dry_run else 'changed'}:")
    for r, name, slo, old, new in changes:
        print(f"    row {r:>2}  {name:<28} {slo}-Quiz  {old!r:>6} -> {new!r}")

    if skipped:
        print(f"  {len(skipped)} cell(s) already had a different value and were left as-is "
              f"(pass --force to overwrite):")
        for r, name, slo, old, new in skipped:
            print(f"    row {r:>2}  {name:<28} {slo}-Quiz  kept {old!r} (CSV says {new!r})")

    if no_submission:
        print(f"  {len(no_submission)} student(s) have no graded submission and were left blank:")
        for name, status in no_submission:
            print(f"    {name}: {status}")

    if bad_scores:
        print(f"  WARNING: {len(bad_scores)} score(s) weren't 0/1/2 and were left blank:")
        for name, slo, raw in bad_scores:
            print(f"    {name}: SLO {slo} = {raw!r}")

    if unmatched:
        print(f"  WARNING: {len(unmatched)} name(s) from the CSV were not found on the Marks roster:")
        for name in unmatched:
            print(f"    {name}")

    return bool(changes)


def main():
    argv = sys.argv[1:]
    dry_run = "--dry-run" in argv
    force = "--force" in argv
    argv = [a for a in argv if a not in ("--dry-run", "--force")]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(script_dir, "grades.xlsx")
    if not os.path.exists(xlsx_path):
        sys.exit(f"File not found: {xlsx_path}")

    if argv:
        csv_paths = argv
        for p in csv_paths:
            if not os.path.exists(p):
                sys.exit(f"File not found: {p}")
    else:
        csv_paths = sorted(glob.glob(os.path.join(script_dir, QUIZ_CSV_GLOB)))
        if not csv_paths:
            sys.exit(f'No files matching "{QUIZ_CSV_GLOB}" found in {script_dir}.')
        print(f"No file given on the command line — found {len(csv_paths)} quiz report(s):")
        for p in csv_paths:
            print(f"  {os.path.basename(p)}")
        print()

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["Marks"]
    header = [c.value for c in ws[1]]
    if "First Name" not in header or "Last Name" not in header:
        sys.exit("Marks sheet needs 'First Name' and 'Last Name' columns")

    any_changes = False
    for i, csv_path in enumerate(csv_paths):
        if process_csv(ws, header, csv_path, dry_run=dry_run, force=force):
            any_changes = True
        if i < len(csv_paths) - 1:
            print()

    if dry_run:
        print("\nDry run — no files were modified.")
        return

    if not any_changes:
        print("\nNo changes to save.")
        return

    backup_path = os.path.join(script_dir, f"grades_backup_{datetime.now():%Y%m%d_%H%M%S}.xlsx")
    shutil.copy2(xlsx_path, backup_path)
    wb.save(xlsx_path)
    print(f"\nSaved {xlsx_path}")
    print(f"Backup of the previous version: {backup_path}")


if __name__ == "__main__":
    main()
