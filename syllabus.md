---
layout: default
title: Syllabus
permalink: /syllabus/
---

# Syllabus

## Learning Objectives

**Overall:** Develop the ability to explore, analyze, and model tabular data by applying mathematical, statistical, and computational tools; and effectively communicate insights, with attention to issues of interpretability, fairness, and responsible use.

There are **30 objectives** in total. Each code indicates when it is covered: the digits are the week number and the letter is its position within that week (e.g., 06B is the second objective of Week 6).

<table class="slo-table">
<thead><tr><th>Code</th><th>Learning Objective</th></tr></thead>
<tbody>
<tr class="slo-week"><td colspan="2">Week 2 &mdash; Dataframe Basics</td></tr>
<tr><td>02A</td><td>I can manipulate the structure and contents of pandas DataFrames by accessing, adding, and deleting rows and columns.</td></tr>
<tr><td>02B</td><td>I can sort, filter, and query DataFrames to find and highlight specific information.</td></tr>
<tr><td>02C</td><td>I can choose appropriate visual encodings (axes, color, size, symbol, text) to represent variables in a visualization.</td></tr>
<tr class="slo-week"><td colspan="2">Week 3 &mdash; Exploring DataFrames: grouping and plotting</td></tr>
<tr><td>03A</td><td>I can clean and transform text data using string operations in DataFrames.</td></tr>
<tr><td>03B</td><td>I can group data to calculate aggregates such as counts, means, or sums.</td></tr>
<tr><td>03C</td><td>I can produce and interpret histograms, scatter plots, line plots, and bar charts to explore a dataset visually.</td></tr>
<tr class="slo-week"><td colspan="2">Week 4 &mdash; Relational Tables: keys, joining and tidying</td></tr>
<tr><td>04A</td><td>I can describe the structure of relational data and identify key columns and relationships between tables.</td></tr>
<tr><td>04B</td><td>I can join tables using different join types (inner, left, right, outer) and explain when each is appropriate.</td></tr>
<tr><td>04C</td><td>I can reshape data between wide and long (tidy) formats.</td></tr>
<tr class="slo-week"><td colspan="2">Week 5 &mdash; Clustering &amp; Dimensionality Reduction</td></tr>
<tr><td>05A</td><td>I can apply k-means clustering to group data and interpret the resulting cluster assignments.</td></tr>
<tr><td>05B</td><td>I can evaluate clustering quality using the elbow method and silhouette score to choose an appropriate k.</td></tr>
<tr><td>05C</td><td>I can apply PCA to reduce dimensionality and interpret how much variance each component explains.</td></tr>
<tr class="slo-week"><td colspan="2">Week 6 &mdash; Classification Basics: k-NN</td></tr>
<tr><td>06A</td><td>I can train and interpret k-NN classification models and explain how the choice of k affects overfitting and underfitting.</td></tr>
<tr><td>06B</td><td>I can compute and interpret classification metrics — accuracy, precision, recall, and the confusion matrix.</td></tr>
<tr><td>06C</td><td>I can split data into training and test sets to evaluate how well a model generalizes to unseen data.</td></tr>
<tr class="slo-week"><td colspan="2">Week 7 &mdash; Decision Trees and Hyperparameter Tuning</td></tr>
<tr><td>07A</td><td>I can train and interpret decision tree models and explain how tree depth affects overfitting and underfitting.</td></tr>
<tr><td>07B</td><td>I can use cross-validation to evaluate model performance across multiple data splits.</td></tr>
<tr><td>07C</td><td>I can tune model hyperparameters using grid search.</td></tr>
<tr class="slo-week"><td colspan="2">Week 9 &mdash; Feature Engineering</td></tr>
<tr><td>09A</td><td>I can apply preprocessing steps — scaling and one-hot encoding — and explain why each is needed before modeling.</td></tr>
<tr><td>09B</td><td>I can build a scikit-learn pipeline that chains preprocessing and modeling steps into a single reproducible workflow.</td></tr>
<tr><td>09C</td><td>I can identify how missing data arise (MCAR, MAR, MNAR) and choose appropriate imputation strategies for each case.</td></tr>
<tr class="slo-week"><td colspan="2">Week 10 &mdash; Linear Regression</td></tr>
<tr><td>10A</td><td>I can train and interpret linear regression models.</td></tr>
<tr><td>10B</td><td>I can apply Ridge and Lasso regularization to reduce overfitting and explain the effect of the regularization parameter.</td></tr>
<tr><td>10C</td><td>I can compute and interpret regression performance metrics — MAE, RMSE, and R².</td></tr>
<tr class="slo-week"><td colspan="2">Week 11 &mdash; Other Models: logistic regression and ensembles</td></tr>
<tr><td>11A</td><td>I can train and interpret logistic regression models for binary and multiclass classification.</td></tr>
<tr><td>11B</td><td>I can train ensemble models (random forests, gradient boosting) and explain how they improve on a single decision tree.</td></tr>
<tr class="slo-week"><td colspan="2">Week 12 &mdash; Other Techniques: imbalanced and time-series data</td></tr>
<tr><td>12A</td><td>I can identify class imbalance in a dataset and apply techniques such as resampling or adjusted decision thresholds to address it.</td></tr>
<tr><td>12B</td><td>I can engineer features for time-series data (lag features, rolling statistics) and use time-aware train-test splits to avoid data leakage.</td></tr>
<tr class="slo-week"><td colspan="2">Week 14 &mdash; Fairness and Interpretability</td></tr>
<tr><td>14A</td><td>I can apply fairness metrics to compare model performance across demographic subgroups and articulate trade-offs between competing fairness criteria.</td></tr>
<tr><td>14B</td><td>I can use interpretability techniques — feature importance, partial dependence plots, and LIME — to explain model predictions.</td></tr>
</tbody>
</table>

