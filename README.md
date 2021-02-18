## Calvin University - DATA 202

Notes after 20FA:

### Overall Strategy

* Use 20FA projects as 21FA case studies.
  * Visuals
  * Modeling
* Cover time series forecasting as a main topic.
* How to trace back the source of data … maybe do a full project in class where we trace the provenance of some dataset and discuss the issues that come up in it
* Walk through the process of scoping a project? E.g., person has gotten to some point in their project, what steps might they take next and why? Case study, perhaps driven by final projects from this year
* Visualization of modeling would be a good emphasis for next year. Interpretabiblity.
* Students were quite weak at critiquing others’ presentations. We could practice this.
* No one is referencing prior analyses of their data. We could do a critique-replicate-improve workflow here too.

### Presentation

Overall

* Need to give students copious examples of good reporting of modeling results.
* I’m commenting about whether a plot is “legible” or not a lot. Should describe and comment on this.
* Reports have play-by-play and updates, rather than a synthesis based on “all that I now know”. (e.g., Joe P)
* People should read their own reports, to discover issues like missing blank line before headings.
* I got a bunch of vague citations. Give examples of clear vs unclear citations to data?

Tech / details

* Give students tools for reporting modeling tables effectively, not just yardstick %>% kable
* Y axis labels in bar graphs are usually upside down...why?
* Discuss caching for speeding up knitting with large data.
* The suggested report outline is a bit odd in terms of how data is described. Work a few good examples?
* Give good examples of summarizing data structure. (glimpse() is poor but many people used it)
* My graph of classification metrics (accuracy, sens, spec) for CV results was lazy; it’s not a good data visualization. Too many people copying it.
* Discuss how to turn on and off various things in RMarkdown reports for better presentation


### Wrangling

* Practice log-transforming data
* Providing weather data would be good
* So many people had weak handling of missing data! Often it just got dropped unceremoniously. Need examples of thoughtful reporting and implications of missingness.
* Do the data wrangling once, early. (counterexamples: Joe P, Ben Steves)

### Modeling

* Need some examples of different validation strategies and why each one is helpful
* Should reinforce how linear regression can be hard to interpret. E.g., Won Seok’s project
* MAE is pretty interpretable, but maybe a relative error metric would be even more clear to include.
* Discuss potential modeling issues (class imbalance, e.g. the solar flare data)
* Discuss interpretation of variable importance
* Should probably discuss tools for working with large datasets.
* Discuss hyperparameter tuning 
* Histogram of the response variable, potentially transforming it to be less skewed or to be unbounded.
