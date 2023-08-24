
# Data Wrangling


```r
library(tidyverse)
```


## Resources

First, here are [some questions to ask if you're working with data that you didn't collect yourself](http://bit.ly/quaesita_notyours).
(That article is one of my favorites from the [analytics writings by the Head of Decision Intelligence at Google](https://decision.substack.com/p/analytics-the-complete-minicourse)


For more resources, see the previous chapter but also:

* [R for Data Science: Factors](https://r4ds.had.co.nz/factors.html)
* [dplyr](https://dplyr.tidyverse.org/): [cheat sheet](https://github.com/rstudio/cheatsheets/blob/master/data-transformation.pdf)
* [lubridate](https://lubridate.tidyverse.org/): [cheat sheet](https://rawgit.com/rstudio/cheatsheets/master/lubridate.pdf)

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

## A File Per Year

When you have multiple data files containing the same data, differing only by year or the like, it's typically best to combine them together early and do all the data wrangling to the combined data frame. For example, let's *pretend* that gapminder gave us their data one year at a time, and we got data frames like:




```r
head(gm_1952, 3)
```

```
## # A tibble: 3 × 5
##   country     continent lifeExp     pop gdpPercap
##   <fct>       <fct>       <dbl>   <int>     <dbl>
## 1 Afghanistan Asia         28.8 8425333      779.
## 2 Albania     Europe       55.2 1282697     1601.
## 3 Algeria     Africa       43.1 9279525     2449.
```

```r
head(gm_1957, 3)
```

```
## # A tibble: 3 × 5
##   country     continent lifeExp      pop gdpPercap
##   <fct>       <fct>       <dbl>    <int>     <dbl>
## 1 Afghanistan Asia         30.3  9240934      821.
## 2 Albania     Europe       59.3  1476505     1942.
## 3 Algeria     Africa       45.7 10270856     3014.
```

etc. We could merge those together like this:


```r
gm_combined <- bind_rows(
  year_1952 = gm_1952,
  year_1957 = gm_1957,
  .id = "year"
)
gm_combined
```

```
## # A tibble: 284 × 6
##    year      country     continent lifeExp      pop gdpPercap
##    <chr>     <fct>       <fct>       <dbl>    <int>     <dbl>
##  1 year_1952 Afghanistan Asia         28.8  8425333      779.
##  2 year_1952 Albania     Europe       55.2  1282697     1601.
##  3 year_1952 Algeria     Africa       43.1  9279525     2449.
##  4 year_1952 Angola      Africa       30.0  4232095     3521.
##  5 year_1952 Argentina   Americas     62.5 17876956     5911.
##  6 year_1952 Australia   Oceania      69.1  8691212    10040.
##  7 year_1952 Austria     Europe       66.8  6927772     6137.
##  8 year_1952 Bahrain     Asia         50.9   120447     9867.
##  9 year_1952 Bangladesh  Asia         37.5 46886859      684.
## 10 year_1952 Belgium     Europe       68    8730405     8343.
## # … with 274 more rows
```

We'd then want to convert that `year` column into a number. Two approaches: first the lazy one:


```r
gm_combined %>% mutate(year = parse_number(year))
```

```
## # A tibble: 284 × 6
##     year country     continent lifeExp      pop gdpPercap
##    <dbl> <fct>       <fct>       <dbl>    <int>     <dbl>
##  1  1952 Afghanistan Asia         28.8  8425333      779.
##  2  1952 Albania     Europe       55.2  1282697     1601.
##  3  1952 Algeria     Africa       43.1  9279525     2449.
##  4  1952 Angola      Africa       30.0  4232095     3521.
##  5  1952 Argentina   Americas     62.5 17876956     5911.
##  6  1952 Australia   Oceania      69.1  8691212    10040.
##  7  1952 Austria     Europe       66.8  6927772     6137.
##  8  1952 Bahrain     Asia         50.9   120447     9867.
##  9  1952 Bangladesh  Asia         37.5 46886859      684.
## 10  1952 Belgium     Europe       68    8730405     8343.
## # … with 274 more rows
```

And then the more principled one:


```r
gm_combined %>% 
  separate(year, into = c(NA, "year")) %>% 
  mutate(year = as.numeric(year)) # or pass `convert = TRUE` to separate
```

```
## # A tibble: 284 × 6
##     year country     continent lifeExp      pop gdpPercap
##    <dbl> <fct>       <fct>       <dbl>    <int>     <dbl>
##  1  1952 Afghanistan Asia         28.8  8425333      779.
##  2  1952 Albania     Europe       55.2  1282697     1601.
##  3  1952 Algeria     Africa       43.1  9279525     2449.
##  4  1952 Angola      Africa       30.0  4232095     3521.
##  5  1952 Argentina   Americas     62.5 17876956     5911.
##  6  1952 Australia   Oceania      69.1  8691212    10040.
##  7  1952 Austria     Europe       66.8  6927772     6137.
##  8  1952 Bahrain     Asia         50.9   120447     9867.
##  9  1952 Bangladesh  Asia         37.5 46886859      684.
## 10  1952 Belgium     Europe       68    8730405     8343.
## # … with 274 more rows
```

For some more advanced techniques, see "[Read Multiple Files into a Single Data Frame](https://www.mjandrews.org/blog/readmultifile/)".

## Panel Survey Data (e.g., Pew Research)

Pew and other sources release data in a file format used by SPSS, a commercial
statistical analysis tool. Fortunately it's straightforward to read this data
in R, using the [`haven`](https://haven.tidyverse.org/) package.

I'll show an example with the [American Trends Panel](https://www.pewresearch.org/our-methods/u-s-surveys/the-american-trends-panel/).

### Reading SPSS files with `haven`


```r
library(tidyverse)
atp_w34 <- haven::read_sav("data/W34_Apr18/ATP W34.sav")
```

The easiest way to look at this data is to click on it in the "Environment" panel,
or run `View(atp_w34)` on the Console. (Remember not to leave a `View` call in
an Rmd when you Knit.)

You'll see that each column has a label. It might be hard to read all of them, so
here's a bit of magic code to make a table of just the column labels:


```r
getColumnLabels <- function(df) {
  tibble(
    name = names(df),
    label = map_chr(names(df), ~ attr(df[[.]], "label"))
  )
}
getColumnLabels(atp_w34)
```

```
## # A tibble: 140 × 2
##    name            label                                                        
##    <chr>           <chr>                                                        
##  1 QKEY            Unique ID USE THIS TO MERGE WAVES                            
##  2 Device_Type_W34 Wave 34 New Device Type                                      
##  3 LANGUAGE_W34    Language                                                     
##  4 FORM_W34        FORM Assignment                                              
##  5 SCI1_W34        SCI1. Overall, do you think science has made life easier or …
##  6 SCI2A_W34       SCI2A. Do you think science has had a mostly positive or mos…
##  7 SCI2B_W34       SCI2B. Do you think science has had a mostly positive or mos…
##  8 SCI2C_W34       SCI2C. Do you think science has had a mostly positive or mos…
##  9 SCI3A_W34       SCI3A. In your opinion, do you think government investments …
## 10 SCI3B_W34       SCI3B. In your opinion, do you think government investments …
## # … with 130 more rows
```



Many of the columns are actually factors in disguise. To decode their labels,
call `as_factor`. For example, to get party affiliations and leanings from
the ATP data, we can do:


```r
atp_w34_wrangled <- atp_w34 %>% 
  mutate(
    party = as_factor(F_PARTY_FINAL),
    party_lean = as_factor(F_PARTYLN_FINAL),
    age = as_factor(F_AGECAT_FINAL))
atp_w34_wrangled %>% select(party, party_lean)
```

```
## # A tibble: 2,537 × 2
##    party       party_lean          
##    <fct>       <fct>               
##  1 Republican  <NA>                
##  2 Democrat    <NA>                
##  3 Democrat    <NA>                
##  4 Independent The Republican Party
##  5 Republican  <NA>                
##  6 Republican  <NA>                
##  7 Democrat    <NA>                
##  8 Republican  <NA>                
##  9 Independent The Republican Party
## 10 Republican  <NA>                
## # … with 2,527 more rows
```

Here's a function to rename a bunch of columns to match their labels. I think it's clumsy; probably the above is better.


```r
name_as_label <- function(df, cols_to_rename) {
  new_names <- list()
  for (col in cols_to_rename) {
    new_names[[attr(df[[col]], "label")]] = col
  }
  df %>% rename(!!as_vector(new_names))
}

atp_w34 %>% 
  name_as_label(cols_to_rename = c("F_PARTY_FINAL", "Device_Type_W34", "LANGUAGE_W34"))
```

```
## # A tibble: 2,537 × 140
##      QKEY Wave 34 New …¹ Langu…² FORM_…³ SCI1_…⁴ SCI2A…⁵ SCI2B…⁶ SCI2C…⁷ SCI3A…⁸
##     <dbl>      <dbl+lbl> <dbl+l> <dbl+l> <dbl+l> <dbl+l> <dbl+l> <dbl+l> <dbl+l>
##  1 100314 1 [Mobile pho… 9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 1 [Mos… 1 [Gov…
##  2 100363 1 [Mobile pho… 9 [Eng… 2 [For… 1 [Eas… 2 [Mos… 1 [Mos… 1 [Mos… 1 [Gov…
##  3 100588 1 [Mobile pho… 9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 2 [Mos… 1 [Gov…
##  4 100637 3 [Desktop]    9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 1 [Mos… 2 [Gov…
##  5 101224 3 [Desktop]    9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 1 [Mos… 2 [Gov…
##  6 101322 1 [Mobile pho… 9 [Eng… 1 [For… 1 [Eas… 2 [Mos… 2 [Mos… 2 [Mos… 2 [Gov…
##  7 101400 1 [Mobile pho… 9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 1 [Mos… 1 [Gov…
##  8 101437 3 [Desktop]    9 [Eng… 1 [For… 1 [Eas… 2 [Mos… 2 [Mos… 1 [Mos… 2 [Gov…
##  9 101472 3 [Desktop]    9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 1 [Mos… 1 [Gov…
## 10 101493 1 [Mobile pho… 9 [Eng… 1 [For… 1 [Eas… 1 [Mos… 1 [Mos… 1 [Mos… 1 [Gov…
## # … with 2,527 more rows, 131 more variables: SCI3B_W34 <dbl+lbl>,
## #   SCI3C_W34 <dbl+lbl>, SCI4_W34 <dbl+lbl>, SCI5_W34 <dbl+lbl>,
## #   EAT1_W34 <dbl+lbl>, EAT2_W34 <dbl+lbl>, FUD30A_W34 <dbl+lbl>,
## #   FUD30B_W34 <dbl+lbl>, FUD30C_W34 <dbl+lbl>, FUD30D_W34 <dbl+lbl>,
## #   EAT3A_W34 <dbl+lbl>, EAT3B_W34 <dbl+lbl>, EAT3C_W34 <dbl+lbl>,
## #   EAT3D_W34 <dbl+lbl>, EAT3E_W34 <dbl+lbl>, EAT3F_W34 <dbl+lbl>,
## #   EAT3G_W34 <dbl+lbl>, EAT3H_W34 <dbl+lbl>, EAT3I_W34 <dbl+lbl>, …
```


### Weights

Note that Pew survey data include *weights*. Read their Methodology sections for details about these weights.
Once you've identified the correct weights to use, you can use the `wt` parameter to `count`
to weight your counts accordingly, or the `weighted.mean` function if you're interested in a
specific outcome.

For example, the following gives the proportion of each party among *survey respondents*:


```r
atp_w34_wrangled %>% 
  count(party) %>% 
  mutate(proportion = n / sum(n))
```

```
## # A tibble: 6 × 3
##   party              n proportion
##   <fct>          <int>      <dbl>
## 1 Republican       575   0.227   
## 2 Democrat         973   0.384   
## 3 Independent      696   0.274   
## 4 Something else   280   0.110   
## 5 Refused           12   0.00473 
## 6 <NA>               1   0.000394
```

while this gives the (estimated) proportion of each party in the US:


```r
atp_w34_wrangled %>% 
  count(party, wt = WEIGHT_W34) %>% 
  mutate(proportion = n / sum(n))
```

```
## # A tibble: 6 × 3
##   party               n proportion
##   <fct>           <dbl>      <dbl>
## 1 Republican     619.     0.244   
## 2 Democrat       804.     0.317   
## 3 Independent    728.     0.287   
## 4 Something else 370.     0.146   
## 5 Refused         14.8    0.00583 
## 6 <NA>             1.42   0.000558
```

Add more variables to `count` to get cross-tabulations:


```r
atp_w34_wrangled %>% 
  count(party, age, wt = WEIGHT_W34) %>% 
  group_by(age) %>% # Get party membership within each age range
  mutate(proportion = n / sum(n))
```

```
## # A tibble: 23 × 4
## # Groups:   age [5]
##    party       age        n proportion
##    <fct>       <fct>  <dbl>      <dbl>
##  1 Republican  18-29  68.0       0.132
##  2 Republican  30-49 173.        0.209
##  3 Republican  50-64 198.        0.289
##  4 Republican  65+   177.        0.353
##  5 Republican  <NA>    2.23      0.573
##  6 Democrat    18-29 128.        0.248
##  7 Democrat    30-49 287.        0.345
##  8 Democrat    50-64 233.        0.340
##  9 Democrat    65+   157.        0.312
## 10 Independent 18-29 172.        0.334
## # … with 13 more rows
```




## Afterward

* [Arquero](https://observablehq.com/@uwdata/introducing-arquero) is a new
  JavaScript library that uses almost all of the same basic concepts
  of the Grammar of Data, though sometimes with different names.