## Assignments

| Assignment | Frequency | Description | Deadline |
|------------|-----------|-------------|----------|
| Retrieval Quiz | Every class | Short in-class quiz at the start of each session to reinforce recent material. Retakes are allowed as many times as you like during class time. Completion counts as attendance. | During class |
| Reading | Weekly · 11 total | Interactive H5P reading on Moodle with embedded comprehension questions. Covers the week's concepts and counts toward your mastery score on each learning objective. | Monday of the same week |
| Practice | Weekly · 11 total | Jupyter Notebook assignment started during Friday's class and completed independently. Submitted via GitHub Classroom. Directly exercises the week's skills. | Monday of the following week |
| Quiz | Every other week (alternates with Forum weeks) · 6 total | In-class quiz assessing mastery of recent learning objectives. Each new quiz will repeat questions from the previous quiz, so that you have another chance of showing mastery. Alternates with Forum weeks. | During class |
| Forum | Every other week (alternates with Quiz weeks) · 6 total | In-class annotated worksheet based on the current chapter of *Counting* by Deborah Stone — completed individually, then compared with classmates, then photographed/scanned and uploaded to Moodle. See [Forum Instructions]({{ '/forum/' | relative_url }}) for the full process. | Wednesday of the following week |
| Final Project | 4 milestones + 2 in-class progress checks + Final Submission | Semester-long data analysis project completed individually or in pairs, submitted as a Jupyter Notebook. Structured around four milestones with two in-class progress checks. See the [Final Project]({{ '/finalproject/' | relative_url }}) page for full specifications. | Saturday of certain weeks (in the second half) |

## Assessment & Grading {#assessment}

This course uses **Standards-Based Grading (SBG)**, also called Mastery Grading. Rather than accumulating points, you are assessed on your mastery of each of the 30 learning objectives listed above.

### Objective mastery

Each learning objective is tied to three assignment types: a **Reading**, a **Quiz**, and a **Practice**. Readings are scored as Completed or Incomplete; quizzes and practices are scored as **A** (Achieved), **P** (Partially Achieved), or **N** (Not Yet).

The reading must be completed first — if incomplete, mastery is **N** regardless of quiz or practice scores. Otherwise, mastery is the **lower** of your quiz and practice scores:

|             | Practice: A | Practice: P | Practice: N |
|-------------|:-----------:|:-----------:|:-----------:|
| **Quiz: A** |    **A**    |    **P**    |    **N**    |
| **Quiz: P** |    **P**    |    **P**    |    **N**    |
| **Quiz: N** |    **N**    |    **N**    |    **N**    |
{: style="width:auto"}

### Final grade

Your final letter grade depends on four criteria. In the first two columns, A counts as 1 point and P counts as 0.5. All four criteria must be met to earn the grade; falling short on Forum or Attendance alone drops the final grade by one step.

