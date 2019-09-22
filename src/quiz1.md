# Quiz 1

1. In a sentence, describe one take-away from our discussion of Joy Boulamwini's presentation. For full credit, this take-away should be something that could apply to something other than the accuracy of commercial face recognition systems.

2. Suppose that `x` is a DataFrame and `x.info()` produced the following output:

    ```
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 5 entries, 5 to 105233
    Data columns (total 2 columns):
    n    5 non-null object
    h    5 non-null float64
    dtypes: float64(1), object(1)
    memory usage: 120.0+ bytes
    ```

    What would be a plausible result for `x.head(n=2)`?

3. Suppose that `movie_earnings` is a DataFrame and `movie_earnings.info()` produced the following output:

    ```
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 18 entries, 0 to 17
    Data columns (total 5 columns):
    Director    18 non-null object
    Genre       18 non-null object
    Movie       18 non-null object
    Rating      18 non-null int64
    Revenue     18 non-null int64
    dtypes: int64(2), object(3)
    memory usage: 800.0+ bytes
    ```

    Which of the following expressions would give the Series of the `Genre`s of all movies with `Revenue` more than 50,000? `high_earnings_genres = ...`

    a. `movie_earnings.loc[Genre, Revenue > 50000]`

    b. `movie_earnings.loc["Genre", "Revenue" > 50000]`

    c. `movie_earnings[movie_earnings["Revenue"] > 50000]["Genre"]`

    d. `movie_earnings[movie_earnings["Revenue" > 50000]]["Genre"]`

    e. `movie_earnings["Revenue" > 50000].loc["Genre"]`

4. Suppose that `high_earnings_genres` is the Series computed in #3. `high_earnings_genres.head(3)` looks like the following:

    ```
    0           Action & Adventure
    1                       Comedy
    2    Science Fiction & Fantasy
    Name: Genre, dtype: object
    ```

    Which expression would show the `Genre` that occurs most commonly in `high_earnings_genres`? (If the output will also include some other information, that's ok.)

    a. `high_earnings_genres.loc[0]` (no: that's just the first entry)
    
    b. `high_earnings_genres.sort_values().loc[0]` (no, that would be the first genre alphabetically)
    
    c. `high_earnings_genres.value_counts().head(1))` (returns a single-item Series with the genre as the one index item and its occurrence count as the value. Add `.index[0]` to get the actual value.)


    
5. Name one type of data that an organization is collecting about you that you hadn't thought about before taking this course.

6. Name one business decision that an organization you relate with is making based on data.

Rate how much you agree with these statements on a scale of 1 (strongly disagree) to 5 (strongly agree). Any comments are welcome.

* I'm finding the content of this course *interesting*:
* I'm finding the content of this course *relevant*:
* I know what the goal of most class meetings is.
* I know what the goal of most assignments is.
* I feel I can succeed at most assignments.



Here is a Moodle Cloze format for Q2, generated with the help of [this tool](http://projects.ael.uni-tuebingen.de/quiz/htmlarea/index.php)

```
<table class="dataframe" border="1">
<thead>
<tr style="text-align: right;"><th>&nbsp;</th><th>{1:SHORTANSWER:%100%n#}</th><th>{1:SHORTANSWER:%100%h#}</th></tr>
<tr><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th></tr>
</thead>
<tbody>
<tr>
<td>{1:SHORTANSWER:%100%5#}</td>
<td>{1:MULTICHOICE:%100%Oscar#~%100%5.5#more likely it would be a string, but this is also valid.}</td>
<td>{1:MULTICHOICE:%100%5.5#~%0%Matthew#Should be a floating point number}</td>
</tr>
<tr>
<td>{1:MULTICHOICE:%100%6#~%0%2#~%0%Index#~%0%h#}</td>
<td>{1:MULTICHOICE:%100%Ruth#~%100%5.5#more likely it would be a string, but this is also valid.}</td>
<td>{1:MULTICHOICE:%100%7.8#~%0%$4.5#Should be a floating point number}</td>
</tr>
</tbody>
</table>
```


Some good example responses to Question 1:

* "One other takeaway that I had from that presentation is that algorithms can easily become biased, even if nobody is actually attempting to make them biased; and to solve this issue in this situation, we need to have more diversity in the tech industry."
* "We talked about how often we don't recognize bias that is towards group of people different from ourselves, and how those biases are dangerous, as they can easily slip through if we're not conscious and thinking about them."
* "We as a future people in the technology field have to be conscious of the bias that we may accidentally program into our software."
* "It is important to use a representative dataset and it's important to be mindful of ways that your dataset might not be representative by considering others' viewpoints."
