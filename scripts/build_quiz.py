"""
Generic engine for building an in-class paper quiz as two printable PDF
versions (A/B) plus a human-readable answer-key markdown file.

Usage:
    python scripts/build_quiz.py <quiz_number>
    e.g. python scripts/build_quiz.py 1

Looks up which week that quiz belongs to from _data/weeks.yml, imports the
matching content module scripts/quiz_content/quizNN.py (NN zero-padded),
and writes into that week's folder:
    weeks/<week>/quizNN.md     -- human-readable source + answer key
                                   (excluded from the Jekyll site, see
                                   _config.yml)
    weeks/<week>/quizNN_A.pdf  -- printable Version A (blank, for students)
    weeks/<week>/quizNN_B.pdf  -- printable Version B (blank, for students)

Requires: pandoc + a LaTeX engine (xelatex) on PATH.

To add a new quiz: create scripts/quiz_content/quizNN.py exposing a
module-level `CONTENT: QuizContent` (see the dataclasses below), then run
this script with that quiz number. Everything in this file is meant to be
reused as-is -- content modules should not need to touch LaTeX directly
except via the helpers here (blank_table, code_box, sketch_box, blank_line).
"""

import argparse
import importlib
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Content contract
# ---------------------------------------------------------------------------

@dataclass
class Question:
    heading: str        # e.g. "Question 1 (SLO 02A)"
    intro_md: str        # markdown/prose shown to students (may include tex_escape'd inline raw latex)
    body_latex: str      # a raw-latex block: the fillable table/code/sketch box (build with the helpers below)
    answer_md: str        # markdown shown in the answer-key .md, with the real answer filled in


@dataclass
class QuizVersion:
    rows: list                  # sample-data rows for this version: list[dict], keyed by QuizContent.sample_columns
    questions: list              # list[Question]


@dataclass
class QuizContent:
    title: str                  # plain text, e.g. "DATA 202 -- Quiz 1"
    subtitle: str                # plain text, e.g. "Week 2 -- DataFrame Basics & Visual Encodings"
    dataset_intro_md: str         # prose describing the dataset (shared across versions)
    sample_columns: list          # ordered column headers for the sample-rows table
    versions: dict                # {"A": QuizVersion, "B": QuizVersion}


# ---------------------------------------------------------------------------
# LaTeX document chrome (reusable across all quizzes)
# ---------------------------------------------------------------------------

PREAMBLE = r"""
\usepackage[margin=1in]{geometry}
\usepackage{array}
\usepackage{fancyhdr}
\usepackage{xcolor}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small %(header_left)s}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\renewcommand{\arraystretch}{1.6}
"""

TOP_HEADER = r"""
\begin{center}
{\LARGE \textbf{%(title)s}}\\[2pt]
{\large %(subtitle)s}
\end{center}

\vspace{6pt}
\noindent Name: \rule{7cm}{0.4pt} \hfill Date: \rule{3cm}{0.4pt}

\vspace{6pt}
\hrule
\vspace{6pt}
"""


# ---------------------------------------------------------------------------
# Escaping / raw-LaTeX helpers
# ---------------------------------------------------------------------------

_TEX_SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_\allowbreak{}",  # allowbreak: long identifier_names have no spaces to wrap at otherwise
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex_escape(s: str) -> str:
    """Escape LaTeX-special characters in a plain string being dropped into
    a raw-LaTeX context. Content modules should pass plain, unescaped text/
    code to the helpers below; escaping happens here, at the point of
    embedding, not when authoring content -- so the same plain strings can
    also be reused verbatim in the plain-markdown answer key."""
    return "".join(_TEX_SPECIAL.get(ch, ch) for ch in str(s))


def raw_latex(body: str) -> str:
    """Wrap a raw LaTeX snippet as a pandoc raw-latex fenced block."""
    return "```{=latex}\n" + body.strip("\n") + "\n```\n"


def blank_line(width: str = "0.6\\linewidth") -> str:
    """A ruled blank for students to write an answer on, sized in LaTeX units."""
    return r"\rule{%s}{0.4pt}" % width