| Grade | Learning objectives | Final project | Forum | Attendance |
|-------|---------------------|---------------|-------|------------|
| A     | ≥ 28/30             | ≥ 9.5/10      | ≥ 4/6 | ≥ 93%     |
| A−    | ≥ 27/30             | ≥ 9/10        | ≥ 4/6 | ≥ 90%     |
| B+    | ≥ 26.5/30           | ≥ 8.5/10      | ≥ 3/6 | ≥ 87%     |
| B     | ≥ 25/30             | ≥ 8/10        | ≥ 3/6 | ≥ 83%     |
| B−    | ≥ 24/30             | ≥ 7.5/10      | ≥ 3/6 | ≥ 80%     |
| C+    | ≥ 23.5/30           | ≥ 7/10        | ≥ 2/6 | ≥ 77%     |
| C     | ≥ 22/30             | ≥ 6.5/10      | ≥ 2/6 | ≥ 73%     |
| C−    | ≥ 21/30             | ≥ 6/10        | ≥ 2/6 | ≥ 70%     |
| D+    | ≥ 20.5/30           | ≥ 5.5/10      | ≥ 1/6 | ≥ 67%     |
| D     | ≥ 19/30             | ≥ 5/10        | ≥ 1/6 | ≥ 63%     |
| D−    | ≥ 18/30             | ≥ 4.5/10      | ≥ 1/6 | ≥ 60%     |
| F     | < 18/30             | < 4.5/10      | 0/6   | < 60%     |

## Materials

### Weekly readings

Weekly readings are delivered as **interactive H5P readings on Moodle** — each combines the text with embedded comprehension questions. There is no textbook to purchase; readings are made available one week in advance.

Content is adapted from diverse sources — books, papers, and classes that I put together in previous years (referenced when adequate) —, and it is necessary to disclaim that I used some "AI copiloting" for formatting and getting ideas of examples and comprehension questions.

### Forum book

For the Forum assignments we read *Counting: How We Use Numbers to Decide What Matters* by **Deborah Stone** (Liveright, 2020). The book examines how data science practices shape — and are shaped by — political, cultural and societal values. Every forum activity will cover one chapter (6 in total).

### Supplemental references

Most of these are open-access books. None are required, but each is excellent for going deeper on specific topics:

