---
layout: slides
title: "Week 1: Introduction"
---

# Introduction to Machine Learning

### DATA 202 · Week 1 · Calvin University

---

> Dear Heavenly Father,
> As we gather here today to embark on a new journey of learning, we invite Your presence into this classroom. Bless each student with wisdom, understanding, and a thirst for knowledge. Let Your light shine upon us, illuminating the path of learning, so we may contemplate your beauty and love in everything you made.
>
> May this classroom be a place of respect, fellowship, and growth. Guide our imaginations and desires towards your love and justice, so that we may respond adequately to your call to be Christ's agents of renewal in the world.
>
> Through our Lord Jesus Christ, Amen.

---

## Data Science?

"Using data to search for **meaningfulness** in creation."

- **Describe** — what is the world like? *(What fraction of loan applicants default?)*
- **Relate** — what factors are associated? *(What predicts default?)*
- **Infer / predict** — can we generalize? *(Will this applicant repay?)*

---

## Machine Learning?

- We then use these meaningful patterns in order to act.
  - Machine learning is apprehending the patterns and acting from them.

> "A computer program is said to learn from **experience E** with respect to some class of **tasks T** and **performance measure P**, if its performance at tasks T, as measured by P, improves with experience E."
> — Tom Mitchell, *Machine Learning* (1997)

- **Task (T):** what the program does — classify an email, predict a price, detect fraud
- **Experience (E):** the data it learns from — labeled examples, past transactions
- **Performance (P):** how we measure success — accuracy, error rate, F1 score

---

## Three Kinds of Machine Learning

**Supervised learning** — answering a question (classification, estimation, prediction) based on past experiences
- Spam detection, image classification, loan default prediction

**Unsupervised learning** — just find structure in data (no pre-given answer)
- Customer segmentation, anomaly detection, topic modeling

**Reinforcement learning** — elaborate a way of acting given previous rewards or penalties
- Game-playing AI, robot navigation, recommendation systems

---

## Traditional Programming vs. Machine Learning

| Traditional Programming | Machine Learning |
|---|---|
| Rules + Data → Output | Data + Output → Rules |
| We write the logic | The model *learns* the logic |
| Brittle to new situations | Generalizes (if trained well) |

---

## Why data?

Data is one way we record experience and make it shareable.

- **Explicit** — written down, not just in someone's head
- **Accessible** — can be examined, questioned, passed on
- **Scalable** — machines can process millions of records

---

## But data are limited

- **Imprecise** — the same word means different things to different people
- **Ambiguous** — context changes meaning
- **Biased** — only captures some populations, some moments
- **Distorted** — recording errors, format changes, transmission loss
- **Stale** — things change; old data may not reflect today

*A model trained on bad data learns bad patterns.*

---

## Types of data

- Numerical
- Categorical
- Time-series
- Event / duration / survival
- Text
- Image
- Video
- Geospatial

---

## Structures and databases

- Tables
- Spreadsheets (Excel, etc.)
- Dataframes (pandas)
- SQL databases
- Hierarchical (XML, JSON, YAML)
- Graphs (networkx, Neo4j)
- And many others...

---

## Application Areas

- <span style="color:green">Natural Sciences🔬</span>
- <span style="color:olive">Humanities🏛️</span>
- <span style="color:red">Health🩺</span>
- <span style="color:brown">Law & Policy⚖️</span>
- <span style="color:orange">Business📈</span>
- <span style="color:blue">Industry🏭</span>
- <span style="color:purple">Art, Sports & Entertainment🎭</span>

---

## Why programming?

- Why not just Excel?
  - Indeed, it can be useful for simple tasks.
  
- However, Python/R are...
	- more reproducible
	- more scalable
	- easier to automate
	- more analytics libraries
	- more visualization libraries
	- more integration with other tools
	- large community and ecosystem
	- open-source and free to use
	- actually HAS MACHINE LEARNING libraries
	- although: harder to learn and use

---

## Python or R?

