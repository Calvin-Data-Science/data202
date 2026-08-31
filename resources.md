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
   - **In the browser** — click the workspace's VS Code (browser) button; this opens a full VS Code interface with the Python/Jupyter extensions already installed, no local install needed at all
   - **In VS Code Desktop** — install [VS Code](https://code.visualstudio.com/) locally, install the **Coder** extension (`coder.coder-remote`) from the Extensions panel, then use it to connect to your workspace; VS Code Desktop then runs against the remote workspace exactly as if the files were local
3. Download the `.ipynb` file from the course website
4. Open it in your workspace (drag-and-drop into the Explorer sidebar, or use the file upload button), then open the file
5. In the top-right of the notebook, use **Select Kernel** to pick the Python environment (only needed once per workspace), then run cells with **Shift + Enter**

**Tip:** files persist in your workspace between sessions — always save before closing.

### Option B — Local Installation

If you prefer to run notebooks entirely on your own machine:

1. Install Python — either [Anaconda](https://www.anaconda.com/download) (includes Python plus most scientific libraries) or a plain install from [python.org](https://www.python.org/downloads/)
2. Install [VS Code](https://code.visualstudio.com/)
3. In VS Code, install the **Python** and **Jupyter** extensions (see above)
4. Open a terminal (VS Code's built-in terminal, `` Ctrl+` ``) and install any missing libraries:
   ```bash
   pip install pandas plotly scikit-learn otter-grader
   ```
5. Download the `.ipynb` file from the course website into a local folder
6. In VS Code, use **File → Open Folder** on that folder (recommended, so relative paths to datasets/images resolve correctly), then open the `.ipynb` file from the Explorer sidebar
7. Use **Select Kernel** in the top-right of the notebook to choose your Python interpreter, then run cells with **Shift + Enter**

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
