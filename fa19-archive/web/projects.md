
---
title: Projects
...

There is no final exam for this course; instead, students will do two projects. Both may be done individually or in groups of 2 or 3.

## **Project 1**: replicate and critique some real-world data science

For this project you will pick some existing data science work (a blog post, report, research paper, etc.) and replicate a visual from it.

The project will explore the intersection between three things:

* The data
* The visualization
* The story that the visualization tells about the data (and, indirectly, about the world)

The three components to this project involve each of these three things:

* **Data**: Obtain some real-world dataset. Trace where it came from and how it's structured. Load it and process it using the Python data science toolkit to a form that's appropriate for making the visualization.
* **Visualization**: Replicate (re-create) a visualization that someone else already made based on that data. Evaluate some of the choices and assumptions that were made in the visualization process: in what ways does the visualization faithfully represent the data (or not)? What sort of stories does the chosen visualization amplify?
* **Story**: Consider the story that the original source told using the visualization. Is that story accurate? complete? clearly articulated? How did choices in the data collection, preparation, and visualization affect the storytelling? Are there other stories that the data might also be telling?

This project addresses our course-level learning objectives in this way:

* **Technical skills**: manipulating data with Pandas, constructing visualizations with Seaborn and Matplotlib. Creating reports using Jupyter Notebooks.
* **Communication**: analyzing choices made in visualization and text with respect to how it tells a story about data. Proposing and implementing changes to improve the clarity of communication.
* **Ethics and Critical Thinking**: identify potential ethical questions (e.g., of transparency, diversity, etc.) that emerge in the process of obtaining, manipulating, and communicating with data.

### Project 1 Milestones

Milestones are due along with the corresponding week's homework.

* **Week 2**: Propose 2 or 3 potential options that interest you, and write why you find them interesting. The course staff will help you determine what's feasible.
* **Week 3**: Pick a specific visualization to recreate and identify concrete steps towards obtaining the data.
* **Week 4**: Create a rough-draft visualization, including brief notes on how the data were obtained and story was originally told using that data. We will workshop some visualizations in class.
* **Week 5**: Provide feedback to other students.
* **Week 6**: Final visual, plus your critique of the original article and some follow-up questions.

## **Project 2**: ask and answer your own data science question

This project will require doing new work, either extending some existing work (like the first project) or starting from scratch. Results will be presented in the form of a blog post (only posted publicly if want to), supporting code, and a brief presentation to the class. Successful outcomes should include visual, analytical, and perspectival components.

The final course meeting (during the designated final exam period on December 12) will be devoted to final project presentations. Feedback on others' projects will be part of your final project grade, so attendance is mandatory.

### Project 2 Milestones

(Revised milestone schedule posted on the [calendar](calendar.html).)

* **Week 7**: Draft of a project proposal including specific questions
* **Week 8**: Revised project proposal
* **Week 10**: Dataset and exploratory visualization done
* **Week 12**: Initial modeling and visualization
* **Week 15**: Final presentation

### Project 2 Detailed Expectations

**NOTES**:

* In all of the following analyses, you will likely need to make some choices regarding what variables to include, whether to do some pre-processing (e.g., addressing missing values, generating new variables), etc. Clearly state which decisions you made, explain why you made them and what might have been alternative choices. 
* If you use any code from the internet, you should acknowledge its source and provide a link.
* You should submit all of the code needed to replicate your results, but **your report should be understandable without looking at the code**.

Your report should include the following elements:

* A succinct but descriptive **title**
* **Question**(s)
  * A **real-world question** that you'd like to explore, and *why* it's interesting. (This question should be stated in language that is understandable to someone who hasn't studied data science and doesn't know the details of your dataset.)
  * A **modeling question** for which you'll use regression, classification, or some other kind of modeling. (This question should be stated in more specific technical terms and reference the particular features of your dataset.) This question ideally helps answer the real-world question, but it's okay if it doesn't.
  * An analysis of the **appropriateness of your dataset** for addressing these questions.
* **Dataset**
  * A brief (2-4 sentences) verbal description of the dataset: what is the dataset about?
  * A description of its *provenance*: where did the data come from originally? Where did you download it from? And (as much as you can tell or speculate) how did it end up available there?
  * The number of records in the dataset, and what each one represents
  * A list of the features in the dataset and their [types](https://www.textbook.ds100.org/ch/04/eda_data_types.html)
* **Exploratory Data Analysis**
  * Show plots illustrating the distribution of at least 4 variables in your dataset. Comment on anything interesting you observe.
  * Show plots illustrating bivariate relationships for at least 2 pairs of variables. Explain what you observe (e.g., positive/negative correlation, no correlation, etc.).
* **Modeling**
  * Clearly state what is the target variable you are trying to predict, which variables (features) you are using to predict it, and why you chose those features.
  * Fit a basic predictive model using one of the techniques we discussed in class (*regression*: Nearest Neighbors or Linear Regression, *classification*: Nearest Neighbors or Logistic Regression; other choices such as Decision Trees are also fine)
  * Report the results of your basic predictive model on held-out data or via cross-validation.
  * Make one or more changes to the predictive model to improve the accuracy. Discuss what changes you made, why you made them, and what the results were.
  * **Alternative**: instead of a supervised prediction task, you can define an unsupervised learning task and use clustering. In this case, clearly state what you want to understand through the clustering, and report your observations.
* **Findings**: Summarize the analyses you performed and what the results told you. What do your findings say about the real-world and prediction (or clustering) questions you posed?
* **Limitations**: What are some limitations of your analyses and potential biases of the data you used? 
* **Future Directions**: What new questions came up following your exploration of this data? Describe at least one question that could not be answered using your data alone, and specify what additional data you would collect to address it.

(Project descriptions thanks to [Ofra Amir](https://scholar.harvard.edu/oamir/home))

#### Connection to Learning Objectives

Projects should demonstrate proficiency in the primary learning outcomes of this course:

| Learning outcome | Evidence in project |
| ---- | ----- |
| **Formulate** a question or problem that can be answered by data | Includes a statement of the goal of the project that clearly shows what a successful outcome looks like (e.g., how does the work answer the question? Did the work achieve the goal?) |
| **Acquire** data responsibly | Describes where the data came from and evaluates the suitability of that source for that data |
| **Transform** data faithfully into usable forms | Includes some data wrangling (merging multiple data sources, aggregating, re-coding data, identifying and dealing with missing data, etc.) |
| **Explore** datasets to interrogate their representativeness, build intuition, and generate hypotheses | Includes results of exploratory analytics about data values, completeness, etc. (e.g., exploratory visualizations and/or descriptive statistics); includes some reflection on how the actually available data shaped the project goal / question |
| **Apply** predictive tools to draw conclusions, evaluating the suitability of these models | Includes a predictive model (regression or classification) that uses two or more features to predict an outcome. Includes a discussion of how modeling decisions were made and on how accurate the model should be on unseen (e.g., future) data, based on quantitative evidence (e.g., cross-validation). |
| **Communicate** visual and textual data-driven narratives that are useful, faithful, and intelligible to both technical and non-technical audiences | Includes a blog post and a brief presentation |
| **Analyze** considerations of responsibility and justice in all of the above practices | Demonstrates humility and awareness throughout the project, e.g., includes appropriate caveats with claims, includes discussion of implications of decisions that were made during acquisition / modeling / communication. Identifies potential ethical issues raised by existing data. |
