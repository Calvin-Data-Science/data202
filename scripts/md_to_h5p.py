#!/usr/bin/env python3
"""
md_to_h5p.py — Convert a markdown reading file (text + questions) to a single
               H5P.InteractiveBook package that can be imported into Moodle or
               any H5P-enabled LMS.

Usage:
    python scripts/md_to_h5p.py weeks/01/reading.md [--out weeks/01/reading.h5p]

Page structure
--------------
Each H1 heading (# Title) starts a new page (chapter) in the InteractiveBook.
All content between two H1 headings belongs to that page.
If there is only one H1 (or none), the output has a single page.

Within each page, --- lines become native H5P separators between cells.

Question block syntax
---------------------

MULTIPLE CHOICE
    <!-- QUESTION:multiple-choice -->
    **Question text**
    - [x] Correct answer
    - [ ] Wrong answer
    <!-- END QUESTION -->

FILL IN THE BLANK  (gaps marked as **[answer]**)
    <!-- QUESTION:fill-in-the-blank -->
    Sentence with a **[answer]** gap and another **[word]** gap.
    <!-- END QUESTION -->

TRUE / FALSE  (answer: true | false in the comment header)
    <!-- QUESTION:true-false
    answer: false
    -->
    Statement text.
    <!-- END QUESTION -->

DRAG THE WORDS  (draggable words marked as *[word]*)
    <!-- QUESTION:drag-the-words -->
    Text with a *[word]* slot and another *[term]* slot.
    <!-- END QUESTION -->

SORT THE PARAGRAPHS  (numbered list = correct order)
    <!-- QUESTION:sort-paragraphs -->
    1. First step
    2. Second step
    <!-- END QUESTION -->

Library versions (must match your H5P server installation):
    H5P.InteractiveBook  1.7
    H5P.AdvancedText     1.1
    H5P.MultiChoice      1.16
    H5P.TrueFalse        1.8
    H5P.Blanks           1.14
    H5P.DragText         1.10
    H5P.SortParagraphs   0.11
"""

import argparse
import io
import json
import re
import sys
import urllib.request
import uuid
import zipfile
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Optional markdown library — used for text→HTML; falls back to basic regex
# ---------------------------------------------------------------------------
try:
    import markdown as _markdown_lib

    def md_to_html(text: str) -> str:
        return _markdown_lib.markdown(
            text,
            extensions=["tables", "fenced_code"],
        )

except ImportError:
    _markdown_lib = None

    def md_to_html(text: str) -> str:  # type: ignore[misc]
        """Minimal markdown → HTML without external dependencies."""
        lines = text.splitlines()
        html_lines = []
        in_ul = False
        for line in lines:
            # Headings
            m = re.match(r"^(#{1,4})\s+(.+)$", line)
            if m:
                if in_ul:
                    html_lines.append("</ul>")
                    in_ul = False
                level = len(m.group(1))
                html_lines.append(f"<h{level}>{_inline(m.group(2))}</h{level}>")
                continue
            # Horizontal rule
            if re.match(r"^-{3,}$", line.strip()):
                if in_ul:
                    html_lines.append("</ul>")
                    in_ul = False
                html_lines.append("<hr>")
                continue
            # Unordered list item (not a checkbox)
            if re.match(r"^[-*]\s+(?!\[)", line.strip()):
                if not in_ul:
                    html_lines.append("<ul>")
                    in_ul = True
                content = re.sub(r"^[-*]\s+", "", line.strip())
                html_lines.append(f"<li>{_inline(content)}</li>")
                continue
            # Blank line
            if not line.strip():
                if in_ul:
                    html_lines.append("</ul>")
                    in_ul = False
                html_lines.append("")
                continue
            # Blockquote
            if line.startswith("> "):
                if in_ul:
                    html_lines.append("</ul>")
                    in_ul = False
                html_lines.append(f"<blockquote><p>{_inline(line[2:])}</p></blockquote>")
                continue
            # Plain paragraph
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<p>{_inline(line)}</p>")

        if in_ul:
            html_lines.append("</ul>")
        return "\n".join(html_lines)


def _inline(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


EXT_IMG   = re.compile(r'<img([^>]*?)\bsrc="(https?://[^"]+)"([^>]*?/?)>',                  re.DOTALL)
LOCAL_IMG = re.compile(r'<img([^>]*?)\bsrc="(?!https?://)(?!data:)([^"]+)"([^>]*?/?)>', re.DOTALL)
IMG_TAG   = re.compile(r'<img([^>]*)/?>', re.DOTALL)

MIME_TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
    "gif": "image/gif",  "webp": "image/webp", "bmp": "image/bmp",
    "tif": "image/tiff", "tiff": "image/tiff",
}


