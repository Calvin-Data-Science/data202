# HW1

**Before you begin**, please fill out [this form](https://docs.google.com/forms/d/e/1FAIpQLSeMuh5YkZucF1uw5R6qtDBHF8hyY3yMkp-vfrWYxSLETxfzuQ/viewform?usp=sf_link).

## Preliminaries

You'll be submitting two files: a PDF of your answers to Part 1, and a Jupyter Notebook file for your answers to Part 2 and beyond.

The two main parts are equally weighted.

## Part 1: Notice Data

Pick four organizations that use data:

- Two **online** (websites, apps, etc. -- where the your primary interaction with them is digital)
- Two **off-line** (stores, governmental organizations, religious organizations, etc. -- where your primary interaction is in person)

For each, answer the following questions:

- What data are they collecting about you?
  - each record is a... (e.g., page load, video played, comment submitted, ...): ___
  - some of the fields in that record might be...: ___
  - (optional) How do you feel about them collecting that data?
- What is one decision that the organization is probably making based on that data?
  - Be specific: if it's deciding between two things, give an example of what those things might be. If it's deciding how much of something, or when to do something, specify what those things might be. etc.
  - Why might that decision matter for their goals?
  - (optional) How do you feel about them making those decisions?

Finally, answer those same two questions (data collected, decision made) for **one example for each of the following**:

1. the data is being collected about people not like the typical DATA 202 student
2. data-driven decisions are being made that affect the lives of people not like the typical DATA 202 student.

Notes:

- You're welcome to share ideas of sites and organizations on Piazza. Let's try to get a diverse set of examples from the class!
- The lines between online and offline are blurry; don't fret about that. The point is just to get a diverse set of examples.

## Part 2: Practice with Data

### Acquire Data

Find and download **two*- different *tabular* datasets about a topic remotely interesting to you. For each of them, answer these questions:

- What specific instructions could someone else follow to obtain exactly the same file(s) as you got? Did you have to go through any hoops (like creating an account)?
- What file format is it in?
- How big is it?

Example: *I found the data by searching for "`___`" in the list at `____`. The dataset's main URL is `___`. I downloaded `http://___` and got a 15 MB Zip file containing a 40 MB CSV that has a SHA1 hash of `____`. The website says there should be 140,185 records, so that would mean the average record is 40000000/140185=285 bytes.*

Also answer the following, to the extent that the dataset tells you. Many datasets *don't* specify some of these things; if it doesn't specify, briefly describe why that question might matter for this dataset.

- **Provenance**: How did the data get to you? specifically:
  - How was it collected? By whom? Under what circumstances?
  - What processing (filtering, transformation, etc.) was done to get it in the form you now have?
  - What different people or organizations did it go through?
- **License**: What permissions do you have to use it? Is there anything the authors explicitly allow or disallow you to do with it?

Some places you might start looking for data will be posted on Piazza. Please add more!

### Explore Data

For each dataset:

- Write code to load the data using Pandas (e.g., `pd.read_csv`)
- Write code to show how many records are in the dataset.
- Write code to show how many columns the data has and what they are.
- Pick two or three columns and do the following (try to pick columns with a variety of types so you get practice):
  - Report a few representative examples of specific values from that column.
  - If it's a numerical column, report its range and a meaningful measure of central tendency (arithmetic mean, median, mode, etc.). Plot a histogram of the values.
  - If it's a categorical column, report a few of its most common values and how prevalent they are. (Are there some values that are probably the same thing but written down differently?)
  - Do you notice any missing values?
  - Based on your findings, describe what you think the data in the column means, in the language of the real world, with units if applicable, and how you came to that conclusion (e.g., "The documentation didn't say, but I'd guess that the `age` column gives the patient's age (though perhaps it could be the medical device's age??). I'd guess it would be in years, but there are some negative numbers above 150 so maybe some of the dates are in months or days. About 2% of the numbers are negative; they might represent missing data.")
- Based on your exploration, what are two questions that would be easy to answer about this data? What are two questions that would be possible to answer with this data if it were reorganized, joined with another dataset, or otherwise transformed? What are two questions about this topic that this dataset can't answer?
- In what ways might this dataset not be representative? You might consider:
  - Are there kinds of records that are missing from this dataset? (Just state what kind of record you'd look for; don't worry about checking whether there may in fact be a record like it.)
  - Are there certain kinds of records that might be under- or over-represented in this dataset? (e.g., Joy Buolamwini pointed out that "pale males" were over-represented in some face datasets.) Again, don't worry about checking the dataset to see if it's actually representative.
  - Are there ways that the data are coded that might be exclusionary or reflect cultural assumptions?

### Compare and Contrast

Now, compare and contrast the two datasets along the following axes:

- Distribution (ease of finding/acquisition, file type, etc.)
- Documentation (provenance information, licensing clarity, ease of understanding what the columns mean)
- Size (file size, record count, etc.)
- Representation (column count, consistency, missing data, etc.)
- Representativeness

## For fun

What was your favorite first day of class this semester (or ever)?

## Submitting

Also write down (a) how long this assignment actually took you and (b) which part actually took you the longest.
Submit the resulting `.ipynb` file on Moodle.
