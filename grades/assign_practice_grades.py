#!/usr/bin/env python3
"""
Turn otter-grade output (grades_practiceNN.csv) into mastery marks (A/P/N) on
the Marks sheet of grades.xlsx.

Each practice CSV has one column per sub-question (e.g. 02A.1, 02A.2, 02A.3,
02B.1, ...) plus a "points-per-question" row giving each one's max score.
Sub-questions are grouped by their SLO prefix (e.g. "02A"), and each
student's mastery mark for that SLO is:

    percent = points earned in that SLO / points possible in that SLO
    >0.5            -> A
    >0.1 and <=0.5  -> P
    <=0.1           -> N

The mark is written to the "<SLO>-Practice" column (e.g. "02A-Practice") of
the matching student's row, matched by First+Last name.

Only rows with grading_status "Completed" are marked — a submission that
crashed the grader (wrong file, docker error, etc.) has no real percentage
to grade on, so it's left for manual follow-up instead of being marked N.

Cells that already hold a value are left untouched, same policy as
update_attendance_from_quiz.py — pass --force to recompute them anyway.

Usage:
    cd grades/
    python3 assign_practice_grades.py                        # every grades_practice*.csv found
    python3 assign_practice_grades.py grades_practice01.csv   # target specific file(s)
    python3 assign_practice_grades.py --dry-run
    python3 assign_practice_grades.py --force
"""

import csv
import glob
import os
import re
import shutil
import sys
from datetime import datetime

import openpyxl

PRACTICE_CSV_GLOB = "grades_practice*.csv"
QUESTION_RE = re.compile(r"^(\d{2}[A-Z])\.\d+$")


def slo_thresholds(pct):
    if pct > 0.5:
        return "A"
    if pct > 0.1:
        return "P"
    return "N"


def load_slo_scores(csv_path):
    """Return {student_file_stem: {slo: (earned, possible)}} and the ordered list of SLOs found."""
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        sys.exit(f"{csv_path}: no rows found")

    fieldnames = rows[0].keys()
    question_cols = [c for c in fieldnames if QUESTION_RE.match(c)]
    if not question_cols:
        sys.exit(f"{csv_path}: no question columns matching NNX.N found (headers: {list(fieldnames)})")

    slo_of = {c: QUESTION_RE.match(c).group(1) for c in question_cols}
    slos = sorted(set(slo_of.values()))

    points_row = next((r for r in rows if r.get("file", "").strip().lower() == "points-per-question"), None)
    if points_row is None:
        sys.exit(f"{csv_path}: no 'points-per-question' row found")
    max_points = {c: float(points_row[c]) for c in question_cols}

    by_student = {}
    for row in rows:
        fname = row.get("file", "").strip()
        if not fname or fname.lower() == "points-per-question":
            continue
        stem = fname[:-6] if fname.lower().endswith(".ipynb") else fname
        status = row.get("grading_status", "").strip()
        if status != "Completed":
            by_student[stem] = ("SKIP", status)
            continue

        per_slo = {}
        for slo in slos:
            cols = [c for c in question_cols if slo_of[c] == slo]
            earned = sum(float(row[c]) for c in cols)
            possible = sum(max_points[c] for c in cols)
            per_slo[slo] = (earned, possible)
        by_student[stem] = ("OK", per_slo)

    return by_student, slos


def process_csv(ws, header, csv_path, dry_run, force):
    by_student, slos = load_slo_scores(csv_path)
    print(f"{os.path.basename(csv_path)}: {len(slos)} SLO(s) found: {', '.join(slos)}")

    target_cols = {}
    for slo in slos:
        col_name = f"{slo}-Practice"
        if col_name not in header:
            print(f"  SKIPPING SLO {slo}: no '{col_name}' column on the Marks sheet")
            continue
        target_cols[slo] = header.index(col_name) + 1  # openpyxl 1-indexed

    if not target_cols:
        return False

    name_to_row = {}
    for r in range(2, ws.max_row + 1):
        fn = ws.cell(r, header.index("First Name") + 1).value
        ln = ws.cell(r, header.index("Last Name") + 1).value
        if fn is None and ln is None:
            continue
        name_to_row[f"{(fn or '').strip()} {(ln or '').strip()}".strip().lower()] = r

    changes = []   # (row, name, slo, old, new, pct)
    skipped = []   # (row, name, slo, existing)
    not_completed = []  # (name, status)
    unmatched = []

    for stem, result in by_student.items():
        row_idx = name_to_row.get(stem.strip().lower())
        if row_idx is None:
            unmatched.append(stem)
            continue
        if result[0] == "SKIP":
            not_completed.append((stem, result[1]))
            continue

        per_slo = result[1]
        for slo, col_idx in target_cols.items():
            earned, possible = per_slo[slo]
            pct = earned / possible if possible else 0.0
            new_val = slo_thresholds(pct)
            cell = ws.cell(row_idx, col_idx)
            old_val = cell.value
            if old_val is not None and not force:
                if old_val != new_val:
                    skipped.append((row_idx, stem, slo, old_val))
                continue
            if old_val != new_val:
                changes.append((row_idx, stem, slo, old_val, new_val, pct))
            if not dry_run:
                cell.value = new_val

    print(f"  {len(changes)} cell(s) {'would change' if dry_run else 'changed'}:")
    for r, name, slo, old, new, pct in changes:
        print(f"    row {r:>2}  {name:<28} {slo}-Practice  {old!r:>6} -> {new!r}  ({pct:.0%})")

    if skipped:
        print(f"  {len(skipped)} cell(s) already had a value and were left as-is "
              f"(pass --force to overwrite):")
        for r, name, slo, old in skipped:
            print(f"    row {r:>2}  {name:<28} {slo}-Practice  kept {old!r}")

    if not_completed:
        print(f"  {len(not_completed)} submission(s) did not grade successfully and were left blank "
              f"(needs manual follow-up):")
        for name, status in not_completed:
            print(f"    {name}: {status}")

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
        csv_paths = sorted(glob.glob(os.path.join(script_dir, PRACTICE_CSV_GLOB)))
        if not csv_paths:
            sys.exit(f'No files matching "{PRACTICE_CSV_GLOB}" found in {script_dir}.')
        print(f"No file given on the command line — found {len(csv_paths)} practice report(s):")
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