def _pad_to_canvas_width(dest: Path, canvas_w_px: int) -> None:
    """Center image on a wider white canvas, overwriting dest in place."""
    try:
        import io as _io
        from PIL import Image as _PILImg
        with _PILImg.open(dest) as img:
            w, h = img.size
            if w >= canvas_w_px:
                return
            canvas = _PILImg.new("RGB", (canvas_w_px, h), (255, 255, 255))
            canvas.paste(img.convert("RGB"), ((canvas_w_px - w) // 2, 0))
            buf = _io.BytesIO()
            canvas.save(buf, format="PNG", optimize=True)
        dest.write_bytes(buf.getvalue())
    except Exception:
        pass


def _render_table_png(
    headers: list[str], rows: list[list[str]], dest: Path, content_w_px: int | None = None
) -> None:
    """Render a data table as a styled PNG using matplotlib.

    content_w_px: pixel width of the table content (default 780 = full Moodle column).
    If narrower than 780, the saved image is padded to 780px so H5P scales it to the
    right apparent size when it stretches all images to 100% container width.
    """
    import textwrap
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    dest.parent.mkdir(parents=True, exist_ok=True)

    CANVAS_W_PX = 780   # H5P container display width (CSS px)
    BASE_DPI    = 120   # reference DPI for display-size calculations
    RENDER_DPI  = 288   # physical render DPI; browser scales image down → sharp text
    if content_w_px is None:
        content_w_px = CANVAS_W_PX
    content_w_px = min(content_w_px, CANVAS_W_PX)

    ncols = max(len(headers), *(len(r) for r in rows)) if rows else max(len(headers), 1)
    nrows = len(rows)

    # Figure size in inches is fixed by display size; RENDER_DPI controls sharpness only.
    # Apparent CSS font size = FONTSIZE × (RENDER_DPI/72) × (780 / canvas_render_px)
    #                        = FONTSIZE × (BASE_DPI/72) ≈ 8 × 1.67 = 13.3 px ✓
    TARGET_W_IN = content_w_px / BASE_DPI
    FONTSIZE    = 8     # pt
    w_ratio     = content_w_px / CANVAS_W_PX
    WRAP        = max(12, int(52 * w_ratio / ncols))   # chars per cell

    def _wrap(text: str) -> str:
        return "\n".join(textwrap.wrap(text, WRAP)) if text else ""

    hdrs = [_wrap(h) for h in list(headers) + [""] * (ncols - len(headers))]
    data = [[_wrap(c) for c in list(r) + [""] * (ncols - len(r))] for r in rows]

    all_rows    = [hdrs] + data
    row_lines   = [max((c.count("\n") + 1 for c in r), default=1) for r in all_rows]
    total_lines = sum(row_lines)

    LINE_H = 0.20       # inches per text line
    fig_w  = TARGET_W_IN
    fig_h  = max(0.4, total_lines * LINE_H + 0.10)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")

    tbl = ax.table(
        cellText=data,
        colLabels=hdrs or None,
        loc="center",
        cellLoc="left",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(FONTSIZE)
    tbl.auto_set_column_width(list(range(ncols)))

    for i, n_lines in enumerate(row_lines):
        h = n_lines / total_lines
        for j in range(ncols):
            tbl[i, j].set_height(h)

    for j in range(ncols):
        cell = tbl[0, j]
        cell.set_facecolor("#0b5e73")
        cell.set_text_props(color="white", fontweight="bold")
        cell.set_edgecolor("#ffffff")

    for i in range(1, nrows + 1):
        for j in range(ncols):
            cell = tbl[i, j]
            cell.set_facecolor("#f0f7f9" if i % 2 == 1 else "#ffffff")
            cell.set_edgecolor("#cccccc")

    fig.savefig(str(dest), dpi=RENDER_DPI, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)

    # Pad to full canvas width if content is narrower. Canvas width scales with RENDER_DPI
    # so the padded image and the content image have the same pixel density.
    canvas_render_px = round(CANVAS_W_PX * RENDER_DPI / BASE_DPI)
    if content_w_px < CANVAS_W_PX:
        _pad_to_canvas_width(dest, canvas_render_px)


def _tables_to_images(html: str, source_dir: Path, counter: list[int]) -> str:
    """Convert HTML tables to PNG images; respects <!-- width: N --> hints before tables."""
    TABLE_RE = re.compile(r"<table[^>]*>.*?</table>", re.DOTALL | re.IGNORECASE)
    ROW_RE   = re.compile(r"<tr[^>]*>(.*?)</tr>",     re.DOTALL | re.IGNORECASE)
    CELL_RE  = re.compile(r"<t[hd][^>]*>(.*?)</t[hd]>", re.DOTALL | re.IGNORECASE)
    TAG_RE   = re.compile(r"<[^>]+>")
    WIDTH_RE = re.compile(r"<!--\s*width:\s*(\d+)\s*-->\s*$")

    def _text(s: str) -> str:
        return TAG_RE.sub("", s).strip()

    def _parse_table(table_html: str):
        row_matches = list(ROW_RE.finditer(table_html))
        if not row_matches:
            return None, None
        first = row_matches[0]
        if re.search(r"<th", first.group(1), re.I):
            headers   = [_text(c.group(1)) for c in CELL_RE.finditer(first.group(1))]
            data_rows = [[_text(c.group(1)) for c in CELL_RE.finditer(r.group(1))]
                         for r in row_matches[1:]]
        else:
            headers   = []
            data_rows = [[_text(c.group(1)) for c in CELL_RE.finditer(r.group(1))]
                         for r in row_matches]
        return headers, data_rows

    result = []
    pos = 0
    for m in TABLE_RE.finditer(html):
        before = html[pos:m.start()]
        # Detect <!-- width: N --> immediately before this table
        content_w_px = None
        wm = WIDTH_RE.search(before)
        if wm:
            content_w_px = int(wm.group(1))
            before = before[:wm.start()]
        result.append(before)

        headers, data_rows = _parse_table(m.group(0))
        if headers is None:
            result.append(m.group(0))
            pos = m.end()
            continue

        counter[0] += 1
        img_name = f"table_{counter[0]:03d}.png"
        img_path = source_dir / "images" / img_name

        try:
            _render_table_png(headers, data_rows, img_path, content_w_px=content_w_px)
            alt = "Table: " + " | ".join(headers) if headers else "Table"
            result.append(f'<img src="images/{img_name}" alt="{alt}">')
        except Exception as exc:
            print(f"WARNING: Could not render table as image: {exc}", file=sys.stderr)
            parts = ["<hr>"]
            if headers:
                parts.append("<p><strong>" + " | ".join(headers) + "</strong></p>")
                parts.append("<hr>")
            for row in data_rows:
                parts.append("<p>" + " | ".join(row) + "</p>")
            parts.append("<hr>")
            result.append("\n".join(parts))

        pos = m.end()

    result.append(html[pos:])
    return "".join(result)


def _fix_blockquotes(html: str) -> str:
    """Convert blockquotes to <hr> + italic text with Unicode quote marks.
    H5P strips both style= and blockquote default indent, so we need character-based fallback."""
    def _convert(m: re.Match) -> str:
        inner = m.group(1).strip()
        inner = re.sub(r"</?p[^>]*>", "", inner).strip()
        return f"<hr>\n<p><em>&#10077; {inner} &#10078;</em></p>\n<hr>"
    return re.sub(r"<blockquote[^>]*>(.*?)</blockquote>", _convert, html, flags=re.DOTALL | re.IGNORECASE)



def _split_html_at_images(html: str) -> list[dict]:
    """Split HTML at <img> tags into alternating text/image chunks."""
    parts: list[dict] = []
    pos = 0
    for m in IMG_TAG.finditer(html):
        before = html[pos : m.start()].strip()
        if before:
            parts.append({"type": "text", "html": before})
        attrs = m.group(1)
        src_m = re.search(r'src="([^"]+)"', attrs)
        alt_m = re.search(r'alt="([^"]*)"', attrs)
        if src_m:
            parts.append({"type": "image", "src": src_m.group(1), "alt": alt_m.group(1) if alt_m else ""})
        pos = m.end()
    tail = html[pos:].strip()
    if tail:
        parts.append({"type": "text", "html": tail})
    return parts or [{"type": "text", "html": html}]


def _postprocess_html(html: str, source_dir: Path = None, table_counter: list = None) -> str:
    # Unwrap <p><img ...></p> so the image splits cleanly without orphaned tags
    html = re.sub(r"<p>\s*(<img[^>]*?/?>\s*)</p>", r"\1", html, flags=re.DOTALL | re.IGNORECASE)
    if source_dir is not None:
        html = _tables_to_images(html, source_dir, table_counter if table_counter is not None else [0])
    html = _fix_blockquotes(html)
    return html


# ---------------------------------------------------------------------------
# Document segmenter — splits markdown into ordered text / question segments
# ---------------------------------------------------------------------------

QUESTION_START = re.compile(
    r"<!--\s*QUESTION:(?P<qtype>[\w-]+)(?P<attrs>[^>]*?)-->",
    re.DOTALL,
)
QUESTION_END = re.compile(r"<!--\s*END QUESTION\s*-->")
FRONTMATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def strip_frontmatter(text: str) -> str:
    m = FRONTMATTER.match(text)
    return text[m.end():] if m else text


def parse_attrs(raw: str) -> dict[str, str]:
    attrs = {}
    for line in raw.strip().splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            attrs[key.strip()] = val.strip()
    return attrs


def extract_title(md_text: str) -> str:
    """
    Return the title for the H5P package.
    Priority: YAML frontmatter 'title:' field → first H1 heading → fallback.
    """
    fm = FRONTMATTER.match(md_text)
    if fm:
        title_m = re.search(
            r'^title:\s*["\']?(.+?)["\']?\s*$', fm.group(0), re.MULTILINE
        )
        if title_m:
            return title_m.group(1).strip()
    h1 = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    return h1.group(1).strip() if h1 else "Reading"


H1_PATTERN  = re.compile(r"^#\s+(.+)$", re.MULTILINE)
HR_LINE     = re.compile(r"^[ \t]*-{3,}[ \t]*$", re.MULTILINE)
FENCED_CODE = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.MULTILINE | re.DOTALL)


def _mask_code_blocks(text: str) -> str:
    """Replace fenced code block content with spaces/newlines, preserving character positions."""
    def _blank(m: re.Match) -> str:
        return ''.join('\n' if c == '\n' else ' ' for c in m.group(0))
    return FENCED_CODE.sub(_blank, text)


def split_into_chapters(md_text: str) -> list[dict]:
    """
    Split the document at H1 headings. Each H1 becomes one page (chapter).
    Returns a list of {"title": str, "body": str}.
    If there are no H1 headings the whole document is treated as one chapter.
    H1 detection ignores lines inside fenced code blocks.
    """
    md_text = strip_frontmatter(md_text)
    # Find H1 headings only in non-code regions
    masked  = _mask_code_blocks(md_text)
    matches = list(H1_PATTERN.finditer(masked))

    if not matches:
        return [{"title": "Content", "body": md_text.strip()}]

    chapters = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        body = md_text[body_start:body_end].strip()
        chapters.append({"title": title, "body": body})
    return chapters


def _split_text_on_hr(text: str) -> list[dict]:
    """
    Split a text block at standalone '---' lines.
    Returns alternating {"kind": "text"} and {"kind": "separator"} dicts.
    """
    parts = HR_LINE.split(text)
    result = []
    for i, part in enumerate(parts):
        if part.strip():
            result.append({"kind": "text", "body": part.strip()})
        if i < len(parts) - 1:
            result.append({"kind": "separator"})
    return result


def parse_chapter_body(body: str, q_start: int = 0) -> tuple[list[dict], int]:
    """
    Parse one chapter's markdown body into an ordered segment list:
      {"kind": "text",      "body": str}
      {"kind": "separator"}
      {"kind": "question",  "type", "attrs", "body", "index"}

    Returns (segments, next_q_index) so callers can maintain a global question
    counter across chapters.
    """
    segments = []
    pos = 0
    q_index = q_start

    while pos < len(body):
        m_start = QUESTION_START.search(body, pos)
        if not m_start:
            tail = body[pos:].strip()
            if tail:
                segments.extend(_split_text_on_hr(tail))
            break

        text_before = body[pos : m_start.start()].strip()
        if text_before:
            segments.extend(_split_text_on_hr(text_before))

        qtype = m_start.group("qtype").lower()
        attrs = parse_attrs(m_start.group("attrs"))

        m_end = QUESTION_END.search(body, m_start.end())
        if not m_end:
            print(
                f"WARNING: QUESTION:{qtype} has no END QUESTION marker -- skipped.",
                file=sys.stderr,
            )
            pos = m_start.end()
            continue

        qbody = body[m_start.end() : m_end.start()].strip()
        q_index += 1
        segments.append(
            {"kind": "question", "type": qtype, "attrs": attrs, "body": qbody, "index": q_index}
        )
        pos = m_end.end()

    return segments, q_index


# ---------------------------------------------------------------------------
# Question body parsers
# ---------------------------------------------------------------------------


def parse_multiple_choice(body: str) -> dict[str, Any]:
    question_lines, answers = [], []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("- ["):
            correct = s.startswith("- [x]") or s.startswith("- [X]")
            text = re.sub(r"^-\s*\[[xX ]\]\s*", "", s)
            answers.append({"text": text, "correct": correct})
        else:
            question_lines.append(line)
    question = re.sub(r"\*\*(.+?)\*\*", r"\1", "\n".join(question_lines).strip())
    return {"question": question, "answers": answers}


def parse_fill_in_the_blank(body: str) -> dict[str, Any]:
    # Strip the optional intro line (no gaps) to keep only the gapped text
    lines = body.splitlines()
    gapped = [l for l in lines if "**[" in l]
    text = "\n".join(gapped).strip() if gapped else body.strip()
    h5p_text = re.sub(r"\*\*\[(.+?)\]\*\*", r"*\1*", text)
    # Pass the intro line as task description
    intro_lines = [l for l in lines if "**[" not in l and l.strip()]
    task_desc = intro_lines[0].strip() if intro_lines else "Fill in the blanks."
    return {"taskDescription": task_desc, "text": h5p_text}


def parse_true_false(body: str, attrs: dict) -> dict[str, Any]:
    answer = attrs.get("answer", "true").strip().lower()
    if answer not in ("true", "false"):
        answer = "true"
    return {"question": body.strip(), "correct": answer}


def parse_drag_the_words(body: str) -> dict[str, Any]:
    lines = body.splitlines()
    gapped = [l for l in lines if "*[" in l]
    text = "\n".join(gapped).strip() if gapped else body.strip()
    h5p_text = re.sub(r"\*\[(.+?)\]\*", r"*\1*", text)
    intro_lines = [l for l in lines if "*[" not in l and l.strip()]
    task_desc = intro_lines[0].strip() if intro_lines else "Drag the correct word into each gap."
    return {"taskDescription": task_desc, "textField": h5p_text}


def parse_sort_paragraphs(body: str) -> dict[str, Any]:
    paragraphs = []
    for line in body.splitlines():
        m = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if m:
            paragraphs.append(m.group(1).strip())
    return {"paragraphs": paragraphs}


BODY_PARSERS = {
    "multiple-choice":   lambda body, attrs: parse_multiple_choice(body),
    "fill-in-the-blank": lambda body, attrs: parse_fill_in_the_blank(body),
    "true-false":        parse_true_false,
    "drag-the-words":    lambda body, attrs: parse_drag_the_words(body),
    "sort-paragraphs":   lambda body, attrs: parse_sort_paragraphs(body),
}

# ---------------------------------------------------------------------------
# H5P content.json builders (params for each question widget)
# ---------------------------------------------------------------------------

BEHAVIOUR_BASE = {
    "enableRetry": True,
    "enableSolutionsButton": True,
    "enableCheckButton": True,
}


def build_multiple_choice_params(p: dict) -> dict:
    return {
        "question": f"<p>{p['question']}</p>",
        "answers": [
            {
                "text": f"<div>{a['text']}</div>",
                "correct": a["correct"],
                "tipsAndFeedback": {"tip": "", "chosenFeedback": "", "notChosenFeedback": ""},
            }
            for a in p["answers"]
        ],
        "behaviour": {
            **BEHAVIOUR_BASE,
            "type": "auto",
            "singlePoint": False,
            "randomAnswers": False,
            "showSolutionsRequiresInput": True,
            "autoCheck": False,
            "passPercentage": 100,
        },
        "UI": {
            "checkAnswerButton": "Check",
            "submitAnswerButton": "Submit",
            "showSolutionButton": "Show solution",
            "tryAgainButton": "Retry",
            "tipsLabel": "Show tip",
            "scoreBarLabel": "You got :num out of :total points",
        },
    }


def build_true_false_params(p: dict) -> dict:
    return {
        "question": f"<p>{p['question']}</p>",
        "correct": p["correct"],
        "behaviour": {
            **BEHAVIOUR_BASE,
            "autoCheck": False,
            "confirmCheckDialog": False,
            "confirmRetryDialog": False,
        },
        "l10n": {
            "trueText": "True",
            "falseText": "False",
            "score": "You got @score of @total points",
            "checkAnswer": "Check",
            "showSolutionButton": "Show solution",
            "tryAgain": "Retry",
        },
    }


def build_fill_in_the_blank_params(p: dict) -> dict:
    return {
        "taskDescription": f"<p>{p['taskDescription']}</p>",
        "questions": [f"<p>{p['text']}</p>"],
        "behaviour": {
            **BEHAVIOUR_BASE,
            "autoCheck": False,
            "caseSensitive": False,
            "showSolutionsRequiresInput": True,
            "separateLines": False,
        },
        "UI": {
            "checkAnswerButton": "Check",
            "submitAnswerButton": "Submit",
            "showSolutionButton": "Show solution",
            "tryAgainButton": "Retry",
            "scoreBarLabel": "You got :num out of :total points",
        },
    }


def build_drag_the_words_params(p: dict) -> dict:
    return {
        "taskDescription": f"<p>{p['taskDescription']}</p>",
        "textField": p["textField"],
        "behaviour": {
            **BEHAVIOUR_BASE,
            "enableFullScreen": False,
            "showScorePoints": True,
            "instantFeedback": False,
        },
        "l10n": {
            "checkAnswer": "Check",
            "submitAnswer": "Submit",
            "tryAgain": "Retry",
            "showSolution": "Show solution",
            "scoreBarLabel": "You got :num out of :total points",
        },
    }


def build_sort_paragraphs_params(p: dict) -> dict:
    return {
        "description": "<p>Arrange the steps in the correct order.</p>",
        "paragraphs": [{"text": f"<p>{item}</p>"} for item in p["paragraphs"]],
        "behaviour": {**BEHAVIOUR_BASE, "enableFullScreen": False},
        "l10n": {
            "checkAnswer": "Check",
            "tryAgain": "Retry",
            "showSolution": "Show solution",
            "scoreBarLabel": "You got :num out of :total points",
        },
    }


PARAM_BUILDERS = {
    "multiple-choice":   build_multiple_choice_params,
    "fill-in-the-blank": build_fill_in_the_blank_params,
    "true-false":        build_true_false_params,
    "drag-the-words":    build_drag_the_words_params,
    "sort-paragraphs":   build_sort_paragraphs_params,
}

# ---------------------------------------------------------------------------
# Library registry
# ---------------------------------------------------------------------------

LIBRARIES = {
    "interactive-book":  ("H5P.InteractiveBook", 1,  7),
    "column":            ("H5P.Column",           1, 16),
    "text":              ("H5P.AdvancedText",     1,  1),
    "image":             ("H5P.Image",            1,  1),
    "multiple-choice":   ("H5P.MultiChoice",      1, 16),
    "true-false":        ("H5P.TrueFalse",        1,  8),
    "fill-in-the-blank": ("H5P.Blanks",           1, 14),
    "drag-the-words":    ("H5P.DragText",         1, 10),
}

CONTENT_TYPES = {
    "multiple-choice":   "Multiple Choice",
    "fill-in-the-blank": "Fill in the Blanks",
    "true-false":        "True/False Question",
    "drag-the-words":    "Drag the Words",
    "sort-paragraphs":   "Sort the Paragraphs",
    "text":              "Text",
    "image":             "Image",
}


def lib_entry(key: str) -> dict:
    name, major, minor = LIBRARIES[key]
    return {"machineName": name, "majorVersion": major, "minorVersion": minor}


def lib_string(key: str) -> str:
    name, major, minor = LIBRARIES[key]
    return f"{name} {major}.{minor}"


def new_id() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Content item builder (shared by all chapter/page types)
# ---------------------------------------------------------------------------


def build_content_item(library_key: str, params: dict, title: str, use_separator: str = "auto") -> dict:
    return {
        "content": {
            "library": lib_string(library_key),
            "params": params,
            "subContentId": new_id(),
            "metadata": {
                "contentType": CONTENT_TYPES.get(library_key, "Content"),
                "license": "U",
                "title": title,
            },
        },
        "useSeparator": use_separator,
    }



def build_image_item(src: str, alt: str, use_separator: str = "auto") -> dict:
    """Create an H5P.Image Column item. src is the original (pre-bundle) local path."""
    ext  = src.rsplit(".", 1)[-1].lower() if "." in src else "png"
    mime = MIME_TYPES.get(ext, "image/png")
    return {
        "content": {
            "library": lib_string("image"),
            "params": {
                "file": {"path": src, "mime": mime, "copyright": {"license": "U"}},
                "decorative": False,
                "alt": alt,
                "title": alt[:60] if alt else "Image",
            },
            "subContentId": new_id(),
            "metadata": {"contentType": "Image", "license": "U", "title": alt[:60] if alt else "Image"},
        },
        "useSeparator": use_separator,
    }


def build_chapter_items(segments: list[dict], source_dir: Path = None, table_counter: list = None) -> tuple[list[dict], set[str]]:
    """
    Convert a flat segment list into H5P content items for one chapter/page.
    '---' separator segments become useSeparator='enabled' on the next item.
    Returns (items_list, used_library_keys).
    """
    items: list[dict] = []
    used_libs: set[str] = {"text"}
    pending_separator = False
    text_block_num = 0

    for seg in segments:
        if seg["kind"] == "separator":
            pending_separator = True
            continue

        use_sep = "enabled" if pending_separator else "auto"
        pending_separator = False

        if seg["kind"] == "text":
            html = _postprocess_html(md_to_html(seg["body"]), source_dir, table_counter)
            sub_parts = _split_html_at_images(html)
            first = True
            for part in sub_parts:
                cur_sep = use_sep if first else "auto"
                first = False
                if part["type"] == "image":
                    items.append(build_image_item(part["src"], part["alt"], cur_sep))
                    used_libs.add("image")
                else:
                    text_block_num += 1
                    items.append(
                        build_content_item("text", {"text": part["html"]}, f"Text {text_block_num}", cur_sep)
                    )

        elif seg["kind"] == "question":
            qtype = seg["type"]
            if qtype not in BODY_PARSERS:
                print(
                    f"WARNING: Unknown question type '{qtype}' at Q{seg['index']} -- skipped.",
                    file=sys.stderr,
                )
                continue
            parsed = BODY_PARSERS[qtype](seg["body"], seg["attrs"])
            params = PARAM_BUILDERS[qtype](parsed)
            title = f"Q{seg['index']}: {CONTENT_TYPES.get(qtype, qtype)}"
            items.append(build_content_item(qtype, params, title, use_sep))
            used_libs.add(qtype)

    return items, used_libs


# ---------------------------------------------------------------------------
# H5P.InteractiveBook content builder
# ---------------------------------------------------------------------------


def build_interactive_book_content(
    chapters: list[dict],
    source_dir: Path = None,
) -> tuple[dict, set[str]]:
    """
    Build the H5P.InteractiveBook content.json from a list of chapter dicts.
    Each chapter dict: {"title": str, "segments": list[dict]}.
    Returns (content_dict, used_library_keys).
    """
    book_chapters = []
    all_used_libs: set[str] = {"interactive-book", "column", "text"}
    table_counter: list[int] = [0]

    for ch in chapters:
        items, used_libs = build_chapter_items(ch["segments"], source_dir, table_counter)
        all_used_libs |= used_libs

        # Prepend the chapter title as a visible H1 — InteractiveBook shows the title
        # only in the nav/TOC in some versions, not on the page itself.
        title_item = build_content_item(
            "text", {"text": f"<h1>{ch['title']}</h1>"}, "Chapter Title"
        )
        items = [title_item] + items

        book_chapters.append(
            {
                "library": lib_string("column"),
                "params": {"content": items},
                "subContentId": new_id(),
                "metadata": {
                    "contentType": "Column",
                    "license": "U",
                    "title": ch["title"],
                },
            }
        )

    content = {
        "chapters": book_chapters,
        "behaviour": {
            "defaultTableOfContents": True,
            "progressAuto": True,
            "displaySummary": False,
        },
        "l10n": {
            "read": "Read",
            "displayTOC": "Display 'Table of contents'",
            "hideTOC": "Hide 'Table of contents'",
            "nextPage": "Next page",
            "previousPage": "Previous page",
            "navigateToTop": "Navigate to the top",
            "fullscreen": "Fullscreen",
            "exitFullscreen": "Exit fullscreen",
            "bookProgressSubtext": ":num of :total pages",
            "summaryHeader": "Finished!",
            "allInteractions": "All interactions",
            "unansweredInteractions": "Unanswered interactions",
            "scoreText": "Your book score:",
            "close": "Close",
            "hideSummary": "Hide book summary",
            "shareResults": "Share results",
            "shareScore": "I got @score out of @maxScore points on",
            "shareLink": "Link to this page",
            "confirmCloseHeader": "Close the book?",
            "confirmCloseBody": "Are you sure you want to close the book? Progress will be lost.",
            "confirmCloseCancel": "Cancel",
            "confirmCloseConfirm": "Confirm",
            "solutionModeHeader": "Task Name",
            "solutionModeText": "Retries are disabled in this mode.",
            "noChapter": "You have not navigated to any chapter yet.",
            "markAsFinished": "I am done - continue",
            "hasStar": "Contains a summary task",
            "openSummary": "Open summary",
            "summaryHeaderIntro": "You have reached the end of",
            "summaryHeaderScore": "Your result on this course:",
        },
    }

    return content, all_used_libs


def slugify(text: str) -> str:
    """
    Convert a title to a machine-name slug for the h5p.json 'name' field.
    Rules observed from Moodle's H5P validator:
      - lowercase letters, digits, hyphens only
      - must start with a letter
      - max 64 chars
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)   # keep only a-z, 0-9, space, hyphen
    text = re.sub(r"[\s-]+", "-", text.strip())  # collapse spaces/hyphens
    text = re.sub(r"^[^a-z]+", "", text)         # ensure starts with a letter
    return text[:64].strip("-")


def build_h5p_json(title: str, used_libs: set[str]) -> dict:
    # InteractiveBook is always first (it is the mainLibrary).
    # Then text, then question types actually used.
    dep_order = [
        "interactive-book", "column", "text", "image",
        "multiple-choice", "fill-in-the-blank", "true-false",
        "drag-the-words",
    ]
    deps = [lib_entry(k) for k in dep_order if k in used_libs]
    return {
        "name": slugify(title),
        "title": title,
        "language": "und",
        "mainLibrary": "H5P.InteractiveBook",
        "embedTypes": ["div"],
        "license": "U",
        "preloadedDependencies": deps,
    }


# ---------------------------------------------------------------------------
# ZIP writer
# ---------------------------------------------------------------------------


def _read_as_landscape(img_path: Path, hint: str) -> tuple[bytes, str]:
    """Return (image_bytes, filename_hint).

    Portrait images (height > width) are padded with a neutral background to a
    2:1 landscape canvas so they display at a reasonable height when H5P.Image
    renders them at full container width.  Landscape images are returned as-is.
    """
    try:
        import io as _io
        from PIL import Image as _PILImg

        with _PILImg.open(img_path) as img:
            w, h = img.size
            if h <= w:                          # already landscape — pass through
                return img_path.read_bytes(), hint

            # Portrait: embed in a 2:1 landscape canvas
            canvas_w = max(w * 2, 600)
            canvas_h = h
            canvas = _PILImg.new("RGB", (canvas_w, canvas_h), (250, 250, 250))
            paste_x = (canvas_w - w) // 2
            rgb = img.convert("RGB")
            canvas.paste(rgb, (paste_x, 0))

            buf = _io.BytesIO()
            canvas.save(buf, format="PNG", optimize=True)
            # Return with .png hint so _add_to_zip uses the correct extension
            stem = hint.rsplit(".", 1)[0] if "." in hint else hint
            return buf.getvalue(), stem + ".png"

    except Exception:
        return img_path.read_bytes(), hint


def _bundle_images(content: dict, zf: zipfile.ZipFile, source_dir: Path) -> None:
    """Bundle images into the ZIP (local files and external URLs) and update src= in-place."""
    seen: dict[str, str | None] = {}  # original src → zip-local path
    counter = [0]

    H5P_IMG_EXTS = {"jpg", "jpeg", "png", "gif", "bmp", "tif", "tiff", "webp"}

    def _add_to_zip(data: bytes, hint: str) -> str | None:
        ext = hint.split("?")[0].rsplit(".", 1)[-1].lower()
        if ext == "svg":
            print(
                f"WARNING: H5P does not allow SVG files. "
                f"Convert {hint} to PNG (e.g. with matplotlib) and update the reference.",
                file=sys.stderr,
            )
            return None
        if ext not in H5P_IMG_EXTS:
            ext = "png"
        counter[0] += 1
        local = f"images/img_{counter[0]:03d}.{ext}"
        zf.writestr(f"content/{local}", data)
        return local

    def _resolve(src: str) -> str | None:
        if src in seen:
            return seen[src]
        if src.startswith("http://") or src.startswith("https://"):
            try:
                req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
                data = urllib.request.urlopen(req, timeout=15).read()
                local = _add_to_zip(data, src)
                seen[src] = local
                if local:
                    print(f"  bundled (url):   {src[:72]}")
            except Exception as exc:
                print(f"WARNING: Could not fetch {src[:72]}: {exc}", file=sys.stderr)
                seen[src] = None
        else:
            # Local path relative to the markdown file's directory
            img_path = source_dir / src
            if img_path.exists():
                data, hint = _read_as_landscape(img_path, src)
                local = _add_to_zip(data, hint)
                seen[src] = local
                if local:
                    print(f"  bundled (local): {src}")
            else:
                print(f"WARNING: Local image not found: {img_path}", file=sys.stderr)
                seen[src] = None
        return seen[src]

    def _rewrite(html: str) -> str:
        def _sub(m: re.Match) -> str:
            local = _resolve(m.group(2))
            if local:
                return f'<img{m.group(1)}src="{local}"{m.group(3)}>'
            alt_m = re.search(r'alt="([^"]*)"', m.group(0))
            alt = alt_m.group(1) if alt_m else "Image"
            return f"<p><em>[Image: {alt}]</em></p>"
        html = EXT_IMG.sub(_sub, html)
        html = LOCAL_IMG.sub(_sub, html)
        return html

    def _walk(obj: Any) -> None:
        if isinstance(obj, dict):
            # H5P.Image item — resolve file.path
            if obj.get("library", "").startswith("H5P.Image"):
                file_info = obj.get("params", {}).get("file", {})
                src = file_info.get("path", "")
                if src:
                    local = _resolve(src)
                    if local:
                        file_info["path"] = local
                        ext = local.rsplit(".", 1)[-1].lower()
                        file_info["mime"] = MIME_TYPES.get(ext, "image/png")
                return  # don't recurse further into this item
            for k in list(obj):
                v = obj[k]
                if k == "text" and isinstance(v, str) and "<img" in v:
                    obj[k] = _rewrite(v)
                else:
                    _walk(v)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)

    _walk(content)
    bundled = sum(1 for v in seen.values() if v)
    failed  = sum(1 for v in seen.values() if v is None)
    if bundled:
        print(f"Images  : {bundled} bundled into package")
    if failed:
        print(f"WARNING : {failed} image(s) missing — shown as italic alt text", file=sys.stderr)


def write_h5p(h5p_meta: dict, content: dict, dest: Path, source_dir: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        _bundle_images(content, zf, source_dir)
        zf.writestr("h5p.json", json.dumps(h5p_meta, indent=2, ensure_ascii=False))
        zf.writestr(
            "content/content.json",
            json.dumps(content, indent=2, ensure_ascii=False),
        )
    dest.write_bytes(buf.getvalue())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a markdown reading file to a single H5P.InteractiveBook package.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Library version overrides (must match what is installed in your Moodle):
  --book   X.Y   H5P.InteractiveBook  (default 1.7)
  --column X.Y   H5P.Column           (default 1.16)
  --text   X.Y   H5P.AdvancedText     (default 1.1)
  --mc     X.Y   H5P.MultiChoice      (default 1.16)
  --tf     X.Y   H5P.TrueFalse        (default 1.8)
  --fib    X.Y   H5P.Blanks           (default 1.14)
  --dw     X.Y   H5P.DragText         (default 1.10)

Example:
  python scripts/md_to_h5p.py weeks/01/reading.md --book 1.6 --column 1.15
        """,
    )
    parser.add_argument("source", help="Path to the markdown file (e.g. weeks/01/reading.md)")
    parser.add_argument("--out", default=None,
                        help="Output .h5p path (default: same dir/stem as source)")
    for flag, key, default in [
        ("--book",   "interactive-book",  "1.7"),
        ("--column", "column",            "1.16"),
        ("--text",   "text",              "1.1"),
        ("--mc",     "multiple-choice",   "1.16"),
        ("--tf",     "true-false",        "1.8"),
        ("--fib",    "fill-in-the-blank", "1.14"),
        ("--dw",     "drag-the-words",    "1.10"),
    ]:
        parser.add_argument(flag, dest=f"ver_{key.replace('-','_')}", default=default,
                            metavar="X.Y", help=argparse.SUPPRESS)
    args = parser.parse_args()

    for flag_dest, lib_key in [
        ("ver_interactive_book",  "interactive-book"),
        ("ver_column",            "column"),
        ("ver_text",              "text"),
        ("ver_multiple_choice",   "multiple-choice"),
        ("ver_true_false",        "true-false"),
        ("ver_fill_in_the_blank", "fill-in-the-blank"),
        ("ver_drag_the_words",    "drag-the-words"),
    ]:
        raw = getattr(args, flag_dest, None)
        if raw:
            try:
                major, minor = raw.split(".")
                name = LIBRARIES[lib_key][0]
                LIBRARIES[lib_key] = (name, int(major), int(minor))
            except (ValueError, KeyError):
                sys.exit(f"ERROR: bad version '{raw}' for {lib_key} -- use X.Y format.")

    source = Path(args.source)
    if not source.exists():
        sys.exit(f"ERROR: File not found: {source}")

    dest = Path(args.out) if args.out else source.with_suffix(".h5p")

    md_text = source.read_text(encoding="utf-8")
    title = extract_title(md_text)
    raw_chapters = split_into_chapters(md_text)

    # Parse each chapter body into segments, keeping a global question counter
    q_index = 0
    chapters = []
    for ch in raw_chapters:
        segs, q_index = parse_chapter_body(ch["body"], q_start=q_index)
        chapters.append({"title": ch["title"], "segments": segs})

    total_q    = sum(1 for ch in chapters for s in ch["segments"] if s["kind"] == "question")
    total_text = sum(1 for ch in chapters for s in ch["segments"] if s["kind"] == "text")
    print(f"Source  : {source}")
    print(f"Title   : {title}")
    print(f"Pages   : {len(chapters)}  ({', '.join(ch['title'] for ch in chapters)})")
    print(f"Content : {total_text} text block(s), {total_q} question(s)")

    if not chapters:
        sys.exit("ERROR: No content found.")

    content, used_libs = build_interactive_book_content(chapters, source_dir=source.parent)
    h5p_meta = build_h5p_json(title, used_libs)
    write_h5p(h5p_meta, content, dest, source.parent)

    print(f"Output  : {dest}  ({dest.stat().st_size // 1024 + 1} KB)")
    print()
    print("Import into Moodle: Activities > H5P  OR  H5P Content bank > Add > Upload.")
    if _markdown_lib is None:
        print()
        print("TIP: pip install markdown  for better text rendering (tables, fenced code, etc.).")


if __name__ == "__main__":
    main()
