# Overall Notes for FA19

## Content

* We struggled to balance coding and intuition.
* Predictive analytics ≠ time series prediction / predict the future, but many students didn't appreciate this.
* Many students didn't appreciate how our predictive toolkit allows much more than just fitting a trend line
* Need more practice asking and refining real-world and modeling questions.
* Many students asked inference questions for their projects. We could have given them at least the bootstrap as an inference tool.

## Projects

* Many people had very interesting project ideas. Keeping projects open-ended is hard but probably worth it.
* Focus on a falsifiable claim was hard but worth it.
* Ask, for each dataset, *what does a row represent*?
* Emphasize reporting *why* (motivation) for decisions. Maybe even *mindfulness* about decisions.
* Could delve more into visualization fundamentals, intentionally reinforcing what DATA 101 does there.
* Common issues
  * Presentation
    * low-level technical descriptions, e.g., copy-paste from Pandas outputs or sklearn code
  * Wrangling
    * Difficulty handling non-tidy data
  * Coding
    * Lack of fluency with functions

## Tech

* matplotlib was more trouble than it's worth... maybe go with plotly or something else simple.
* Common gotcha: not actually *calling* a function (e.g., `df.value_counts`).

## Logistics

* Simple feedback soon would have been better than comprehensive feedback late.
* Journals and discussions worked well.
  * More lead time for students would be helpful.
* Frequent quizzes worked well, but should be predictable, so students can study/review.
* Group assignments, especially projects, should ask students to describe each person's contribution.

## The project rubric

* Formulation (2)
  * Real-world question
  * Modeling question
* Acquire (4)
  * High-level dataset description
  * Low-level
  * Provenance
  * Appropriateness
* Transform (1)
  * Wrangling
* Explore (2)
  * Univariate EDA
  * Bivariate EDA
* Model (3)
  * Setup/task
  * Baseline results
  * Improvements
* Analyze (4)
  * Findings -> modeling question
  * Findings -> real-world question
  * Limitations
  * Future Directions
* Communicate (5)
  * Decisions clearly stated
  * Report organization
  * Results replicable
  * Presented
  * Responsibility and Justice

# Note to students

I hope everyone has had a wonderful Christmas, New Year, and break! Thank you all so much for entrusting a significant portion of your attention and energy to me in the fall.

I'm very sorry for missing the final project presentations. Although I did end up feeling better shortly after, colleagues wisely advised me to stay home to not get anyone else sick. I'm not sure exactly what I had, but you definitely didn't want it at finals time. I hope to see you all around at other times, some even this Spring!

I've given feedback for all the project 2 final reports. When you look on Moodle, you may need to dig a bit: detailed comments are usually within the grading rubric and, for some people, in attached files.

Projects were graded using a rubric where each rubric item has 4 levels, basically: bad (0), moderate, good, exceptional (3). By design, few projects got exceptional ratings on many items. I intended that an A-level project would be "good" (not necessarily exceptional) on all categories, but Moodle calculates grades such that everything must be "exceptional" in order to get a 100% grade. I did some Moodle gradebook tricks to effectively make each item out of 2 instead of out of 3 for the final calculation, but still don't read too much into your numeric grade.

The most common issues with projects were actually not about technical content, which is great because reflecting on them can help with all of your professional work:

* In both the reports and the presentations, many groups jumped right into the *steps* they took, skipping over the *goal*.
* In the body of the report, few groups clearly *explained their decisions*--both low-level things like what models to try and also high-level things like why you chose your question, why you think the modeling/prediction question you chose was a good one in light of your real-world question, why you set up the modeling task the way you did (e.g., why that train-test split?), etc.
* Many presentations included copy-pastes or screenshots from Pandas or sklearn raw outputs, which are basically unintelligible to a non-technical audience. *Design for the audience*: what's going to be easy for *them* to understand? That's usually not the same as what's *easy for you to produce*.

Finally, if you're in the area, remember that Cathy O'Neil, author of [Weapons of Math Destruction](https://en.wikipedia.org/wiki/Weapons_of_Math_Destruction), is [speaking at the January Series](https://calvin.edu/calendar/event.html?id=5dcf7400-9549-4e25-8536-34c67ecd0174) on January 14 at 12:30 in CFAC. (The talk will not be recorded, so you'll have to actually be there.)
