


# Visualization

We start with visualization because, well, you can see the results.

## Reading

To design good visuals, you need both *why*s and *how*s. You may have come here for the *how*s, but both are important. Our tools are changing more rapidly than ever, so if we want knowledge that lasts, we really need to know the *why*.

### Why

Read **[Look at Data](https://socviz.co/lookatdata.html)** from Healy "Data Visualization".

The text is wordy but well organized, so your speed reading skills should work well. Look at the examples: can you explain to someone else what those examples show?

### How

Read [**Data Visualization**](https://moderndive.com/2-viz.html) from ModernDive.

Try to actually answer the "Learning Check" questions for yourself. Yes this takes longer than just skimming right past them. But they may show up on a quiz...

## Application

* You did some visualization in Lab 1. How did that exercise relate to the "why" reading?

## References

* If you're the slides type, [here's some slides](https://datasciencebox.org/exploring-data.html#slides-application-exercises).
We got to most of this material but not quite all of it yet.
* <https://socviz.co/>
* [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)

## Tweaks

### Reordering bars in a bar plot

Use `fct_reorder` on the categorical variable.


```r
starwars %>% 
  drop_na(height) %>% 
  ggplot(aes(x = height, y = species)) +
  geom_boxplot()
```

<img src="02-Vis_files/figure-html/mass-by-species-1.png" width="672" />


```r
starwars %>% 
  drop_na(height) %>% 
  ggplot(aes(x = height, y = fct_reorder(species, height))) +
  geom_boxplot()
```

<img src="02-Vis_files/figure-html/species-by-height-median-1.png" width="672" />


```r
starwars %>% 
  drop_na(height) %>% 
  ggplot(aes(x = height, y = fct_reorder(species, height, .fun = max))) +
  geom_boxplot()
```

<img src="02-Vis_files/figure-html/species-by-height-max-1.png" width="672" />

For more info, see the [forcats vignette](https://cran.r-project.org/web/packages/forcats/vignettes/forcats.html).

### Tweaking scales

A common request: scientific notation vs not. A few options:

1. Use different units. e.g., millions of people.


```r
gapminder::gapminder %>% 
  filter(country == "United States") %>% 
  ggplot(aes(x = year, y = pop / 1e6)) +
  geom_line() +
  labs(y = "Population (millions)")
```

<img src="02-Vis_files/figure-html/pop-millions-unit-1.png" width="672" />

2. Use `scale_y_continuous` with `labels = scales::comma`.


```r
gapminder::gapminder %>% 
  filter(country == "United States") %>% 
  ggplot(aes(x = year, y = pop)) +
  geom_line() +
  scale_y_continuous(labels = scales::comma) + 
  labs(y = "Population")
```

<img src="02-Vis_files/figure-html/pop-scales-comma-1.png" width="672" />

3. Use `scales::label_number` for even more control (see the help page).


```r
gapminder::gapminder %>% 
  filter(country == "United States") %>% 
  ggplot(aes(x = year, y = pop)) +
  geom_line() +
  scale_y_continuous(labels = scales::label_number(scale = 1e-6, suffix = "M")) + 
  labs(y = "Population")
```

<img src="02-Vis_files/figure-html/pop-label-number-1.png" width="672" />
