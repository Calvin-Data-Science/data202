"""
Shared engine for the printed in-class handouts (weeks/NN/class_wNNdD_handout.pdf).

Each handout has an editable markdown source (class_wNNdD_handout.md) and a small
build script (scripts/make_wNNdD_handout.py) that draws that class's plots and calls
build(). The class notebook is the slides/demonstration; the handout holds the student
activities, drawn on the same data as the notebook.

Markdown format (also explained in each .md's top comment):
  "# ..."              the title line at the top of page 1
  "## ..."             one handout part
  ![](plot:NAME)       the part's plot, drawn by the build script; optional {width=NN%}
                       (default 46): under 80% the plot sits left and the text right;
                       80% or more, the plot spans the page with the text below it
  ____                 4+ underscores = a blank to write on (longer run = longer blank);
                       a line with only underscores = a full-width writing line
  \\newpage             start a new page
  bold, italic, $math$, numbered lists and pipe tables are normal pandoc markdown.
HTML comments (<!-- ... -->) are not printed.

Requires: pandoc + xelatex (same as build_quiz.py).
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_quiz import PREAMBLE, raw_latex, tex_escape

DEFAULT_PLOT_WIDTH = 46      # % of the text width; the text column gets the rest
FULL_WIDTH_FROM = 80         # plots at least this wide go above their text instead

PLOT_STYLE = {               # matplotlib rcParams shared by every handout's plots
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.6, "axes.axisbelow": True,
}

PLOT_LINE = re.compile(r"^!\[[^\]]*\]\(plot:(\w+)\)(?:\{width=(\d+)%\})?\s*$")


def blanks(text):
    """Underscore runs -> ruled blanks: a whole line of them spans the width, 4+ inline = a short blank."""
    out = []
    for line in text.split("\n"):
        full = re.fullmatch(r"(\s*)_{3,}\s*", line)
        if full:   # keep the indentation, so a line inside a list item stays in that item
            out.append(full.group(1) + r"`\rule{\linewidth}{0.4pt}`{=latex}")
        else:
            # `...`{=latex} = pandoc's explicit inline raw LaTeX; a bare \rule would become its own paragraph
            out.append(re.sub(r"_{4,}", lambda m: r"`\rule{%.1fcm}{0.4pt}`{=latex}" % max(1.2, 0.35 * len(m.group(0))), line))
    return "\n".join(out)


def parse(md_text):
    """-> (title, intro, [(heading, plot_name or None, plot_width_pct, body, newpage_after)])"""
    text = re.sub(r"<!--.*?-->", "", md_text, flags=re.S).strip()
    title_match = re.search(r"^# (.+)$", text, flags=re.M)
    assert title_match, "the handout .md needs a '# Title' line"
    title = title_match.group(1).strip()
    text = text[title_match.end():]

    chunks = re.split(r"^## (.+)$", text, flags=re.M)      # [intro, heading1, body1, heading2, body2, ...]
    intro = chunks[0].strip()
    parts = []
    for heading, body in zip(chunks[1::2], chunks[2::2]):
        plot, width, kept, newpage = None, DEFAULT_PLOT_WIDTH, [], False
        for line in body.strip().split("\n"):
            m = PLOT_LINE.match(line.strip())
            if m:
                plot, width = m.group(1), int(m.group(2) or DEFAULT_PLOT_WIDTH)
            elif line.strip() == r"\newpage":
                newpage = True
            else:
                kept.append(line)
        parts.append((heading.strip(), plot, width, "\n".join(kept).strip(), newpage))
    return title, intro, parts


def build_md(title, intro, parts, plots):
    preamble = (PREAMBLE % dict(header_left=tex_escape(title))).replace(
        r"\usepackage[margin=1in]{geometry}", r"\usepackage[margin=0.6in]{geometry}" "\n" r"\usepackage{graphicx}")
    out = [
        "---\npapersize: letter\ngeometry: margin=0.6in\nfontsize: 11pt\nheader-includes:\n  - |\n"
        + "\n".join("    " + line for line in preamble.strip("\n").splitlines())
        + "\n---\n",
        raw_latex(r"\noindent{\Large\bfseries %s}\par\vspace{4pt}\hrule\vspace{8pt}" % tex_escape(title)),
        blanks(intro) + "\n",
    ]
    for heading, plot, width, body, newpage in parts:
        out.append(f"## {heading}\n")
        if plot:
            assert plot in plots, f"unknown plot:{plot} -- choose from {sorted(plots)}"
            path = str(plots[plot]).replace("\\", "/")
            if width >= FULL_WIDTH_FROM:
                out.append(raw_latex(r"\noindent\includegraphics[width=%.2f\linewidth]{%s}\par\vspace{4pt}"
                                     % (width / 100, path)))
                out.append(blanks(body) + "\n")
            else:
                out.append(raw_latex(
                    r"\noindent\begin{minipage}[t]{%.2f\linewidth}\vspace{0pt}" % (width / 100) + "\n"
                    + r"\includegraphics[width=\linewidth]{%s}" % path + "\n"
                    + r"\end{minipage}\hfill" + "\n"
                    + r"\begin{minipage}[t]{%.2f\linewidth}\vspace{0pt}\raggedright" % (0.97 - width / 100)))
                out.append(blanks(body) + "\n")
                out.append(raw_latex(r"\end{minipage}\par\vspace{6pt}"))
        else:
            out.append(blanks(body) + "\n")
        if newpage:
            out.append(raw_latex(r"\newpage"))
    return "\n".join(out)


def render_pdf(md_text, out_pdf):
    """Like build_quiz.render_pdf, plus --columns=1000: a pipe-table row longer than pandoc's default 72
    characters (easy once a ____ blank expands into raw LaTeX) would otherwise stretch the table to full width."""
    tmp_md = out_pdf.with_suffix(".tmp.md")
    tmp_md.write_text(md_text, encoding="utf-8")
    try:
        result = subprocess.run(["pandoc", str(tmp_md), "-o", str(out_pdf), "--pdf-engine=xelatex", "--columns=1000"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"pandoc FAILED for {out_pdf.name}:", result.stdout, result.stderr, sep="\n", file=sys.stderr)
            sys.exit(1)
        print(f"Wrote {out_pdf}")
    finally:
        tmp_md.unlink(missing_ok=True)


def build(source_md, out_pdf, make_plots):
    """Parse source_md, let make_plots(outdir) draw every plot (returns {name: path}), write out_pdf."""
    title, intro, parts = parse(Path(source_md).read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:          # no spaces in this path, so LaTeX can include the plots
        plots = make_plots(Path(tmp))
        render_pdf(build_md(title, intro, parts, plots), Path(out_pdf))
