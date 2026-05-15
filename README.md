# DATA202 — Introduction to Machine Learning

Course website for DATA202 at Calvin University (Fall 2026).  
Live site: `https://cs.calvin.edu/courses/data/202/26fa/`

## Repository structure

```
data202/
├── _layouts/          Jekyll layouts (default, home, week)
├── _includes/         (if any)
├── assets/            CSS and static assets
├── weeks/             Per-week content pages
├── grades.html        Student grade report page (generated — see below)
├── syllabus.md
├── finalproject.md
├── resources.md
├── index.md
├── _config.yml        Jekyll config (includes baseurl for Calvin server)
├── deploy.ps1         Build + deploy script (gitignored)
└── grades/            Private grade data — gitignored, never committed
    ├── grades.xlsx    Master gradebook (Marks + Attendance sheets)
    ├── generate.py    Generates per-student JSON files from grades.xlsx
    └── grade-data/    Per-student JSON files (one per student)
        └── *.json
```

## Grade report

The `/grades/` page lets each student view their own SBG marks by entering a personal key (a Pokémon name). No student can see another student's data.

### How it works

- `grades.html` is a static page in the repo. Edit it directly.
- `grades/grades.xlsx` has two sheets:
  - **Marks** — columns: `Key`, `02A-Reading`, `02A-Quiz`, `02A-Practice`, … `PRO01`–`PRO10`, `Forum 1`–`Forum 6`
  - **Attendance** — columns: `Key`, then one column per session date
  - Values: `A`, `P`, `N`, or blank. Skip columns: `First Name`, `Last Name`, `Unnamed:*`
- `grades/generate.py` reads `grades.xlsx` and writes one JSON file per student to `grades/grade-data/`.
- Jekyll copies `grades/grade-data/*.json` into `_site/grades/grade-data/` (xlsx and generate.py are excluded via `_config.yml`).
- Student link: `https://cs.calvin.edu/courses/data/202/26fa/grades/?key=POKEMONNAME`

## Local preview

```powershell
bundle exec jekyll serve --baseurl ""
```

Then open `http://localhost:4000`. The `--baseurl ""` override is needed because `_config.yml` sets the production baseurl to `/courses/data/202/26fa`.

## Deployment

Deployment is handled by `deploy.ps1` (gitignored — contains server path and SSH key reference):

```
deploy.ps1
  1. Runs grades/generate.py (if grades.xlsx exists)
  2. Runs bundle exec jekyll build
  3. Copies _site/ to Calvin server via scp
```

The server redirect at `/courses/data/202/index.html` points to `/courses/data/202/26fa/`.

## What is gitignored

- `_site/` — Jekyll build output
- `grades/grades.xlsx` — private gradebook with student data
- `grades/grade-data/` — generated per-student JSON files
- `deploy.ps1` — deployment script with server path