| **Criteria**              | **Python**                                                        | **R**                                                           |
|---------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------|
| **Community and Support**  | Large and growing community, with extensive resources and tutorials available. Popular in industry and academia. | Strong community in academia, especially in fields like statistics, bioinformatics, and social sciences. |
| **Ease of Learning**      | Easier for beginners, especially with programming experience.    | Steeper learning curve, particularly for those new to programming. |
| **Data Visualization**     | Strong, with libraries like Matplotlib, Seaborn, Plotly, and Bokeh. Interactive visualizations are well-supported. | Excellent, with ggplot2 being one of the most powerful visualization libraries. However, interactive visualizations are less integrated. |
| **Machine Learning**       | Extensive support with libraries like scikit-learn, TensorFlow, and PyTorch. Broad adoption in industry. | Adequate support for machine learning, though Python libraries are more robust and widely used in industry. |
| **Statistical Analysis**   | Good for general-purpose analysis; extensive libraries, though more basic for advanced statistical techniques. | Excellent for complex statistical analysis; originally designed for statisticians and excels in this area. |
| **Integration and Flexibility** | Highly flexible, integrates well with other languages and systems (e.g., C, C++, Java, SQL). Versatile for many tasks beyond data science. | Primarily focused on statistical computing, less flexible for other types of programming or integration with non-statistical systems. |
| **Performance and Scalability** | Generally faster for large datasets, especially with optimized libraries (e.g., NumPy, Dask). Better for large-scale production environments. | Can be slower with large datasets, though packages like data.table improve performance. Not as well-suited for big data as Python. |
| **Deployment**             | Strong tools for deploying models in production (e.g., Flask, FastAPI, Streamlit). Easy to integrate with web services and databases. | More challenging to deploy in production; Shiny can be used for web applications but is less flexible than Python tools. |

---

## Libraries

- **Data manipulation and analysis**: [pandas](https://pandas.pydata.org/)
  - Alternatives: [Ibis](https://ibis-project.org/), [Polars](https://pola.rs/), [Dask](https://www.dask.org/)
- **Visualization**: [plotly](https://plotly.com/)
  - Alternatives: [matplotlib](https://matplotlib.org/), [seaborn](https://seaborn.pydata.org/), [altair](https://altair-viz.github.io/)
- **Modeling and machine learning**: [Scikit-learn](https://scikit-learn.org/stable/)
  - Alternatives: [TensorFlow](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/), [XGBoost](https://github.com/dmlc/xgboost)

---

## Communication and publishing platforms

- Jupyter Notebooks in JupyterLab (we'll be using those)
- Other useful publishing platforms: [Streamlit](https://streamlit.io/) and [Shiny](https://shiny.posit.co/)

---

## This Course Is Not Just Technical

Skills, knowledge, and *dispositions* — all three need to be developed.

A disposition is a **habit of using skills wisely** — formed only in community, through practice.

---

## Curiosity

Thomas Aquinas distinguishes *studiositas* (virtue) from *curiositas* (vice).

Some failure modes:
- **Arrogance** — seeking knowledge we have no right to act on
- **Superficiality** — satisfied with the surface, skipping the hard part
- **Possessiveness** — delighting in knowing, not in what is known
- **Impertinence** — claiming more certainty than the data supports

We will practice: *noticing and reporting our decisions, acknowledging limitations, validating results.*

---

## Integrity

It is tempting to massage data, cherry-pick results, or report conclusions you wanted rather than found.

We will practice:
- Evaluating claims others make with data
- Clearly articulating our analysis decisions and rationale
- Reproducibility — code and data that others can re-run

---

## Hospitality & Justice

We can use our tools to illuminate — or to obscure.

Data science can **cause harm** and **reveal it**.

We will practice:
- Clear visual communication
- Studying examples of how data causes harm
- Studying examples of how harm is mitigated or revealed

---

## What We Will NOT Cover (this semester)

- Neural networks and deep learning
- Natural language processing (NLP) - transformers, word embeddings, etc
- Optimization algorithms (gradient descent, bayesian, genetic)
- Other linear methods (SVMs, polynomial regression, LDA, GLMs, GAMs)
- Multiclass classification
- Semi-supervised learning
- Active learning
- Reinforcement learning
- Causal models (SEM, SCM, etc)
- Probabilistic graphical models (Bayesian networks, Markov models)
- Lots of other unsupervised methods (association rule learning, autoencoders, SOMs)

---

## This Week

- **Mon (today):** Course introduction — what is ML, tools, dispositions
- **Wed:** Python review — hands-on notebook
- **Fri:** DataFrame basics — loading, accessing, filtering, modifying data

No practice or quiz this week.

**Complete before next Monday:**
- Read the syllabus
- Get the book (*Counting* — Deborah Stone)
- Set up your environment — log in to Coder or install Jupyter locally (see [Resources](../../resources/))
- Complete Moodle Reading 1