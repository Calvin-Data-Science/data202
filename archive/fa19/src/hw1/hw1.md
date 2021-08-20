# HW1

**Before you begin**, please fill out [this form](https://docs.google.com/forms/d/e/1FAIpQLSeMuh5YkZucF1uw5R6qtDBHF8hyY3yMkp-vfrWYxSLETxfzuQ/viewform?usp=sf_link).

## Preliminaries

You'll be submitting two files: a PDF of your answers to Part 1, and a Jupyter Notebook file for your answers to Part 2 and beyond.

The two main parts are equally weighted.

## Part 1: Notice Data

**Objective**: This exercise should help you expand your thinking about *who* uses *what kind* of data for *what purpose*. It may also:

- Grow your skills and habits of awareness to notice situations in which data might be collected or used
- Help you see opportunities to collect or use new kinds of data

**Exercise 1.1**: Pick four organizations that use data:

- Two **online** (websites, apps, etc. -- where the your primary interaction with them is digital)
- Two **off-line** (stores, governmental organizations, religious organizations, etc. -- where your primary interaction is in person)

For each, answer the following questions (concise, bullet points):

1. **What data are they collecting about you?** Your answer should include:

    - What each datum represents (e.g., page load, video played, comment submitted, ...)
    - A few of the fields that might be in that record (e.g., user id, video id, time, ...)
    - (optional) How do you feel about them collecting that data?

2. **What is one decision that the organization is probably making based on that data?**

    - Be specific: if it's deciding between two things, give an example of what those things might be. If it's deciding how much of something, or when to do something, specify what those things might be. etc.
    - Connect this to your answer to the first question: how might the specific fields of data help them answer this question? e.g., "Since YouTube collects who watches which videos, they can recommend videos to me based on how the videos I watched overlap with the videos that other people have watched."
    - Why might that decision matter for their goals? (e.g., "If YouTube makes better recommendations, I watch more videos, so they can show me more ads.")
    - (optional) How do you feel about them making those decisions?

**Exercise 1.2**: Notice how the questions above were about how organizations collect and use data about **you** (or people like you). Now, try to go beyond yourself: think about how data is being *collected* about people who aren't like you. **Answer question 1 above, replacing "you" with a type of person other than yourself** (or, if you prefer, unlike the typical DATA 202 student). For example, [Google was recently fined for collecting and using data about children](https://www.nytimes.com/2019/09/04/technology/google-youtube-fine-ftc.html); if you were to use that example, "you" would become "children". **Do this for one organization** (may be one of the ones you used above, or something different.)

**Exercise 1.3**: Again, going beyond yourself, **answer question 2** for a situation where that decision affects the lives of people unlike yourself (or, if you prefer, unlike the typical DATA 202 student). Again, you only need to do this for one organization / decision; it could be the same as in Ex 1.2 if you like.

Notes:

- You should end up with a total of 5 answers to question 1 (data collection) and 5 answers to question 2 (data-driven decisions).
- You're welcome to share ideas of sites and organizations on Piazza. Let's try to get a diverse set of examples from the class!
- The lines between online and offline are blurry; don't fret about that. The point is just to get a diverse set of examples.
- Exercises 1.2 and 1.3 will probably be challenging. Part of the goal is to notice how hard it is to notice how data affects the lives of people unlike ourselves, and hopefully give us some humility when making decisions about collecting and using data.

## Part 2: Practice with Data

### Objectives

This exercise should help you get your feet wet using Pandas, a key part of the typical Python data science toolkit. It may also:

- Give you awareness of what kinds of datasets are easy and hard to get publicly, and where you might look for them
- Get you frustrated enough about the lack of documentation in many datasets that you'll demand better and do better
- Give you some practice thinking critically about the ways in which datasets might be biased.

### Exercise 2.1: Acquire Data

Find and download **two*- different *tabular* datasets about a topic remotely interesting to you. **For each dataset you downloaded**, answer these questions:

- What specific instructions could someone else follow to obtain exactly the same file(s) as you got? Did you have to go through any hoops (like creating an account)?
- What file format is it in?
- How big is it?

A sentence or two will suffice, for example: *I found the data by searching for "`___`" in the list at `____`. The dataset's main URL is `___`. I downloaded `http://___` and got a 15 MB Zip file containing a 40 MB CSV that has a SHA1 hash of `____`. The website says there should be 140,185 records.*

Also answer the following, to the extent that the dataset tells you. Many datasets *don't* specify some of these things; if it doesn't specify, briefly describe why that question might matter for this dataset.

- **Provenance**: How did the data get to you? specifically:
  - How was it collected? By whom? Under what circumstances?
  - What processing (filtering, transformation, etc.) was done to get it in the form you now have?
  - What different people or organizations did it go through?
- **License**: What permissions do you have to use it? Is there anything the authors explicitly allow or disallow you to do with it?

Some places you might start looking for data will be posted on Piazza. Please add more!

### 2.2: Explore Data

For each dataset:

- Write code to load the data using Pandas (e.g., `pd.read_csv`)
- Write code to show how many rows are in the dataset.
- Write code to show how many columns the data has and what their names are.
- Pick two or three columns and do the following (try to pick columns with a variety of types so you get practice):
  - Report a few representative examples of specific values from that column.
  - If it's a numerical column, report its range and a meaningful measure of central tendency (arithmetic mean, median, mode, etc.). Plot a histogram of the values (using `plt.hist` or `sns.distplot`)
  - If it's a categorical column, report a few of its most common values and how prevalent they are. (Are there some values that are probably the same thing but written down differently?)
  - Based on your findings, describe what you think the data in the column means, in the language of the real world, with units if applicable, and how you came to that conclusion (e.g., "The documentation didn't say, but I'd guess that the `age` column gives the patient's age (though perhaps it could be the medical device's age??). I'd guess it would be in years, but there are some negative numbers above 150 so maybe some of the dates are in months or days. About 2% of the numbers are negative; they might represent missing data.")
- Based on your exploration, what are two questions that would be easy to answer about this data? What are two questions that would be possible to answer with this data if it were reorganized, joined with another dataset, or otherwise transformed? What are two questions about this topic that this dataset can't answer?
- In what ways might this dataset not be representative? You might consider:
  - Are there kinds of records that are missing from this dataset? (Just state what kind of record you'd look for; don't worry about checking whether there may in fact be a record like it.)
  - Are there certain kinds of records that might be under- or over-represented in this dataset? (e.g., Joy Buolamwini pointed out that "pale males" were over-represented in some face datasets.) Again, don't worry about checking the dataset to see if it's actually representative.
  - Are there ways that the data are coded that might be exclusionary or reflect cultural assumptions?

Repeat this exercise for your other dataset. Don't bother about making reusable or pretty code; just use the functions already provided by Pandas / Matplotlib / Seaborn.

### Compare and Contrast

Now, compare and contrast the two datasets along the following axes:

- Distribution (ease of finding/acquisition, file type, etc.)
- Documentation (provenance information, licensing clarity, ease of understanding what the columns mean)
- Size (file size, record count, etc.)
- How the data is represented (column count, consistency, etc.)
- Representativeness / bias

## For fun

What was your favorite first day of class this semester (or ever)?

## Reflection

Write down (a) how long this assignment actually took you and (b) which part actually took you the longest.
