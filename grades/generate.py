#!/usr/bin/env python3
"""
Generate per-student JSON grade files from grades.xlsx.

Excel format:
  Marks sheet (first sheet):
    - One header row; one row per student
    - Column "Key" holds the student's Pokémon key
    - Other columns: 02A-Reading, 02A-Quiz, 02A-Practice,
      PRO01–PRO10, Forum 1–Forum 6, etc.  Values: A, P, N, or blank

  Attendance sheet (tab named "Attendance"):
    - Column "Key" in first column
    - Remaining columns: session labels (e.g. "Jan 13", "Jan 15", ...)
    - Values: P (present), N (absent), blank (upcoming)

Output: grade-data/<pokemon>.json  (one file per student)

Usage:
  cd grades/
  python3 generate.py
"""

import json
import os
import sys
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas not found — run: pip install pandas openpyxl")

EXCEL_FILE      = os.path.join(os.path.dirname(__file__), "grades.xlsx")
OUTPUT_DIR      = os.path.join(os.path.dirname(__file__), "grade-data")
KEY_COLUMN           = "Key"
ATTENDANCE_SHEET     = "Attendance"
SKIP_COLS            = {"First Name", "Last Name", "First name", "Last name", "Name", "Email"}

def is_junk_col(name):
    return not name or str(name).startswith("Unnamed:")

def format_date(label):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(str(label).strip(), fmt)
            return dt.strftime("%b") + " " + str(dt.day)
        except ValueError:
            pass
    return str(label)

if not os.path.exists(EXCEL_FILE):
    sys.exit(f"File not found: {EXCEL_FILE}")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Read marks (first sheet) ───────────────────────────────────────────────
df_marks = pd.read_excel(EXCEL_FILE, sheet_name=0, dtype=str).fillna("")

if KEY_COLUMN not in df_marks.columns:
    sys.exit(f"Column '{KEY_COLUMN}' not found in marks sheet. Columns: {list(df_marks.columns)}")

mark_cols = [c for c in df_marks.columns if c != KEY_COLUMN and c not in SKIP_COLS and not is_junk_col(c)]

# ── Read attendance sheet ──────────────────────────────────────────────────
attendance_by_key = {}
try:
    df_att = pd.read_excel(EXCEL_FILE, sheet_name=ATTENDANCE_SHEET, dtype=str).fillna("")
    if KEY_COLUMN not in df_att.columns:
        print(f"Warning: no '{KEY_COLUMN}' column in Attendance sheet — skipping attendance.")
    else:
        session_cols = [c for c in df_att.columns if c != KEY_COLUMN and c not in SKIP_COLS and not is_junk_col(c)]
        for _, row in df_att.iterrows():
            key = str(row[KEY_COLUMN]).strip().lower()
            if not key:
                continue
            sessions = []
            present = absent = 0
            for col in session_cols:
                val = str(row[col]).strip().upper()
                sessions.append({"label": format_date(col), "value": val if val in ("P", "N") else ""})
                if val == "P":
                    present += 1
                elif val == "N":
                    absent += 1
            happened = present + absent
            future   = len(sessions) - happened
            pct      = round(present / happened * 100, 1) if happened > 0 else None
            attendance_by_key[key] = {
                "sessions": sessions,
                "present":  present,
                "absent":   absent,
                "happened": happened,
                "future":   future,
                "total":    len(sessions),
                "pct":      pct,
            }
except Exception as e:
    print(f"Warning: could not read Attendance sheet ({e}) — attendance will be null.")

# ── Generate one JSON file per student ────────────────────────────────────
count = 0
for _, row in df_marks.iterrows():
    key = str(row[KEY_COLUMN]).strip().lower()
    if not key:
        continue

    marks = {}
    for col in mark_cols:
        val = str(row[col]).strip().upper()
        marks[col] = val if val in ("A", "P", "N") else ""

    data = {
        "marks":      marks,
        "attendance": attendance_by_key.get(key, None),
    }

    out_path = os.path.join(OUTPUT_DIR, f"{key}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    count += 1
    att_note = f"  ({data['attendance']['present']}/{data['attendance']['total']} sessions)" if data["attendance"] else ""
    print(f"  {key}.json{att_note}")

print(f"\n{count} files written to {os.path.abspath(OUTPUT_DIR)}")
