---
layout: default
title: Resources
permalink: /resources/
---

# Resources

## Development Environment

### Coder
The course uses a cloud-based coding environment through **Coder**, so you don't need to install anything locally.

- Log in at [Calvin's Coder instance](coder.cs.calvin.edu) and open a workspace
- Your workspace includes Python, Jupyter, and all required libraries pre-installed
- [What is Coder?](https://coder.com/docs/about) — remote development environments in a browser
- **Tip:** your files persist within your workspace — always save your notebooks before closing

### Google Colab
Weekly demos are provided as notebooks on **Google Colab** — no setup required, runs in a browser.

- [Open Google Colab](https://colab.research.google.com/)
- [Intro to Colab](https://colab.research.google.com/notebooks/intro.ipynb) — official getting-started notebook
- Sign in with your Google account to save your own copies

### Jupyter Notebooks

All course work is done in **Jupyter notebooks** (`.ipynb` files) — documents that mix executable code, output, and text in a single file.

**Key concepts:**
- A notebook is made up of **cells** — each cell is either *code* (Python) or *text* (Markdown)
- Run a cell with **Shift + Enter**; the output appears directly below it
- Cells share state within a session — variables defined in one cell are available in others
- Order matters: run cells top-to-bottom; re-run if you change something earlier

**Common pitfalls:**
- *Restarting the kernel* clears all variables — you'll need to re-run cells from the top
- Output is saved in the file, but the kernel state is not — always re-run on a fresh open
- Before submitting, use **Kernel → Restart & Run All** to confirm your notebook runs clean from top to bottom

**References:**
- [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/stable/)
- [Jupyter keyboard shortcuts](https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330)
- [Markdown cheatsheet](https://www.markdownguide.org/cheat-sheet/) — for formatting text cells

---

## Version Control

### GitHub
Practice assignments are distributed and submitted through **GitHub Classroom**.

- [Sign up for GitHub](https://github.com/signup) — use your `.edu` email to get the [Student Developer Pack](https://education.github.com/pack) for free
- Each practice will give you a GitHub Classroom link that creates a personal repo for your work
- Push your completed notebook to your repo to submit

**Getting started with Git & GitHub:**
- [GitHub's own quickstart guide](https://docs.github.com/en/get-started/quickstart)
- [Git cheat sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
- Key commands you'll use:

```bash
git add .
git commit -m "completed practice"
git push
```

---

## Core Libraries

### pandas — Data Manipulation & Analysis
- [Website](https://pandas.pydata.org/) · [Docs](https://pandas.pydata.org/docs/) · [Getting Started Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)

### plotly — Visualization
- [Website](https://plotly.com/) · [Python Docs](https://plotly.com/python/) · [Getting Started](https://plotly.com/python/getting-started/)

### scikit-learn — Modeling & Machine Learning
- [Website](https://scikit-learn.org/) · [Docs](https://scikit-learn.org/stable/documentation.html) · [Basic Tutorial](https://scikit-learn.org/stable/tutorial/basic/tutorial.html)