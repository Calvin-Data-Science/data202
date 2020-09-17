Homework 3: Bike Sharing Data Wrangling
================
YOUR NAME
TODAY’S DATE

Load Data
---------

    # Read the file, specifying data types for each column.
    rides_2011 <- read_csv("data/rides_2011.csv.gz", col_types = cols(
      start_time = col_datetime(),
      duration = col_double(),
      member_type = col_factor()
    ))
    rides_2012 <- read_csv("data/rides_2012.csv.gz", col_types = cols(
      start_time = col_datetime(),
      duration = col_double(),
      member_type = col_factor()
    ))

Exercise 1
----------

*Your narrative answer here.*

Exercise 2
----------

*Your narrative answer here.*

    # Your code here. Be sure to give this code chunk a meaningful label.

Exercise 3
----------

    # Your code here. Be sure to give this code chunk a meaningful label.

Exercise 4
----------

    # Your code here. Be sure to give this code chunk a meaningful label.

*Your narrative answer here.*

Exercise 5
----------

    # Your code here. Be sure to give this code chunk a meaningful label.

Exercise 6
----------

Add code blocks as needed for this and remaining exercises.

Exercise 7
----------

Exercise 8
----------

Exercise 9
----------
