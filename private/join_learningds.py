import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description='Join PDFs of each chapter.')
parser.add_argument('--chapters', type=str, default="all", help='chapter numbers, separated by commas, or "all"')
parser.add_argument('--path', type=str, default='../learningds', help='path to directory containing pdf files')

args = parser.parse_args()

path = Path(args.path)

if args.chapters == "all":
    chapters = sorted(set([f.name.split(".")[0] for f in path.glob("*.pdf")]))
    # only the numeric
    chapters = [c for c in chapters if c.isnumeric()]
else:
    chapters = args.chapters.split(",")
    chapters = [c.strip() for c in chapters]

for chapter in chapters:
    # We want to run this command: qpdf --empty --pages $chapter.\ *.pdf $chapter.*.*.pdf -- "LGN Chapter $chapter.pdf"
    # But we need to expand those globs first.
    intro_page = list(path.glob(f"{chapter}. *.pdf"))
    assert len(intro_page) == 1
    intro_page = intro_page[0]
    section_pages = sorted(path.glob(f"{chapter}.*.*.pdf"))
    assert intro_page not in section_pages
    assert len(section_pages) > 0

    for page in [intro_page, *section_pages]:
        print(" ", page)
    subprocess.run(["qpdf", "--empty", "--pages", str(intro_page), *map(str, section_pages), "--", f"LGN Chapter {chapter}.pdf"], cwd=path)
