Lab 1: Hello R
================
YOUR NAME HERE
TODAY’S DATE HERE

Packages and Data
=================

We’ll use the following packages:

    library(tidyverse) 
    library(usethis)

Read the data from the CSV

    # This file was initially created using:
    # write_csv(datasauRus::datasaurus_dozen, "datasaurus_dozen.csv")
    datasaurus_dozen <- read_csv(
      "datasaurus_dozen.csv",
      col_types = cols(
        dataset = col_factor(),
        x = col_double(),
        y = col_double()
      )
    )
