
# Data Wrangling

## Resources

First, here are [some questions to ask if you're working with data that you didn't collect yourself](http://bit.ly/quaesita_notyours).
(That article is one of my favorites from the [analytics writings by the Head of Decision Intelligence at Google](https://decision.substack.com/p/analytics-the-complete-minicourse)


For more resources, see the previous chapter but also:

* [R for Data Science: Factors](https://r4ds.had.co.nz/factors.html)
* [dplyr](https://dplyr.tidyverse.org/): [cheat sheet](https://github.com/rstudio/cheatsheets/blob/master/data-transformation.pdf)
* [lubridate](https://lubridate.tidyverse.org/): [cheat sheet](https://rawgit.com/rstudio/cheatsheets/master/lubridate.pdf)
* Some [tips for working with SPSS data](https://cs.calvin.edu/courses/data/202/fa20/spss-tips.html) (e.g., Pew)

### Practice

[TidyTuesday](https://github.com/rfordatascience/tidytuesday) has weekly examples!

David Robinson, contributor to several notable R packages, has done [screencasts](https://www.youtube.com/user/safe4democracy/videos)
of analyzing many TidyTuesday examples. [Here's the code](https://github.com/dgrtwo/data-screencasts).

## SQL and BigQuery

Query languages allow us to query big datasets from our small computers. The most
popular by far is SQL.

Google's BigQuery is a SQL-like language for querying datasets stored on its
cloud infrastructure. Most of the time you'll be querying data that are internal
to your organization, but Google and other providers have published some open
datasets. Some examples:

* [NFL Play-by-Play](https://calogica.com/r/bigquery/2020/08/18/r-bigquery.html)
* [NYC Yellow-Cab Trips](https://cfss.uchicago.edu/notes/sql-databases/#interacting-with-google-bigquery-via-dplyr)
* [FiveThirtyEight analysis of subreddit relationships](https://github.com/fivethirtyeight/data/tree/master/subreddit-algebra)


## Afterward

* [Arquero](https://observablehq.com/@uwdata/introducing-arquero) is a new
  JavaScript library that uses almost all of the same basic concepts
  of the Grammar of Data, though sometimes with different names.
