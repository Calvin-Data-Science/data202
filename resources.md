---
layout: default
title: Resources
permalink: /resources/
---

# Resources

## Running Notebooks

All class materials and practices are `.ipynb` (Jupyter notebook) files, opened and run in **VS Code** — either connected to Calvin's cloud workspace (Coder) or installed on your own machine. Download the file from the course website and run it in one of two ways.

### Required VS Code extensions

Whichever option you use, two extensions make `.ipynb` files work in VS Code:

- **[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)** (`ms-python.python`) — Python language support and environment/interpreter selection
- **[Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)** (`ms-toolsai.jupyter`) — adds the notebook editor itself (cells, kernel picker, outputs)

On a Coder workspace these are pre-installed. Installing VS Code locally, install both from the Extensions panel (`Ctrl+Shift+X`, search by name) before opening any `.ipynb` file.

**Optional but useful:** the **[GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)** extension (plus **GitHub Copilot Chat**) works directly inside notebook cells in VS Code — inline suggestions appear as you type in a code cell, and you can select a cell (or just place your cursor in it) and open Copilot Chat (`Ctrl+Alt+I`) to ask about or modify just that cell, similar to Colab's cell-level AI assistant. Calvin students can get Copilot for free through the [GitHub Student Developer Pack](https://education.github.com/pack) (see [Version Control](#version-control) below) — remember the course's [LLM use policy](/syllabus/#use-of-llms) still applies to anything it suggests.

### Option A — Coder (Recommended)

Calvin provides a cloud-based development environment through **Coder** — nothing to install for the environment itself, only VS Code.

1. Log in at [coder.cs.calvin.edu](https://coder.cs.calvin.edu) with your Calvin credentials and start your workspace
2. Open it one of two ways:
   - **In the browser** — click the workspace's VS Code (browser) button; this opens a full VS Code interface, ready to use with no local install at all
   - **In VS Code Desktop** — install [VS Code](https://code.visualstudio.com/) locally, install the **Coder** extension (`coder.coder-remote`) from the Extensions panel, then use it to connect to your workspace; VS Code Desktop then runs against the remote workspace exactly as if the files were local
3. Download the `.ipynb` file from the course website
4. Upload it into your workspace — in the browser VS Code, the Explorer sidebar (the file-tree panel on the left, usually already open; click the top icon in the left activity bar if not) is where files live. Either:
   - **Drag the file** from your computer straight onto the Explorer panel, or
   - Right-click empty space inside the Explorer panel and choose **Upload...**, then pick the file from your computer's file picker

   If a notebook needs extra files too (a dataset or image, for a few notebooks that don't load data straight from a URL), upload those the same way, into the same folder as the notebook.
5. Click the uploaded `.ipynb` file in the Explorer to open it
6. In the top-right of the notebook, use **Select Kernel** to pick the Python environment (only needed once per workspace), then run cells with **Shift + Enter**

**Tip:** files persist in your workspace between sessions — always save before closing.

### Option B — Local Installation

If you prefer to run notebooks entirely on your own machine:

1. Install Python — either [Anaconda](https://www.anaconda.com/download) (includes Python plus most scientific libraries) or a plain install from [python.org](https://www.python.org/downloads/)
2. Install [VS Code](https://code.visualstudio.com/), then the **Python** and **Jupyter** extensions (see above)
3. Install the course's required packages — see [Configuring Your Environment](#configuring-your-environment) below
4. Download the `.ipynb` file from the course website into a local folder
5. In VS Code, use **File → Open Folder** on that folder (recommended, so relative paths to datasets/images resolve correctly), then open the `.ipynb` file from the Explorer sidebar
6. Use **Select Kernel** in the top-right of the notebook to choose your Python interpreter, then run cells with **Shift + Enter**

### Jupyter Notebooks — Key Concepts

- A notebook is made of **cells** — each is either *code* (Python) or *text* (Markdown)
- Run a cell with **Shift + Enter**; output appears directly below
- Cells share state within a session — variables defined in one cell are available in all others
- Order matters: run cells top-to-bottom; re-run earlier cells if you change them
- *Restarting the kernel* clears all variables — you'll need to re-run from the top
- Before submitting, use the notebook toolbar's **Restart** button followed by **Run All** to confirm your notebook runs clean from scratch

**References:**
- [VS Code Jupyter Notebooks documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- [VS Code keyboard shortcuts](https://code.visualstudio.com/docs/getstarted/keybindings)
- [Markdown cheatsheet](https://www.markdownguide.org/cheat-sheet/) — for formatting text cells

---

## Configuring Your Environment

**On Coder:** every package this course uses — `pandas`, `plotly`, `scikit-learn`, and `otter-grader` — is already installed in your workspace. Nothing to do here; skip to the next section.

**On a local install:** open a terminal (VS Code's built-in terminal, `` Ctrl+` ``) and run:

```bash
pip install pandas plotly scikit-learn otter-grader
```

`pip` isn't always on your PATH, or (rarely, these days) might point at Python 2 instead of Python 3. `pip` and `pip3` almost always do the exact same thing — try them in this order until one works:

```bash
pip install pandas plotly scikit-learn otter-grader
pip3 install pandas plotly scikit-learn otter-grader
python -m pip install pandas plotly scikit-learn otter-grader
```

If neither `pip` nor `pip3` is recognized at all (`'pip' is not recognized...` / `command not found`), `python -m pip install ...` almost always works — it runs pip through whichever `python` you already use to run your code, rather than relying on `pip` being on your PATH separately. (If `python` itself isn't recognized either, try `python3 -m pip install ...` instead.)

**Verify it worked** — run this in the same terminal:

```bash
python -c "import pandas, plotly, sklearn, otter; print('All good!')"
```

If that prints `All good!` with no errors, you're set for every notebook and practice this semester.

---

## Autograding with Otter

This course uses **[otter-grader](https://otter-grader.readthedocs.io/)** for automatic feedback on in-class exercises and practices. (Already installed on Coder; see [Configuring Your Environment](#configuring-your-environment) above for local setup.)

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
