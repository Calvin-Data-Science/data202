# Overall Notes for FA19

## Content

* We struggled to balance coding and intuition.
* Predictive analytics ≠ time series prediction, but many students didn't appreciate this.
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

* I've given feedback for all the project 2 final reports. It took quite a while because I tried to be constructive and identify generalizable take-aways that you can apply to future data-centered work, even if it uses very different tools than we used in DATA 202.
  * See detailed comments within the rubric and, for some people, in attached files.
* Each rubric item has 4 levels, basically: bad (0), moderate, good, exceptional (3). By design, few people will get exceptional ratings on many items. But for how Moodle calculates grades, everything must be exceptional in order to be 100%. So I did some Moodle gradebook tricks to effectively make each item out of 2 instead of out of 3. 
* Common issues with projects
  * Skipping the motivation, jumping right into the weeds.
  * Partially because of the order that I'd listed the elements in, but still... this is basic communication skill.
  * Including copy-pastes / screenshots of coding stuff in the presentation. Amateur. Design for the viewer: what's going to be easy for *them* to understand, not the same as what's easy for you to produce.
  * Not explaining why you made the decisions you did--both low-level things like what models to try and also high-level things like why you chose your question, why you think the modeling/prediction question you chose was a good one in light of your real-world question, why you set up the modeling task the way you did (e.g., why that train-test split?), etc.
* Remember Cathy O'Neil talk
