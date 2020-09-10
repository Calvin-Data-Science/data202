Homework 2: Bike Sharing Data Visualization
================
YOUR NAME
TODAY’S DATE

*Your introduction here*

Read Data
---------

    hourly_rides <- read_csv("data/hour.csv") %>%
      mutate(across(c(season, year, hour, holiday, workingday, day_of_week, weather_type, member_type), as.factor))
    hourly_rides %>% glimpse()

    ## Rows: 34,758
    ## Columns: 14
    ## $ date         <date> 2011-01-01, 2011-01-01, 2011-01-01, 2011-01-01, 2011-01…
    ## $ hour         <fct> 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9,…
    ## $ season       <fct> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,…
    ## $ year         <fct> 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,…
    ## $ holiday      <fct> 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,…
    ## $ workingday   <fct> weekend, weekend, weekend, weekend, weekend, weekend, we…
    ## $ day_of_week  <fct> 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,…
    ## $ weather_type <fct> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1,…
    ## $ temp         <dbl> 0.24, 0.24, 0.22, 0.22, 0.22, 0.22, 0.24, 0.24, 0.24, 0.…
    ## $ feels_like   <dbl> 0.2879, 0.2879, 0.2727, 0.2727, 0.2727, 0.2727, 0.2879, …
    ## $ humidity     <dbl> 0.81, 0.81, 0.80, 0.80, 0.80, 0.80, 0.75, 0.75, 0.75, 0.…
    ## $ windspeed    <dbl> 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, …
    ## $ member_type  <fct> casual, registered, casual, registered, casual, register…
    ## $ rides        <dbl> 3, 13, 8, 32, 5, 27, 3, 10, 0, 1, 0, 1, 2, 0, 1, 2, 1, 7…

Exercise 1: Label days of week
------------------------------

    hourly_rides <- hourly_rides %>%
      mutate(day_of_week = factor(day_of_week, levels = c(0, 1, 2, 3, 4, 5, 6), labels = c("DAY", "ANOTHER DAY", "...", "...", "...", "...", "...")))

Exercise 2: Overall counts by weekday
-------------------------------------

    ride_totals <- hourly_rides %>%
      group_by(member_type, day_of_week) %>% 
      summarize(rides = sum(rides))

    # your code here

Exercise 3: Distribution of Rides by Weekday
--------------------------------------------

    # your code here

Exercise 4: Distribution of Rides by Hour
-----------------------------------------

    # your code here

Exercise 5: Overplotting
------------------------

    ggplot(hourly_rides, aes(x = temp, y = rides)) +
      geom_point() +
      facet_wrap(~ member_type) + 
      labs(x = "Normalized temperature", y = "Rides")

![](hw02-vis_files/figure-gfm/rides-by-temp-overplot-1.png)<!-- -->

### Approach 1

### Approach 2

### Comparison

*Which do you prefer, and why?*
