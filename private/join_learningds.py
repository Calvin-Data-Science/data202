import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description='Process chapter number.')
parser.add_argument('chapter', type=str, help='chapter number')
parser.add_argument('--path', type=str, default='/Users/ka37/Library/CloudStorage/Dropbox/Mac/Desktop/learningds', help='path to directory containing pdf files')

args = parser.parse_args()

chapter = args.chapter
path = Path(args.path)

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
