# Quiz 1

1. In a sentence, describe one take-away from our discussion of Joy Boulamwini's presentation. For full credit, this take-away should be something that could apply to something other than the accuracy of commercial face recognition systems.

2. Suppose that `x` is a `DataFrame`. `x.info()` produced the following output:

    ```
    ...TODO
    ```

    Draw a plausible result for `x.head(n=2)`.

3. Suppose that `movie_earnings` is a DataFrame with the following structure:

    ```
    TODO
    ```

    Which of the following expressions would give the Series of the genres of all movies that grossed more than $50,000? `top_earnings_genres = ...`

    a. `movie_earnings.loc[Genre, Gross > 50000]`

    b. `movie_earnings.loc["Genre", "Gross" > 50000]`

    c. `movie_earnings[movie_earnings["Gross" > 50000]]["Genre"]`

    d. `movie_earnings["Gross" > 50000].loc["Genre"]`

4. Suppose that `top_earnings_genres` is the Series computed in #3. `top_earnings_genres.head(3)` looks like the following:

    ```
    TODO
    ```

    Write an expression that would get the genre that occurs most commonly in that Series.

5. Name one type of data that an organization is collecting about you that you hadn't thought about before taking this course.

6. Name one business decision that an organization you relate with is making based on data.

And a few questions for feedback:

* I'm finding the content of this course *interesting*:
* I'm finding the content of this course *relevant*:
* I know what the goal of most class meetings is.
* I know what the goal of most assignments is.
* I feel I can succeed at most assignments.