def sketch_box(height: str = "1.9in") -> str:
    """Reserved blank vertical space for a hand-written/sketched answer --
    deliberately unbordered, just white space of the given height."""
    return raw_latex(r"\vspace{%s}" % height)


def code_box(lines) -> str:
    """A bordered monospace box showing a code skeleton. Each item in `lines`
    is a literal LaTeX-ready string (already tex_escape'd/formatted by the
    caller, e.g. mixing plain code with blank_line() calls); items are
    joined with LaTeX line breaks inside the box."""
    body = "\\\\\n".join(lines)
    return raw_latex(
        r"""
\noindent\fbox{\begin{minipage}{0.96\linewidth}\ttfamily\raggedright
%s
\end{minipage}}
"""
        % body
    )


def blank_table(given_cols, blank_cols, rows) -> str:
    """A grid table with some given (filled-in) columns and some blank
    (fill-in-the-blank) columns.

    given_cols: list of (header, width_or_None, monospace) -- width is a
        LaTeX length string (e.g. "8.3cm") or None for a narrow centered
        auto column (good for a row index); monospace renders that column's
        cells in \\ttfamily (use for code/commands).
    blank_cols: list of (header, width) -- empty columns for students to
        fill in.
    rows: list of row-values, one value per given_col, in order.
    """
    col_spec_parts = []
    header_parts = []
    for header, width, mono in given_cols:
        if width is None:
            col_spec_parts.append("c")
        elif mono:
            col_spec_parts.append(r">{\ttfamily\raggedright\arraybackslash}p{%s}" % width)
        else:
            col_spec_parts.append(r">{\raggedright\arraybackslash}p{%s}" % width)
        header_parts.append(tex_escape(header))
    for header, width in blank_cols:
        col_spec_parts.append(r">{\centering\arraybackslash}p{%s}" % width)
        header_parts.append(tex_escape(header))
    col_spec = "|" + "|".join(col_spec_parts) + "|"

    lines = [
        r"\begin{tabular}{%s}" % col_spec,
        r"\hline",
        " & ".join(header_parts) + r" \\",
        r"\hline",
    ]
    for row in rows:
        cells = [tex_escape(val) for val in row]
        cells += [""] * len(blank_cols)
        lines.append(" & ".join(cells) + r" \\")
        lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    return raw_latex("\n".join(lines))


def sample_table(columns, rows, total_width_cm: float = 16.0) -> str:
    """A grid table of sample data rows (no blanks), for the PDF. Raw LaTeX
    with an even, wrapped column width per column (rather than pandoc's
    auto-width plain markdown table), so it can't overflow/overlap
    regardless of how many columns there are or how long their names are
    (e.g. long identifier-style headers like `monthly_support_usd`).
    columns: ordered list of header strings. rows: list of dicts keyed by
    those header strings."""
    n = len(columns)
    tabcolsep_cm = 0.1  # shrunk from LaTeX's default ~0.21cm
    col_width = f"{(total_width_cm - 2 * tabcolsep_cm * n) / n:.2f}cm"
    col_spec = "|" + "|".join(
        [r">{\raggedright\arraybackslash}p{%s}" % col_width] * n
    ) + "|"
    lines = [
        r"{\setlength{\tabcolsep}{%.2fcm}" % tabcolsep_cm,
        r"\begin{tabular}{%s}" % col_spec,
        r"\hline",
    ]
    lines.append(" & ".join(tex_escape(c) for c in columns) + r" \\")
    lines.append(r"\hline")
    for r in rows:
        lines.append(" & ".join(tex_escape(r[c]) for c in columns) + r" \\")
        lines.append(r"\hline")
    lines.append(r"\end{tabular}}")
    return raw_latex("\n".join(lines))


