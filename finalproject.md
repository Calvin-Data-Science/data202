---
layout: default
title: Final Project
permalink: /finalproject/
math: true
---

# Final Project

The final project asks you to carry out a complete data science workflow: frame a meaningful question, acquire and document a dataset, explore and clean the data, train and compare models, interpret the results, and engage critically with the ethical dimensions of the problem. All of this is submitted as a single Jupyter notebook — your code, narrative, and outputs together — plus a brief presentation to the class during the final exam period.

The notebook should read at the level of a polished blog post: more rigorous than a homework assignment, less formal than an academic paper. The overview and key visualizations should be understandable to a non-specialist; the methods sections should use precise technical language. You will also situate your work relative to prior analyses on the same topic, showing not just that you can execute an analysis, but that you can evaluate one.

## Specifications

Each spec will have three possible outcomes: **A** (Achieved), **P** (Partially Achieved), or **N** (No Evidence Yet). See the [Assessment & Grading](/syllabus/#assessment) section to check how they will count to your final grade.

The specs are:

1. **[Pose a clear, meaningful data question.](#spec-1)** Identify a well-scoped problem, frame it as a data question, and situate it within relevant background knowledge or prior work in the domain.

2. **[Identify and document a quality dataset.](#spec-2)** Select data appropriate to the question and describe its provenance — source, collection method, and license. Discuss any known limitations or potential issues with the data.

3. **[Conduct exploratory data analysis.](#spec-3)** Characterize variable types and distributions, identify missing values and outliers, and produce informative visualizations that motivate subsequent modeling decisions.

4. **[Clean, transform, and engineer features.](#spec-4)** Handle missing data and outliers, encode categorical variables, scale or normalize as needed, and construct or select features suited to the chosen model.

5. **[Select, train, and evaluate a model.](#spec-5)** Choose a model appropriate to the problem type, justify that choice, train it with a sound validation strategy, and report performance using suitable metrics.

6. **[Compare at least two modeling approaches.](#spec-6)** Train and evaluate multiple models or configurations, discuss trade-offs in performance, complexity, and interpretability, and explain the rationale behind the final choice.

7. **[Interpret findings and draw evidence-based conclusions.](#spec-7)** Answer the original data question based on the results, acknowledge limitations and uncertainty, and avoid overstating what the data can support.

8. **[Engage critically with ethical and broader societal/cultural implications.](#spec-8)** Identify potential sources of bias, fairness concerns, and broader societal impact. Reference relevant concepts or techniques and, where feasible, apply them to the analysis.

9. **[Present a reproducible, well-documented notebook.](#spec-9)** Organize the notebook or report logically, write clearly and precisely, use appropriate formatting, and ensure all results can be reproduced from the submitted code and data.

10. **[Meet project milestones on schedule.](#spec-10)** Submit work on time: at least 3 of 4 milestone checkpoints and the 2 in-class progress checks (A), or at least 2 of 4 milestones and 1 of the 2 in-class progress checks (P).

## Logistics

**Individual or pairs.** You may work alone or in pairs; pairs are encouraged. If working in pairs, both partners are expected to contribute meaningfully to all parts of the project — not to divide it into independent halves.

**Presentations.** The final class meeting (held during the designated final exam period) is devoted to project presentations. Giving and receiving peer feedback counts toward your grade, so attendance is mandatory. Because this course has two sections, there will be two presentation sessions — check the Calvin exam schedule for the exact dates and times.

**Submission.** Your final deliverable is a Jupyter notebook — there is no separate written report. The notebook is the report: it combines your prose narrative (in markdown cells), your code, and your outputs in a single document. Submit the `.ipynb` file along with any data files or helper scripts needed to run it from scratch.

### Milestones {#milestones}

The project is structured around **4 milestones** and **2 in-class progress checks** to prevent the all-too-common pattern of leaving everything to the last week. For each milestone, you are expected to have completed the described work, not just to have started it.

The two **in-class progress checks** (at Milestones 3 and 4) are dedicated class sessions where you share your work-in-progress with both the instructor and your peers. These are low-stakes but high-value: you will give and receive structured feedback, and the conversation often surfaces problems or ideas that no individual review would catch. Attendance at both sessions is part of Specification 10.

---

#### Milestone 1 — Proposal

*Roughly covers: Specs [1](#spec-1) and [2](#spec-2).*

Submit a short written proposal (roughly one page) covering:
- The question you want to investigate and why it is interesting
- The dataset you plan to use, including its source and a brief description
- The type of modeling approach you expect to use
- Any concerns or open questions you already see

The goal is to get early feedback before you have invested significant effort in a direction that may not work.

---

#### Milestone 2 — Data in hand

*Roughly covers: Specs [2](#spec-2), [3](#spec-3), and [4](#spec-4).*

By this checkpoint, your data work should be complete:
- Dataset acquired, loaded, and documented
- Exploratory analysis done: distributions, missing values, key relationships visualized
- Data cleaned, transformed, and features engineered
- A brief written narrative explaining the decisions you made and why

---

#### Milestone 3 — Modeling complete *(+ in-class progress check)*

*Roughly covers: Specs [5](#spec-5), [6](#spec-6), [7](#spec-7)*

By this checkpoint, your core analysis should be done:
- At least two models trained, evaluated, and compared
- Results interpreted in relation to your original question
- Ethical and societal implications identified and discussed

This milestone includes an **in-class progress check**: bring your work to class and be ready to walk through it. You will give feedback to others and receive feedback in return.

---

#### Milestone 4 — Final review *(+ in-class progress check)*

*Roughly covers: Specs [7](#spec-7), [8](#spec-8) and [9](#spec-9).*

At this point the substantive work is finished. The focus is on polish and presentation:
- Notebook is complete and ready for a critical read
- Visualizations are clear and publication-quality
- Code is clean, commented, and reproducible

A second **in-class progress check** gives you one last round of peer and instructor feedback before the final presentation. Use it.

---

## Detailed expectations

### Spec 1 — Pose a clear, meaningful data question {#spec-1}

Your question should be understandable to someone who has not studied data science and does not know your dataset. It should be specific enough to be answerable with data and modeling, but grounded in something that genuinely matters — a real-world phenomenon, a social pattern, a practical decision. The best questions include motivation from prior literature: some pattern or relationship you expect to find, and why.

Your project must include modeling — it should go beyond making visualizations. Predictive modeling is closest to the emphasis of this course, but clustering and other unsupervised approaches are also acceptable with a clear rationale.

**Project types that have worked well:**
- *Participating in a Kaggle competition.* Choose one that is still open. You do not need to win, but you should beat the baseline and contribute original EDA or visualizations beyond what is already in the public notebooks.
- *Reproducing and extending a published analysis.* Find a published analysis, reproduce its core findings, then extend it — different data, an additional model, a new angle on the question.
- *Exploring an interpretable model.* Compare a newer interpretable model to a traditional one from class.

**Finding inspiration:** Kaggle, TowardsDataScience, TidyTuesday, r-bloggers, GitHub, and YouTube are good starting points.

Your notebook’s *Overview* section should open with the real-world question, explain why it is interesting, and include a 2–4 sentence description of the dataset (what it contains, where it came from).

---

### Spec 2 — Identify and document a quality dataset {#spec-2}

Describe the dataset’s provenance in as much detail as you can: where did the data originate, how was it collected, where did you download it from, and under what license is it available? Trace the path from the real-world events or measurements to the file you are working with.

Your documentation should include:
- The number of rows and what each row represents
- A list of the features (columns) and their types
- An example row described in plain language (e.g., “This row represents a patient aged 54 with a blood pressure reading of 130/85…”)
- An honest assessment of the dataset’s suitability: what is good about it for your purposes, and what do you wish were better?

**Practical constraints:** Avoid datasets larger than 500 MB — they are unlikely to fit in a typical Colab or notebook environment. Avoid raw image or audio data unless you have discussed a plan with the instructor in advance.

---

### Spec 3 — Conduct exploratory data analysis {#spec-3}

EDA should inform every downstream decision — it is not a box to check before the “real” analysis begins. Your notebook should show:
- Distributions of at least two variables, with commentary on shape, skew, and outliers
- Bivariate relationships for at least two pairs of variables, with commentary on strength, direction, and any surprising patterns
- A summary of what the EDA reveals and how it shapes your modeling choices

Strong EDA goes beyond histograms: look for unexpected values, class imbalances, temporal trends, or relationships that complicate simple modeling assumptions.

---

### Spec 4 — Clean, transform, and engineer features {#spec-4}

You will inevitably make judgment calls: which variables to include, how to handle missing values, whether to create new features. Document each significant decision by stating:
- **What** you decided
- **Why** you made that choice
- **What the alternatives were** and why you did not take them

Write the “rational reconstruction” of your analysis — the coherent story of the choices that shaped the work. Do not narrate every failed experiment, but do include dead ends that led to an important realization.

---

### Spec 5 — Select, train, and evaluate a model {#spec-5}

Clearly state the modeling setup before presenting results:
- What is the target variable?
- Which features are you using to predict it, and why those?
- How will you measure performance? Can you give the metric meaningful real-world units?
- What validation strategy did you choose (train/test split, cross-validation, etc.) and why?

Fit at least one model from the techniques covered in class (Decision Trees, Linear/Logistic Regression, Random Forests, etc.). Describe why you chose it, what performance you expected, and report results via your chosen validation method. Where applicable, walk through what the model predicts for one or two specific examples — ideally ones that are not in your training set.

---

### Spec 6 — Compare at least two modeling approaches {#spec-6}

Train and evaluate at least two models or configurations. For each, explain what you changed, why, and what happened. Discuss trade-offs in performance, complexity, and interpretability — not just which number was higher.

Strong notebooks include visualizations of the models, their predictions, and their mistakes. A confusion matrix, a residual plot, a feature importance chart, or a decision boundary can reveal things that aggregate metrics hide. Report final performance on a held-out test set where applicable.

If you are doing an unsupervised task (clustering), compare at least two configurations (different k, different linkage, etc.) and clearly state what you are trying to understand through the comparison.

---

### Spec 7 — Interpret findings and draw evidence-based conclusions {#spec-7}

Your *Findings* section should answer the original question based on actual results — not just restate the metrics. What do the numbers mean in the real-world context you started with?

Acknowledge limitations honestly: small sample size, unrepresentative data, proxy variables, or model assumptions that may not hold. Do not overstate what the data can support. Identify at least one *Future Direction* — a new question that emerged from the work, and what data or approach would be needed to pursue it.

---

### Spec 8 — Engage critically with ethical and societal implications {#spec-8}

This is not a section to bolt on at the end. Think through:
- Who or what is represented in the data, and who is not?
- If the model’s predictions were used in a real decision, who would be affected — and how?
- Are there features that act as proxies for protected characteristics?
- What is being optimized, and for whom?

At minimum, identify the relevant concerns and reference concepts or techniques from the course (fairness metrics, disparate impact, etc.). Where feasible, apply them — for example, by computing disaggregated performance across demographic groups.

---

### Spec 9 — Present a reproducible, well-documented notebook {#spec-9}

Your notebook is both the code and the report — there is no separate document. A reader should be able to follow the narrative without running a single cell; someone else should be able to run every cell from top to bottom and reproduce all results. Specifically:
- Submit the `.ipynb` file plus any data files or scripts needed to run it from scratch
- Cite any code taken or adapted from the internet with a link and author
- Write your markdown cells as prose — aim for the register of a polished blog post, not a stream of inline comments
- Use section headers, figure captions, and consistent variable names to help the reader navigate
- Primary visualizations should be interpretable by a non-technical reader; the methods sections should use precise technical language

You will also submit slides for the final presentation separately.

---

### Spec 10 — Meet project milestones on schedule {#spec-10}

See the [Milestones](#milestones) section for the specific deliverables expected at each checkpoint. Meeting this spec requires submitting the right work at the right time — not just eventually.