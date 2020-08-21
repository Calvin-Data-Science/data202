
---
title: Day 1 Notes
...

# Day 1 (Wednesday)

## Notes for next time

* Way too much time on logistics. Don't go through the whole syllabus.
* Photos worked well, but "let me know after class if you don't want shared" would be better.
* didn't get to discussion about what is data science

## Email afterwards

Thanks for coming to the first day of DATA 202, my first class at Calvin! I sincerely apologize for running over time. The last few classes that I've both taught and taken have been 75-minute blocks, so it'll take me some time to get used to 50 minutes.

A few reminders:

* Sign up for Piazza.
* There's a video (12.5 min) and journal to prepare us for a short class discussion on Friday.
* I'll share class photos with all students on Thursday afternoon so we can start learning each other's names for the discussion. If you want to opt out, let me know before noon.

You should also start thinking about what you might want to replicate in your first project, since the first milestone is next week.

This class will be a lot of work for all of us, but God willing we will also learn a lot. I'm excited to be doing this and honored that you're doing it with me.

## Materials

* Copies of info sheets
* Name card paper (and card stock in case we run out)
* Sharpies
* Classroom computer logged on to GitHub with this page
* Moodle opened to Student role

## Outline

* Who am I?
  * Show family photo
  * Micah 6:8: act justly.
  * My story of how God led me to ask what computing/data + justice might look like
  * "this was abbreviated, happy to share more, including my doubts and wrestling with secular humanism"
  * Invitation to talk with me; how to address me.
  * Priestly prayer for students: may you become people who steward the power of data to act justly in the world.
  * 30 sec silence
* Who are you (students)?
  * Make a name card
  * Go around and get introductions: name, year, major, something outside of “data” that you’re interested in. I take a photo of each person with their name card, for us all to share (privately).
  * Fill out info sheet
* How does this course work? (**bring up the syllabus** and Moodle)
  * Goals (tech, communication, data&society, metacognition); **different from course catalog**
    * Technical tools for data science
      * Python data science stack
      * Data wrangling (80% of the work)
      * Predictive modeling (many of the same tools as stats, but different goals)
    * Communication skills (especially important for biz)
    * Social and ethical implications of data collection, data processing, and data-driven action. (important for everyone)
    * Metacognition: teamwork, planning, help-seeking, reflection.
    * This will be challenging, especially for those with less coding experience. But if you work hard at it, and communicate about your struggles, I'm confident you can do it.
  * Lids Down policy
  * Overview of course components
  * The weekly rhythm: due dates, meeting times, readings
    * Fixed weekly rhythm, variable and adaptive content.
  * Discussion: We will devote 20-30 min each week to a discussion of ethical issues and current events
    * Goal: Grow in our awareness of what responsible and irresponsible practices around data are.
      * Eventual goal: articulate a Christian, even Reformed, perspective on data science.
    * assignment for Friday
* What is data science?
  * Fill out a question on info sheet: what comes to mind when you think Data Science? Any recent news? Ow has data science affected your life?
  * Pair, share.
  * Let's think of examples of how data is used in lots of different places. Calvin? Journalism? Government? Retail? Medicine? Climate? ...
  * Show the first 3 min of J.B.’s video, if time allows.

Other

* Why?
  * Loving you means ceding power. I have a reasonably well considered idea of what would be useful, interesting, and feasible for you to study in this class, but I want to adapt what we cover to what's actually going to be interesting and feasible for you.
  * But I also hope that you can grow in responsible individual practices: not just putting in effort, but actually getting things done on time.
  * So in order to let you plan your routine, all the due dates will be the same, period.

Although the schedule of topics and readings may shift (since this is my first time running this course in this format), I want to make sure those shifts don't hinder your ability to plan.

# Day 2 (Friday)

## Materials

* Name card paper (and card stock in case we run out)
* **A printout of these notes**
* Tabs open:
  * [GenderShades website](http://gendershades.org/overview.html)
  * [GenderShades Paper](http://proceedings.mlr.press/v81/buolamwini18a/buolamwini18a.pdf)
  * [Joy Buolamwini's WEF video](https://www.youtube.com/watch?v=_sgji-Bladk)
* Room set up for discussion

## Outline

* Logistics
  * First homework will be released shortly after class.
  * Monday will be in lab
  * Interest in helping organize DS social?
* Warm-up Discussion
  * Data science in the news recently?
    * [NYT: YouTube fined for targeting ads at kids](https://www.nytimes.com/2019/09/04/technology/google-youtube-fine-ftc.html?action=click&module=Well&pgtype=Homepage&section=Business)
  * Let's think of examples of how data is used in lots of different places. Calvin? Journalism? Government? Retail? Medicine? Climate? ...
* First Ethics Discussion
  * Show the first few minutes (unless everyone submitted a journal)
  * Why would governments or companies want face recognition?
    * policing (surveillance, fugitives, aggression detection, ...)
    * military (strike, surveillance)
    * authentication (payment, entry, unlocking devices)
    * hiring (watch how you behave during interview)
    * education (are students paying attention?)
    * [article about China](https://www.scmp.com/news/china/society/article/2157883/drones-facial-recognition-and-social-credit-system-10-ways-china)
    * other applications
      * skin cancer detection -- will it be as good for underrepresented minorities?
  * Why is this news? Weren't we already evaluating accuracy?
  * Why does it matter if systems are inaccurate?
    * Gender classification isn't the main goal of most of these systems!
    * But error on an easy attribute (gender) suggests that other attributes may be wrong
  * Who is pointing this out? Who works at the tech companies?
  * [9:25] take-aways.
    * How we measure things matters.
    * Data affects people.
    * Need for diversity--datasets, employees
    * a personal confession: I thought Joy was "just" an excited MIT undergrad. **I stereotyped.**
* RESET THE ROOM.
* THIS IS DATA SCIENCE.
  * What did Joy actually do?
    * Acquired data (faces)
    * Did a lot of manual labeling (gender from titles/names, skin type by asking a dermatologist)
    * Augmented it with results of different APIs
    * Computed metrics (error rate, [Positive Predictive Value](https://en.wikipedia.org/wiki/Positive_and_negative_predictive_values), etc.) aggregated in different ways
    * **Communicated the results** through graphics, numbers, spoken and written language, poetry.
    * Was it effective? What made it effective?
  * We will do this too.
* If extra time (ha!)
  * draw a DataFrame
  * give some syntax examples
    * how to get at data: columns and iloc for now.
  * useful descriptive functions: info, describe, value_counts
