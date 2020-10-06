Homework 02: Bike Sharing Data Visualization
================

# Homework 02: More Visualization

## Getting Started

    ## Parsed with column specification:
    ## cols(
    ##   instant = col_double(),
    ##   dteday = col_date(format = ""),
    ##   season = col_double(),
    ##   yr = col_double(),
    ##   mnth = col_double(),
    ##   hr = col_double(),
    ##   holiday = col_double(),
    ##   weekday = col_double(),
    ##   workingday = col_double(),
    ##   weathersit = col_double(),
    ##   temp = col_double(),
    ##   atemp = col_double(),
    ##   hum = col_double(),
    ##   windspeed = col_double(),
    ##   casual = col_double(),
    ##   registered = col_double(),
    ##   cnt = col_double()
    ## )

## Exercise 1: Label Days of Week

``` r
# Label Days of the Week
hourly_rides <- hourly_rides %>% 
  mutate(day_of_week = factor(day_of_week, levels = c(0, 1, 2, 3, 4, 5, 6),
                              labels = c("Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat")))
```

  - We can conclude that those were the correct labels by looking at
    what day 1 January 2011 and 2 January 2011 was. Seeing that 1
    January 2011 was a **Saturday**, which is labeled as *6*, and also
    seeing that 2 January 2011 was a **Sunday**, which is labeled as
    *0*, we can then assume that *1 through 5* are **Monday through
    Friday**.

## Exercise 2: Overall Counts by Weekday

``` r
ride_totals <- hourly_rides %>% 
  group_by(member_type, day_of_week) %>% 
  summarise(rides = sum(rides))
```

    ## `summarise()` regrouping output by 'member_type' (override with `.groups` argument)

``` r
ggplot(ride_totals, aes(x = day_of_week, y = rides, fill = member_type)) +
  geom_col(position = position_dodge()) +
  labs(x = "Day of Week", y = "Rides", fill = "Type of Rider")
```

<img src="hw02_solutions_files/figure-gfm/overall_counts_weekday-1.png" style="display: block; margin: auto;" />

  - By using `geom_col(position = position_dodge())`, we avoid the bar
    plot from being stacked.
  - As seen in the plot, there are more **registered** riders than
    **casual** riders in every single day of the week. There are more
    riders in the weekday which can be the result of people biking to
    and from work.

## Exercise 3: Distribution of Rides by Weekday

``` r
hourly_rides %>% 
  ggplot(aes(x = day_of_week, y = rides, fill = member_type)) +
  geom_boxplot() +
  labs(x = "Day of Week", y = "Rides", fill = "Type of Rider")
```

<img src="hw02_solutions_files/figure-gfm/distribution_rides_weekday-1.png" style="display: block; margin: auto;" />

  - The same pattern can be noted in the boxplot, yet the boxplot allows
    us to see *Median*, *Interquartile Range*, and *Outliers*.

## Exercise 4: Distribution of Rides by Hour

``` r
hourly_rides %>% 
  ggplot(aes(x = hour, y = rides, fill = member_type)) +
  geom_boxplot() +
  facet_wrap(~workingday, nrow = 2) +
  labs(x = "Hour", y = "Number of Rides")
```

<img src="hw02_solutions_files/figure-gfm/distribution_rides_hour-1.png" style="display: block; margin: auto;" />

  - There is an interesting pattern with these plots. While the
    *weekend* plot has a **unimodal**, the *workday* plot is
    **bimodal**. This might be the case as workers use bikes to get to
    work in the morning and use them again to go back home in the
    afternoon.

## Exercise 5: Overplotting

``` r
hourly_rides %>% 
  ggplot(aes(x = temp, y = rides)) +
  geom_point(alpha = 0.3) +
  facet_wrap(~member_type) + 
  labs(x = "Normalized Temperature", y = "Rides")
```

<img src="hw02_solutions_files/figure-gfm/over_plot_fix_1-1.png" style="display: block; margin: auto;" />
