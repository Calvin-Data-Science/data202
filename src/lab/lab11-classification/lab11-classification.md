Lab 11: Classification
================

## Acquiring Data

``` r
data_filename <- "data/autism.csv"
if (!file.exists(data_filename)) {
  dir.create("data")
  download.file("https://doi.org/10.1371/journal.pcbi.1005385.s001", data_filename)
}
```

``` r
col_names <- names(read_csv(data_filename, n_max = 1, col_types = cols(.default = col_character())))
autism <- read_csv(data_filename, skip = 2, col_names = col_names, col_types = cols(
  .default = col_double(),
  Group = col_character()
))
```

``` python
autism = r.autism
```

## EDA

## Modeling
