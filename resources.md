---
layout: default
title: Resources
permalink: /resources/
---

# Resources

## Running Notebooks

All class materials and practices are `.ipynb` (Jupyter notebook) files. Download them from the course website and run them in one of two ways.

### Option A — Coder (Recommended)

Calvin provides a cloud-based JupyterLab environment through **Coder** — nothing to install.

1. Log in at [coder.cs.calvin.edu](https://coder.cs.calvin.edu) with your Calvin credentials
2. Open your workspace — Python, JupyterLab, and all required libraries are pre-installed
3. Download the `.ipynb` file from the course website
4. Upload it to your workspace (drag-and-drop into the JupyterLab file browser, or use the upload button)
5. Double-click the file to open it, then run cells with **Shift + Enter**

**Tip:** files persist in your workspace between sessions — always save before closing.

### Option B — Local Installation

If you prefer to run notebooks on your own machine:

1. Install [Anaconda](https://www.anaconda.com/download) — includes Python, JupyterLab, and most scientific libraries
2. Open a terminal (Anaconda Prompt on Windows) and install any missing libraries:
   ```bash
   pip install plotly otter-grader
   ```
3. Download the `.ipynb` file from the course website into a local folder
4. Launch JupyterLab:
   ```bash
   jupyter lab
   ```
5. Navigate to the file in the JupyterLab file browser and open it

### Jupyter Notebooks — Key Concepts

- A notebook is made of **cells** — each is either *code* (Python) or *text* (Markdown)
- Run a cell with **Shift + Enter**; output appears directly below
- Cells share state within a session — variables defined in one cell are available in all others
- Order matters: run cells top-to-bottom; re-run earlier cells if you change them
- *Restarting the kernel* clears all variables — you'll need to re-run from the top
- Before submitting, use **Kernel → Restart & Run All** to confirm your notebook runs clean

**References:**
- [JupyterLab documentation](https://jupyterlab.readthedocs.io/en/stable/)
- [Jupyter keyboard shortcuts](https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330)
- [Markdown cheatsheet](https://www.markdownguide.org/cheat-sheet/) — for formatting text cells

---

## Autograding with Otter

This course uses **[otter-grader](https://otter-grader.readthedocs.io/)** for automatic feedback on in-class exercises and practices.

When you open a notebook, the first cell initializes the grader:

```python
import otter
grader = otter.Notebook("notebook_name.ipynb")
```

After completing each task, run the check cell below it:

```python
grader.check("task_name")
```

A ✅ means your answer passes the tests. If it fails, read the message and try again. For **class exercises**, this is just for your own feedback — nothing is collected. For **practices**, the same tests are used when your notebook is graded.

**Installation** (only needed for local setup — Coder already has it):

```bash
pip install otter-grader
```

---

## Core Libraries

### pandas — Data Manipulation & Analysis
- [Website](https://pandas.pydata.org/) · [Docs](https://pandas.pydata.org/docs/) · [Getting Started Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)

### plotly — Visualization
- [Website](https://plotly.com/) · [Python Docs](https://plotly.com/python/) · [Getting Started](https://plotly.com/python/getting-started/)

### scikit-learn — Modeling & Machine Learning
- [Website](https://scikit-learn.org/) · [Docs](https://scikit-learn.org/stable/documentation.html) · [Basic Tutorial](https://scikit-learn.org/stable/tutorial/basic/tutorial.html)

---

## Version Control

All code is managed with **Git** and hosted on **GitHub**.

- [Sign up for GitHub](https://github.com/signup) — use your `.edu` email to get the [Student Developer Pack](https://education.github.com/pack) for free
- [Git cheat sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub quickstart guide](https://docs.github.com/en/get-started/quickstart)

Key commands:

```bash
git add .
git commit -m "description of changes"
git push
```
