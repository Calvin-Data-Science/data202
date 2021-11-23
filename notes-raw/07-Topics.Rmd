
# Other Topics


## Recommendation Systems

### Discussion Activity

Pick one of the following questions. Read one or more of the linked articles, or find a different article on the topic. Write a response of a paragraph or two where you:

- Summarize the main point of the article, for the sake of others who didn't read it,
- Argue why the question is (or isn't) important or interesting, and
- State your own response: a counter-point, an additional example, a question it raises for you, how it might shape your own life, etc.

Here are the list of questions:

- Should social media platforms be legally responsible for the content they recommend to you?
  - [When Curation Becomes Creation](https://lib-proxy.calvin.edu/login?url=https://cacm.acm.org/magazines/2021/12/256928-when-curation-becomes-creation/fulltext) ([original link](https://cacm.acm.org/magazines/2021/12/256928-when-curation-becomes-creation/fulltext)),  By Liu Leqi, Dylan Hadfield-Menell, Zachary C. Lipton.
  - [the facebook files](https://www.wsj.com/articles/the-facebook-files-11631713039)
- How do social media platforms determine what content to recommend?
  - Read `rsweeny21`'s [comment](https://news.ycombinator.com/item?id=20566514) from a developer of Netflix's autoplay.
  - Do you use Pinterest? [Here's how Pintrest's recommender system works](https://blog.acolyer.org/2018/05/23/pixie-a-system-for-recommending-3-billion-items-to-200-million-users-in-real-time/), at least a few years ago.
  - [YouTube's Recommender System](https://blog.acolyer.org/2016/09/19/deep-neural-networks-for-youtube-recommendations/) uses neural nets to learn from watch times. This paper is a few years old but still insightful.
- Do recommendation systems "radicalize" people?
  - search for "YouTube radicalize" or similar. You'll probably find articles asserting that it happens.
  - But you'll hopefully find some counterpoints, like [Examining the consumption of radical content on YouTube | PNAS](https://www.pnas.org/content/118/32/e2101967118.short).
  - [Designing Recommender Systems to Depolarize | Abstract](https://arxiv.org/abs/2107.04953)
- What do recommendation systems do to human creativity?
  - [Predictive Text Encourages Predictable Writing](https://www.eecs.harvard.edu/~kgajos/papers/2020/arnold20predictcive.shtml)
- Ads are often shown alongside other recommended content. Can ads be harmful?
  - [Discrimination in Online Ad Delivery](https://arxiv.org/abs/1301.6822) -- classic paper by Harvard professor Latanya Sweeney
  


## Text Mining (and bias)

* [Tidy Text Mining](https://www.tidytextmining.com/sentiment.html#sentiment-analysis-with-inner-join) (link is to a specific interesting section)
* [How to make a racist AI without really trying](https://blog.conceptnet.io/posts/2017/how-to-make-a-racist-ai-without-really-trying/)
  and a [follow-up in R](https://notstatschat.rbind.io/2018/09/27/how-to-write-a-racist-ai-in-r-without-really-trying/)

## Resources

ACM Selects:

* [Data Science](https://selects.acm.org/selections/getting-started-with-data-science)

## Relational Databases

Contrasting data storage formats:
* CSVs are useful to store and exchange *small* to *medium* amounts of "static" data
* relational databases are useful when data is growing / changing (especially from multiple sources)
* relational databases are useful when multiple systems or stakeholders need the same data
* relational databases are useful when data is too big to fit in memory, since RDBMS's can often automatically figure out how to compute things in a "distributed" or "streaming" way
  * So-called NoSQL systems, like MongoDB and Firebase, have been popular in recent years, but SQL remains pervasive in industry because of its robustness, consistency, and performance.

SQL tutorials:

* [Codecademy](https://www.codecademy.com/learn/learn-sql)
* [w3schools](https://www.w3schools.com/sql/)

SQL Syntax reference

* I kinda like the "railway diagrams" in the [sqlite syntax documentation](https://www.sqlite.org/lang.html) (e.g., for the [SELECT statement](https://www.sqlite.org/lang_select.html))
* [Codecademy has a reference](https://www.codecademy.com/articles/sql-commands)
* [TutorialsPoint](https://www.tutorialspoint.com/sql/sql-syntax.htm)

[sqlfiddle](http://sqlfiddle.com/)