- **[Learning Data Science](https://learningds.org/)** — Sam Lau, Joey Gonzalez, and Deb Nolan. The closest thing to a textbook for this course. Covers pandas, visualization, and modeling in Python.
- **[Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)** — Claus O. Wilke. A thorough, language-agnostic guide to making effective charts. Useful for the visualization weeks and for the final project.
- **[Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/)** — Christoph Molnar. Covers feature importance, partial dependence plots, LIME, SHAP, and more — directly relevant to Weeks 7 and 14.
- **[Fairness and Machine Learning](https://fairmlbook.org/)** — Solon Barocas, Moritz Hardt, and Arvind Narayanan. The authoritative text on fairness, bias, and accountability in ML. Directly relevant to Week 14.
- **Machine Learners: Archaeology of a Data Practice** — Adrian Mackenzie (MIT Press, 2017). A dense, critical examination of machine learning as a cultural and scientific practice, drawing on Science and Technology Studies (STS), social theory, and the humanities. Not light reading — but we will draw on some of its ideas in class discussions about how ML practices are embedded in broader cultural, social and institutional contexts.

## Policies

### Attendance

Attendance is required and directly affects your final grade — see the [grading table](#final-grade) above.

If you let me know in advance that you won't be able to make it, that absence won't count.

Life is unpredictable, though, and sometimes you'll be absent with no chance to give me a heads-up first — that's why the grading table allows for a handful of misses (around 3 or 4) and still lets you earn an A. But these should be genuine exceptions, not a pattern. If you realize that your schedule makes regular attendance impossible, the right thing to do is to register for a different section or defer the course — not to enroll and miss class repeatedly.

Why does this matter so much? This is a learning community, and that requires us to be present to each other. A lot happens in class that is not captured anywhere else: live demos, discussions, spontaneous clarifications. If you are not there, you miss it — and saying "I didn't know" is not an excuse when you were not there to hear it.


### Late work

Due dates are set as late as they responsibly can be. They exist to keep you on a learning rhythm — and experience shows that falling behind is very hard to recover from.

Submitting on time also means you receive feedback while the material is still fresh. Miss a deadline and you lose not just the submission, but the chance to see how you are doing before the next thing arrives. This matters especially for the project milestones, where each checkpoint builds on the previous one.

I review work at set times, and that review takes real effort on my part. Asking me to accept work late — and/or then regrade everything at the end — is asking me to do significantly more work because your schedule did not align with the one we agreed to at the start of the semester. I try hard to make deadlines fair and achievable; I ask you to respect them in return.

Quizzes cannot be made up except in documented exceptional circumstances, arranged in advance whenever possible.

### Academic Integrity

As the [Calvin Academic Integrity Policy](https://calvin.edu/policies/academic-integrity-policy) states, “the student-faculty relationship is based on trust and mutual respect.” That trust runs in both directions. I will assess your work honestly and invest real effort in making the grading system fair and meaningful. I ask you to engage honestly in return.

**Collaboration** is encouraged — talking through problems, comparing approaches, working side by side. What is not acceptable is submitting someone else’s words or code as your own. Even when you collaborate closely, your submission must reflect your own thinking. Acknowledge any help you receive by name.

**Do not insist or bargain for grades.** A grade is a record of what you have demonstrated, not something to negotiate after the fact. Pressuring me to change a grade without new evidence of learning is not just unhelpful; it is corrosive to the environment we are building together. I want to help you, but "bumping" your grades in dishonesty is not helping you, nor the world towards which we have a responsibility in saying the truth about your learning. Insistence is not a harmless thing, like thinking about "just ask/try, maybe it works" — it is tiresome and annoying, and it corrodes trust, mutual respect and a friendship I'd love to cultivate with you.

I really strive and pray that our community would be a place where we all grow in maturity, virtue and respect. I love to be very chill, light-hearted and joky in the way we teach and interact, but do not conclude from that that I'm not responsible or serious about education. If a serious integrity issue arises, I will involve the Office of Student Support, Accountability, and Restoration as appropriate.

### Use of LLMs

We are following [Calvin's Policy on AI](https://calvincollege.sharepoint.com/sites/CalvinOnline/SitePages/Calvin-University-Policy-on-AI.aspx?CT=1787232184454&OR=OWA-NT-Mail&CID=63229cb9-5e0b-7ac5-8697-b3014e84a9fe&SI=NonSentItems&SLSync=F).

LLMs (ChatGPT, Copilot, and similar tools) can be genuinely useful for understanding concepts, recalling syntax, and getting unstuck. What is not permitted is using them as a ghostwriter — passing a prompt, copying the output, and submitting it as your work.

This matters for three reasons. First, it is not how learning happens. Second, LLMs are frequently wrong, especially on technical details, and you will not notice if you have not understood the material yourself. Third, it shows: LLM-generated code and prose have recognizable patterns, and I will ask you to explain your work during feedback. If you cannot, that becomes part of your assessment.

If you use an LLM or any external source, record it:

- For LLM-generated code: save the prompt you used.
- For code from a website: save the URL.
- For code from a book: note the title and page.

**Big Tip**: Retype borrowed code yourself rather than copy-pasting. The act of retyping — even switching back and forth — is where the learning happens.

### Community & Belonging

This class aims to be a place where everyone is equally respected — regardless of ethnicity, gender, socioeconomic background, political views, religious background, or any other dimension of identity. That kind of environment does not happen automatically; it requires all of us. I invite your active help in building it.

Treat each other with respect in all course spaces — in class, in online forums, and in any collaboration. No personal attacks, trolling, or contemptuous language will be tolerated.

If you are feeling threatened or hurt by another student's behavior, please reach out. You can do so publicly, privately, or anonymously — by talking to me, to the department chair, or by filing a report through [Safer Spaces](https://calvin.edu/safer-spaces).

### Health & Wellness

Many things can interfere with learning: stress, anxiety, relationship difficulties, family situations, food or housing insecurity, and more. Taking care of yourself — sleep, movement, connection, rest — is not separate from your academic work. It is what makes it sustainable.

If something unavoidable comes up, reach out as soon as you can. Early communication gives us more options. If you need an accommodation or extension for a documented reason, go through Calvin Health Services or another support office to get a memo — I want to help, but I need something to work with, and I can do much more at the start of a problem than at the end of the semester.

Asking for help is a skill worth developing. The [Center for Counseling and Wellness](https://calvin.edu/center-counseling-and-wellness) supports one in five Calvin students every year and can connect you with resources on and off campus. You can also reach out to me, to another faculty or staff member, or to someone you trust. You are not alone.