def sample_table_md(columns, rows) -> str:
    """A plain markdown table of sample data rows, for the human-readable
    answer-key .md (not the PDF -- see sample_table for that)."""
    header = "| " + " | ".join(columns) + " |"
    sep = "|" + "|".join(["---"] * len(columns)) + "|"
    lines = [header, sep]
    for r in rows:
        lines.append("| " + " | ".join(str(r[c]) for c in columns) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def build_version_md(content: QuizContent, version_letter: str) -> str:
    version = content.versions[version_letter]
    header_left = "%s --- %s" % (content.title, content.subtitle)
    preamble = PREAMBLE % dict(header_left=tex_escape(header_left))

    yaml_front = (
        "---\n"
        "papersize: letter\n"
        "geometry: margin=1in\n"
        "fontsize: 11pt\n"
        "header-includes:\n"
        "  - |\n"
        + "\n".join("    " + line for line in preamble.strip("\n").splitlines())
        + "\n---\n\n"
    )

    top = raw_latex(
        TOP_HEADER % dict(title=tex_escape(content.title), subtitle=tex_escape(content.subtitle))
    )

    dataset = (
        content.dataset_intro_md
        + "\n\\footnotesize\n\n"
        + sample_table(content.sample_columns, version.rows)
        + "\n\n\\normalsize\n\n"
    )

    body = [dataset]
    for q in version.questions:
        body.append("## %s\n\n%s\n\n%s\n" % (q.heading, q.intro_md, q.body_latex))

    return yaml_front + top + "".join(body)


def render_pdf(md_text: str, out_pdf: Path):
    tmp_md = out_pdf.with_suffix(".tmp.md")
    tmp_md.write_text(md_text, encoding="utf-8")
    try:
        result = subprocess.run(
            ["pandoc", str(tmp_md), "-o", str(out_pdf), "--pdf-engine=xelatex"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"pandoc FAILED for {out_pdf.name}:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)
        print(f"Wrote {out_pdf}")
    finally:
        tmp_md.unlink(missing_ok=True)


def build_readable_md(content: QuizContent, quiz_number: int) -> str:
    lines = [
        f"# {content.title}",
        "",
        content.subtitle,
        "",
        "*(Source content for the printed quiz. Both versions (A/B) are shown",
        f"below. Built via `python scripts/build_quiz.py {quiz_number}`, which",
        f"generates `quiz{quiz_number:02d}_A.pdf` and `quiz{quiz_number:02d}_B.pdf`",
        "for printing. This file is NOT published on the course site -- see",
        "`_config.yml` exclude list.)*",
        "",
        content.dataset_intro_md.strip(),
        "",
    ]
    for letter in ("A", "B"):
        version = content.versions[letter]
        lines += [f"**Version {letter} sample rows:**", "", sample_table_md(content.sample_columns, version.rows), ""]

    # Interleave questions by heading, showing both versions under each.
    n_questions = len(content.versions["A"].questions)
    for i in range(n_questions):
        heading = content.versions["A"].questions[i].heading
        lines += [f"## {heading}", ""]
        for letter in ("A", "B"):
            q = content.versions[letter].questions[i]
            lines += [f"**Version {letter}:**", "", q.answer_md, ""]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Week lookup + CLI
# ---------------------------------------------------------------------------

def week_for_quiz(quiz_number: int) -> int:
    weeks_yml = yaml.safe_load((ROOT / "_data" / "weeks.yml").read_text(encoding="utf-8"))
    for entry in weeks_yml:
        if entry.get("quiz") == quiz_number:
            return entry["week"]
    raise SystemExit(f"No week in _data/weeks.yml has quiz: {quiz_number}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quiz_number", type=int, help="Quiz number, e.g. 1 for quiz01")
    args = parser.parse_args()
    quiz_number = args.quiz_number

    week = week_for_quiz(quiz_number)
    module_name = f"quiz_content.quiz{quiz_number:02d}"
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        content_module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        raise SystemExit(
            f"Could not import scripts/quiz_content/quiz{quiz_number:02d}.py ({e}). "
            "Create it with a module-level CONTENT: QuizContent."
        )
    content: QuizContent = content_module.CONTENT

    out_dir = ROOT / "weeks" / f"{week:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"quiz{quiz_number:02d}"

    for letter in ("A", "B"):
        md = build_version_md(content, letter)
        render_pdf(md, out_dir / f"{stem}_{letter}.pdf")

    (out_dir / f"{stem}.md").write_text(build_readable_md(content, quiz_number), encoding="utf-8")
    print(f"Wrote {out_dir / (stem + '.md')}")


if __name__ == "__main__":
    main()
