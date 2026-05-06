---
layout: week
title: "Week 1: Introduction to Machine Learning"
week_number: 1
---

# What Is Machine Learning?

## From Rules to Learning

Traditional computer programs follow explicit instructions written by a programmer. If you wanted software to detect spam emails in 2000, you might write rules like: *"If the message contains the word 'free' and comes from an unknown sender, mark it as spam."* This works — until spammers change their language. You would have to update your rules constantly.

Machine learning takes a different approach. Instead of writing the rules yourself, you collect **labeled examples** — thousands of emails that humans have already sorted into "spam" and "not spam" — and let the program figure out the patterns on its own. Tom Mitchell's classic definition captures this:

> *"A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks T, as measured by P, improves with experience E."*

In the spam example, the task T is classifying emails, the experience E is the labeled dataset, and P is accuracy on new, unseen emails.

---

## Traditional Programming vs. Machine Learning

The table below summarizes the key difference in mindset:

| Traditional Programming | Machine Learning |
|---|---|
| Rules + Data → Output | Data + Output → Rules |
| You write the logic | The model learns the logic |
| Breaks when the world changes | Can be retrained on new data |

This shift has made machine learning the dominant approach for problems where writing explicit rules is impractical — recognizing faces, understanding speech, recommending content, or detecting fraud.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**Which statement best describes how machine learning differs from traditional programming?**

- [ ] Machine learning requires programmers to write more detailed rules.
- [x] In machine learning, the model learns rules from data rather than following rules written by a programmer.
- [ ] Traditional programming relies on large datasets, while machine learning uses hand-crafted rules.
- [ ] Machine learning can only be applied to text-based problems.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: false
-->

Once a machine learning model is trained and deployed, it does not need further monitoring because it automatically adapts to changes in the real world.

<!-- END QUESTION -->

# Three Flavors and the Workflow

## Three Flavors of Machine Learning

Not all ML problems look the same. Researchers typically organize them into three broad categories:

**Supervised learning** is the most common type. You provide a dataset where every example has an input and a known correct answer — called a *label*. The model learns a function that maps inputs to outputs. Examples: predicting house prices, detecting tumors in MRI scans, or classifying emails as spam or not-spam.

**Unsupervised learning** works with data that has no labels. The algorithm must find structure on its own. Clustering algorithms, for example, group similar customers together without being told in advance what the groups should be. Unsupervised learning is useful for exploration — you do not always know what patterns exist in your data.

**Reinforcement learning** is inspired by how animals learn through trial and error. An *agent* takes actions in an *environment* and receives *rewards* or *penalties*. Over time, it learns a *policy* — a strategy for acting that maximizes cumulative reward. This is how AlphaGo mastered the game of Go and how robots learn to walk.

---

## The Machine Learning Workflow

A data scientist working on an ML project typically moves through these stages:

**1. Frame the problem.** What exactly are you trying to predict or decide? What does success look like? Who will use this system, and how?

**2. Collect and explore the data.** Machine learning depends entirely on data. You need to understand its shape: How many examples do you have? Are there missing values? Does it reflect the real world, or does it carry historical biases?

**3. Prepare features.** Raw data is rarely ready to feed into a model. Feature engineering — transforming raw inputs into informative numerical representations — can be the most time-consuming and impactful step.

**4. Choose and train a model.** Select an algorithm appropriate to your task, fit it to your training data, and tune its *hyperparameters*.

**5. Evaluate and iterate.** Measure performance on data the model has never seen. Is it accurate enough? Does it fail in systematic ways? Iterate on all prior steps as needed.

**6. Deploy and monitor.** Shipping a model to production is only the beginning. Data distributions shift over time, and a model that was accurate last year may degrade silently.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

Complete the following sentences.

In **[supervised]** learning, every training example has a known correct answer called a **[label]**. By contrast, **[unsupervised]** learning finds structure in data that has no labels. A third paradigm, **[reinforcement]** learning, trains an agent by giving it **[rewards]** or penalties based on the actions it takes.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each gap to describe the ML workflow.

You start by *[framing]* the problem and defining success. Next you *[collect]* and explore data, checking for biases. Then you engineer *[features]* from raw inputs before selecting a model. After training, you *[evaluate]* the model on held-out data. Once deployed, you must *[monitor]* it because real-world data distributions shift over time.

<!-- END QUESTION -->

# A Critical Lens

## Machine Learning Is Not Neutral

Machine learning is powerful, but it is not objective. Every dataset reflects the world that produced it — including its inequities. When a hiring algorithm trained on historical data learns to deprioritize resumes from certain demographic groups, it is not making a mistake; it is doing exactly what it was trained to do. The mistake happened earlier: in deciding to train on biased data, or in failing to audit the output.

Consider a few well-documented examples:

- A recidivism prediction tool used in US courts was found to be twice as likely to falsely flag Black defendants as high-risk compared to white defendants.
- Facial recognition systems trained mostly on lighter-skinned faces perform significantly worse on darker-skinned faces.
- Recommendation algorithms can amplify extreme content because engagement — not truth or wellbeing — is what is being optimized.

---

## Asking the Right Questions

Technical skill alone is not enough. As you build ML systems, keep asking:

- **Who benefits** from this model, and who might be harmed?
- **What is being optimized?** Accuracy on average can hide failure for specific groups.
- **Where did the data come from?** Historical data encodes historical power structures.
- **Who was not in the room** when this system was designed?

These are not just ethical add-ons — they are engineering requirements. A model that performs well on average but systematically fails for a minority group is not a good model.

---

<!-- QUESTION:true-false
answer: false
-->

Machine learning models are inherently objective and free from bias because they learn patterns directly from data rather than from human-written rules.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term to complete each critical observation about ML systems.

A recidivism tool was found to produce *[biased]* predictions that harmed specific demographic groups. Facial recognition systems trained on *[unrepresentative]* data perform poorly on underrepresented faces. Recommendation algorithms that optimize for *[engagement]* can amplify harmful content. Auditing model outputs for *[fairness]* across groups is an engineering requirement, not an optional extra.

<!-- END QUESTION -->
