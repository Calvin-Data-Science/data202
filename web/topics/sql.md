# SQL

* [Textbook chapter](https://www.textbook.ds100.org/ch/09/sql_intro.html)
  * Note: The rationale for RDBMS's in the first section is incomplete. I'd say:
    * CSVs are useful to store and exchange *small* to *medium* amounts of "static" data
    * relational databases are useful when data is growing / changing (especially from multiple sources)
    * relational databases are useful when multiple systems or stakeholders need the same data
    * relational databases are useful when data is too big to fit in memory, since RDBMS's can often automatically figure out how to compute things in a "distributed" or "streaming" way
  * So-called NoSQL systems, like MongoDB and Firebase, have been popular in recent years, but SQL remains pervasive in industry because of its robustness, consistency, and performance.
* [DATA100 Slides](https://docs.google.com/presentation/d/1AJfF2wFqRIYM8qdnyhwFyqY1DKY3VBqpaoWZ0GjI38w/edit)
* Other SQL tutorials:
  * [Codecademy](https://www.codecademy.com/learn/learn-sql)
  * [w3schools](https://www.w3schools.com/sql/)
* Syntax reference
  * I kinda like the "railway diagrams" in the [sqlite syntax documentation](https://www.sqlite.org/lang.html) (e.g., for the [SELECT statement](https://www.sqlite.org/lang_select.html))
  * [Codecademy has a reference](https://www.codecademy.com/articles/sql-commands)
  * [TutorialsPoint](https://www.tutorialspoint.com/sql/sql-syntax.htm)

## Extra Resources

* sqlfiddle [example](http://sqlfiddle.com/#!9/a6c585/1)