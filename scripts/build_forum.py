"""
build_forum.py — Convert a forumN.md discussion-questions page into a
                  printable worksheet PDF: a group-names blank, the chapter's
                  argument summary for context, and a bordered blank writing
                  space under each discussion question.

Usage:
    python scripts/build_forum.py <forum_number>
    e.g. python scripts/build_forum.py 1

Looks up which week that forum belongs to from _data/weeks.yml (the
`forum:` key), reads weeks/<week>/forum<N>.md, and writes
weeks/<week>/forum<N>_worksheet.pdf next to it.

Parsing assumptions about forumN.md (matches the current forum pages):
  - An italic "*Week N — Topic*" line right under the H1 title.
  - A "## Reading" section whose prose paragraphs (after the
    "Read **Chapter X: ..."** instruction line) are the chapter's argument
    summary, reused verbatim on the printed sheet.
  - A "## Discussion Questions" section holding a numbered list, ONE
    QUESTION PER LINE (no wrapped multi-line items).
If a future forum page's questions wrap across lines, extend
parse_forum_md() rather than hand-editing its output.

Requires: pandoc + a LaTeX engine (xelatex) on PATH, same as build_quiz.py.
Reuses build_quiz.py's LaTeX chrome/helpers rather than redefining them.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_quiz import PREAMBLE, raw_latex, render_pdf, sketch_box, tex_escape

ROOT = Path(__file__).resolve().parent.parent

GROUP_HEADER = r"""
\begin{center}
{\LARGE \textbf{%(title)s}}\\[2pt]
{\large %(subtitle)s}
\end{center}

\vspace{6pt}
\noindent\textbf{Group members} (all three names): \\[6pt]
\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}l l l}
1.\ \rule{4.4cm}{0.4pt} & 2.\ \rule{4.4cm}{0.4pt} & 3.\ \rule{4.4cm}{0.4pt}
\end{tabular*}

\vspace{8pt}
\hrule
\vspace{6pt}
"""


def week_for_forum(forum_number: int) -> int:
    weeks_yml = yaml.safe_load((ROOT / "_data" / "weeks.yml").read_text(encoding="utf-8"))
    for entry in weeks_yml:
        if entry.get("forum") == forum_number:
            return entry["week"]
    raise SystemExit(f"No week in _data/weeks.yml has forum: {forum_number}")


def parse_forum_md(path: Path):
    """Pull the topic line, reading argument-summary paragraphs, the
    discussion-time hint, and the numbered discussion questions out of a
    forumN.md file."""
    text = path.read_text(encoding="utf-8")

    topic_match = re.search(r"^\*(.+?)\*\s*$", text, re.MULTILINE)
    topic = topic_match.group(1).strip() if topic_match else ""

    reading_match = re.search(r"^## Reading\s*\n(.*?)\n##", text, re.DOTALL | re.MULTILINE)
    reading_body = reading_match.group(1).strip() if reading_match else ""
    reading_paras = [p.strip() for p in reading_body.split("\n\n") if p.strip()]
    # Drop the "Read **Chapter X..." instruction line -- the chapter/title
    # already appear in the printed header; keep the argument summary itself.
    reading_paras = [p for p in reading_paras if not p.startswith("Read **Chapter")]

    dq_heading_match = re.search(r"^## Discussion Questions\s*(\(.*?\))?", text, re.MULTILINE)
    time_hint = dq_heading_match.group(1) if dq_heading_match and dq_heading_match.group(1) else ""

    dq_match = re.search(
        r"^## Discussion Questions.*?\n(.*?)(?:\n##|\Z)", text, re.DOTALL | re.MULTILINE
    )
    dq_body = dq_match.group(1) if dq_match else ""
    questions = []
    for line in dq_body.splitlines():
        m = re.match(r"^\d+\.\s+(.*\S)\s*$", line)
        if m:
            questions.append(m.group(1))

    return topic, reading_paras, time_hint, questions


def build_worksheet_md(forum_number: int, week: int) -> str:
    weeks_yml = yaml.safe_load((ROOT / "_data" / "weeks.yml").read_text(encoding="utf-8"))
    entry = next(e for e in weeks_yml if e.get("forum") == forum_number)
    chapter_num = entry.get("book_chapter")
    chapter_title = entry.get("book_chapter_title", "")

    forum_path = ROOT / "weeks" / f"{week:02d}" / f"forum{forum_number}.md"
    topic, reading_paras, time_hint, questions = parse_forum_md(forum_path)
    if not questions:
        raise SystemExit(f"No discussion questions found in {forum_path}")

    title = f"DATA 202 --- Forum {forum_number}"
    subtitle = f'Ch. {chapter_num} --- "{chapter_title}"' if chapter_num else topic

    header_left = f"{title} --- {subtitle}"
    preamble = PREAMBLE % dict(header_left=tex_escape(header_left))
    yaml_front = (
        "---\n"
        "papersize: letter\n"
        "fontsize: 11pt\n"
        "header-includes:\n"
        "  - |\n"
        + "\n".join("    " + line for line in preamble.strip("\n").splitlines())
        + "\n---\n\n"
    )

    top = raw_latex(GROUP_HEADER % dict(title=tex_escape(title), subtitle=tex_escape(subtitle)))

    intro_parts = []
    if topic:
        intro_parts.append(f"*{topic}*")
    intro_parts += reading_paras
    if time_hint:
        intro_parts.append(f"*Discuss and write a response to each question below {time_hint}.*")
    intro = "\n\n".join(intro_parts) + "\n\n"

    body_parts = [top, intro]
    box_height = "1.8in"
    for i, q in enumerate(questions, start=1):
        # Wrap question text + its blank answer space in one unbreakable
        # minipage: a minipage can't be split across a page break, so if it
        # doesn't fit in what's left of the current page, LaTeX pushes the
        # *whole* thing (text and space together) to the next page instead
        # of stranding the question at the bottom with its space cut off.
        body_parts.append(raw_latex(r"\noindent\begin{minipage}{\linewidth}"))
        body_parts.append(f"**{i}.** {q}\n\n")
        body_parts.append(sketch_box(box_height))
        body_parts.append(raw_latex(r"\end{minipage}"))
        body_parts.append("\n\n")

    return yaml_front + "".join(body_parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("forum_number", type=int, help="Forum number, e.g. 1 for forum1")
    args = parser.parse_args()

    week = week_for_forum(args.forum_number)
    md = build_worksheet_md(args.forum_number, week)

    out_dir = ROOT / "weeks" / f"{week:02d}"
    out_pdf = out_dir / f"forum{args.forum_number}_worksheet.pdf"
    render_pdf(md, out_pdf)


if __name__ == "__main__":
    main()
