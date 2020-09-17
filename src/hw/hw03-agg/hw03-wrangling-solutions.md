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

    rides <- bind_rows(
      rides_2011,
      rides_2012
    )

There are 3255678 rides in this dataset.

Exercise 2
----------

`duration` is probably measured in seconds, because most rides are less
than 30 \* 60 seconds (30 minutes), but some are as long as 86,355,
which is most of a day (86,400 seconds).

    rides %>% 
      ggplot(aes(x = duration)) +
        geom_histogram(binwidth = 30 * 60)

![](hw03-wrangling-solutions_files/figure-gfm/duration-hist-1.png)<!-- -->

Exercise 3
----------

    rides %>%
      count(member_type)

    ## # A tibble: 3 x 2
    ##   member_type       n
    ##   <fct>         <int>
    ## 1 Member      2636066
    ## 2 Casual       619591
    ## 3 Unknown          21

Exercise 4
----------

    hourly_rides <- rides %>%
      group_by(start_hour = floor_date(start_time, unit = "hours")) %>% 
      count()

Exercise 5
----------

    hourly_rides <- rides %>%
      group_by(hour = floor_date(start_time, unit = "hours"), member_type) %>% 
      summarize(rides = n())

Exercise 6
----------

    daily_rides <- rides %>%
      group_by(day = floor_date(start_time, unit = "days"), member_type) %>% 
      summarize(rides = n())

Exercise 7
----------

    hourly_rides %>%
      filter(member_type != "Unknown") %>% 
      ggplot(aes(x = wday(hour, label = TRUE), y = rides, fill = member_type)) +
      geom_boxplot() +
      labs(y = "Rides", x = "Day of Week", fill = "Type of Rider")

![](hw03-wrangling-solutions_files/figure-gfm/rides-by-weekday-1.png)<!-- -->

Exercise 8
----------

| weekday | Member | Casual |
|:--------|-------:|-------:|
| Sun     |     88 |     27 |
| Mon     |    111 |     18 |
| Tue     |    120 |     18 |
| Wed     |    121 |     17 |
| Thu     |    128 |     18 |
| Fri     |    134 |     21 |
| Sat     |     99 |     29 |

Exercise 9
----------

    hourly_rides %>% 
      filter(member_type != "Unknown") %>% 
      mutate(is_weekend = if_else(
        wday(hour, label = TRUE) %in% c("Sat", "Sun"),
        "Weekend", "Weekday")) %>% 
      ggplot(aes(x = as_factor(lubridate::hour(hour)), y = rides, fill = member_type)) + 
        geom_boxplot() +
        facet_wrap(~ is_weekend, scales = "free_y", nrow = 2)

![](hw03-wrangling-solutions_files/figure-gfm/ride-distributions-by-hour-1.png)<!-- -->
