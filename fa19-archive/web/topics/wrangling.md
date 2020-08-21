# Data Wrangling

Two crucially important tasks in data wrangling are *merging* multiple datasets and
*aggregating* observations. Almost every project involves bringing
together data from two or more different sources, so you\'ll probably
find this very useful.

If you\'re a **reader:**

- [Chapter
    3.3](https://www.textbook.ds100.org/ch/03/pandas_grouping_pivoting.html)
    of the textbook
- Pandas\' [grouping
    documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html)
    (includes a *lot* more than we\'ll need, so pay attention mainly to
    the first few examples in the following sections: Aggregation,
    Transformation, Filtration, and \"Dispatching to instance methods\".

or if you\'re a **watcher**:

- [These
    slides](https://docs.google.com/presentation/d/1PuaVQkMaytd6fK-jb_FSnYn54EgWIhLThSsHFbNq6Rs/edit#slide=id.g4131093782_0_40)
    and [lecture video](https://youtu.be/RwsyYhSQSoU?t=902) from
    Data 100.

You\'ll only be responsible for knowing what we actually do together in
class, so don\'t worry about every detail of this reading.

## In-Class Exercise

* How many people share your birth month? groupby-transform
* How many people were born each month? groupby-aggregate(sum)
* What is your birthstone? join
* What is the earliest birthday in each month? groupby-aggregate(first)
* Who has the earliest birthday? groupby-aggregate(first)
* What is the average height for each month?
* How much above or below average are you for your month?
* Repeat for grouping by semester number at Calvin (starting at 1)

## Extra Resources

* [dplyr for R](https://dplyr.tidyverse.org/): grouping, aggregation, filtering
* [compared with Pandas](https://gist.github.com/TomAugspurger/6e052140eaa5fdb6e8c0/)