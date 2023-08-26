---
title: "Forum and Moodle"
author: "K Arnold"
output: html_document
---

# Before First Week

Welcome to DATA 202!

We'll be meeting in our classroom space, NH 253, on Monday and Wednesday. (We'll be in the Maroon lab, SB 372, most Fridays.) If you have a laptop, bring it with you.

If you want to get a head start, you can: 

1. Read through the [Syllabus](https://calvin-data-science.github.io/data202/).
2. Start working on Reading 1 on Moodle.
3. See the links on Moodle to try logging into RStudio. (What are those? Come to class!)

Please email/Teams us any questions you may have. We're excited to be embarking on this data science journey with all of you this semester.

See you Monday!\
Prof. Arnold



# Final Presentation Notes

Good work to those who presented today! Here are a few things that came up for several presentations, so I thought I'd share them with the whole class:

- What does each row of the data represent?
- If you're doing predictive modeling, be very clear about what your *task* is:
  "I'm trying to predict the XXX of each YYY based on measures of ZZZ".
- Make your plots and tables *human-friendly*:
  - Label plots with meaningful names (vs, say, "model1")
  - Show only the important stuff (vs, say, every single column of your data including ones you're not using)
  - `knitr::kable` your tables
  - Consider using `comment = ""` as a chunk option. e.g., my `setup` chunk often contains `knitr::opts_chunk$set(echo = TRUE, comment = "")`
  - Show stuff in inline code. *For an example of how to do this for model accuracy, search for `model1_accuracy_estimate` in [Exercise 10](https://cs.calvin.edu/courses/data/202/21fa/ex/ex10/ex10-validation-inst.html).
- Do your data wrangling *once*, especially *before* splitting into train and test, so that the only difference between the datasets is which rows are included in which one.
- The projector in the classroom is 4x3, so "wide" presentations will run off the edge of the screen.

Meeting in the classroom worked well today, so let's do that again tomorrow. Even those who presented today are also welcome tomorrow; there's enough room.


# Unit 13

Last week of class!

Regarding the second midterm exam: instead of holding it in class, it'll be a [wrap-up homework](https://cs.calvin.edu/courses/data/202/21fa/hw/hwFinal/hwFinal-inst.html). Officially it'll be due on Reading Recess, but extensions will be freely granted.  Given the short time, I tried to keep it small.
(Why? We didn't get enough quiz/homework practice on the material in the second half to make me comfortable giving a high-stakes exam on it.
This is a bug with how I scheduled things this year.)

We'll be in the classroom both days this week:

- Monday we'll discuss communication and reporting.
- Come to class on Wednesday ready to reflect on all our Discussions this semester. So you should have Discussion 12 done by then. We'll also take a few minutes to do course evaluations.

As I mentioned in class, I'm expecting that most project teams will want to meet with me at least once for some reason or another. In anticipation of that,
I am not holding regular office hours this week; just message me and we'll find a time.

See you in class!

# Unit 12

We're approaching the end, folks! Although our main focus will be final projects,
we'll be taking the last 5(!) days of class to discuss some additional useful
topics to round out your data science expertise, including geospatial data,
text data, and more data science ethics.

Logistics:

- I have created team repos for your final projects.
  - Find your team's repo by going to our [class GitHub organization](https://github.com/Calvin-DS202-21FA) and finding the `proj-` repo with your name on it.
  - Each person on the team has read/write access to the repo.
  - If the team membership is incorrect in any way, please let me know ASAP.
  - You can each make your own clones of the repo, or you can "Share Project" for a "Google Docs" collaborative editing experience. See the [project sharing documentation](https://support.rstudio.com/hc/en-us/articles/211659737-Sharing-Projects-in-RStudio-Workbench-RStudio-Server-Pro) for details.
  - Remember to knit-commit-push often, whether you're using separate clones or a shared project. If you're using a shared project, acknowledge who did what work in the commit message.
- Please submit your milestones under the Final Project assignment in Moodle.
  - You should be able to update the submission as you progress.
  - Only one person from each team needs to submit; Moodle is configured so that everyone on a team shares that assignment.
  - Select "Knit to PDF" to make a PDF for submission (normally knitting will make just an HTML document, which is faster but doesn't show up well in Moodle).
- The next milestone is to have some exploratory visualizations and analyses of your data. That is, you should have the EDA section of your report complete, and a good start on everything before that. See the suggested report outline in the [project spec](https://cs.calvin.edu/courses/data/202/21fa/projects.html#Project_2_Detailed_Expectations) for details.
- Discussion 12, on recommendation systems, is due Tuesday. The readings there could be fodder for family discussions. (Sorry I didn't remind you about this before Thanksgiving.)
- If you didn't get to Prep 12 last week, this would be a good time: we're reading about [SQL](https://mdsr-book.github.io/mdsr2e/ch-sql.html), [Geospatial](https://mdsr-book.github.io/mdsr2e/ch-spatial.html), and [Text](https://mdsr-book.github.io/mdsr2e/ch-text.html). This could also be a good time to skim any of the other chapters that we haven't covered. In particular, check out [chapter 14](https://mdsr-book.github.io/mdsr2e/ch-vizIII.html) for some tools that may be useful for your project.

Finally: as much as we may want Covid to be over, it isn't. Especially in Michigan.
Here's [some plots](https://covidactnow.org/us/michigan-mi/county/kent_county/?s=26051513),
although note that there are some [artifacts with moving averages around holidays](https://www.nytimes.com/interactive/2021/11/22/us/covid-data-holiday-averages.html).
So: this is the time to **wear masks like it matters** and maybe even keep some distance,
even if you're vaccinated, until this surge abates.


# Week 9: Modeling and Ethics

- Read MDSR chapter 8, [Ethics](https://mdsr-book.github.io/mdsr2e/ch-ethics.html).
  - Note: The discussion there is secular and left-leaning.
  - As you read, try to identify at least one point of *resonance* with a Reformed Christian perspective, and at least one point of *tension*.
- Finish working through the Google "[attacking discrimination](http://research.google.com/bigpicture/attacking-discrimination-in-ml/)" example that we started in class.
  - Note that this whole scenario requires knowing something that is not knowable: the distinction between light and dark grey people.
  - Explain each of the objectives in your own words. For each one, identify *who* would prefer that objective. For example, a big bank might prefer the "max profit" objective because they're legally required to make decisions to maximize value to their shareholders. Who might prefer "group unaware"? "Demographic parity"? "Equal opportunity"?
  - Which of the objectives do you think is most "right"?

# Week 7: Modeling intro, vis replication project

This week we start modeling, which is what some people consider the coolest and most useful part of data science. Some people even go so far as to call it “AI”.

- *Reminder*: the coding (online) part of Midterm 1 closes on Wednesday night.
- I just posted the templates for Project Milestone 2. If you've been working on it somewhere else, please move your work into the appropriate place in the template. It's mainly there to help you follow the suggested [report outline](https://cs.calvin.edu/courses/data/202/21fa/projects.html#Report_Outline) and to have everyone's stuff in one place.
- Target date for Milestone 2 is this Friday, but again it's okay if that has to slip by a few days.
- Plan to drop by the STEM Division Summer Research Poster Fair on Friday, October 22 from 12:30-3:30 pm in the Science Complex. The discussion post this week will be about plots you see there. See the Forum for details and pointers about how to do this respectfully. I'll try to make our exercise on Friday shorter so that you can swing by at the end of class in case your schedule is otherwise jammed.


# Week 6: Tidy Data

So far we've been working with data that's all in a nice "tidy" structure. It should be little surprise that data doesn't always come structured that way. This week we'll learn to mold the structure of data to fit what we need to do with it.

Weekly assignments:

- **Homework 4** is posted, due on Friday.
- Rather than a **Discussion** this week, you'll be giving me your proposals for the replication project. Details coming soon.
- **Quiz 6** will also be posted soon.
- Don't forget **Preparation 6**. Sorry about posting it late; if you need extra time to complete the prep quiz that's fine.

Heads-up: our first test will be a week from Friday, during class time, in the lab.


# Week 5: Multiple Tables

Next week we level up our data wrangling skills by working with *relational* data. We'll also think more about how data structure relates to visualization structure.

***DATA SCIENCE FIREPIT!*** There's an informal social at Professor Pruim’s home on Wednesday (Sept 29), 7-9pm. This will be an informal, come-when-you-can evening in which you can meet data science students, faculty, and enthusiasts. Find the details and a signup sheet [here](https://docs.google.com/spreadsheets/d/1xZg0D-uASE87nhDogpx6J1YicFwTooevHYVL0sYAHVA/edit?usp=sharing).

Also, see Moodle for the usual weekly assignments:

- **Homework 3** is posted, due on Friday.
- **Discussion 4** is posted (see Moodle); it's asking you to make specific replies to other students in *last week's* forum. So it's due on Reply day (Thursday).
- Don't forget **Preparation 5** (due by class time Monday).
