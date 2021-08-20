
# Tools

## Useful Resources

* [Markdown Cheatsheet](https://commonmark.org/help/), [Tutorial](https://commonmark.org/help/tutorial/)
* [Getting Used to R, RStudio, and R Markdown](https://ismayc.github.io/rbasics-book/index.html): Screenshots and screencasts (with no audio)
* [Tidyverse Style Guide](https://style.tidyverse.org/index.html)

## Why these tools?

* R
  * It uses nouns and verbs where Python/Pandas uses syntax
  * Its operations map pretty cleanly onto generalizable concepts
  * It has an extensive library of useful packages
  * It plays well with Python
* Python
  * It's very commonly used.
  * It's extremely versatile.
  * It's reasonably fast.
* RMarkdown
  * It embodies reproducibility
  * ... which helps us practice integrity and humility.
* Git and GitHub
  * It helps us be hospitable to teammates and future readers
  * It's very commonly used.

## R and RStudio

### rstudio.calvin.edu

Your Calvin login and password should get you onto <https://rstudio.calvin.edu>

### RStudio on the Linux machines

R and RStudio are also installed on the Linux machines in the Maroon and Gold Labs.
They are accessible via <https://remote.cs.calvin.edu>.

### Rstudio on your own machine

You can download and install
[RStudio](https://rstudio.org/download/desktop)
and [R](http://cran.r-project.org/)
on your personal computer.


## R packages

You will need a number of R packages. We will have these installed for
your on <https://rstudio.calvin.edu>, but if you work on your own machine or on the Linux
lab machines, you will need to install these yourself.

Individual packages can be installed from within RStudio by clicking on the install icon
in the packages tab. Alternatively, you can run the following code from the command line.


```r
# make sure all current packages are up-to-date
update.packages()

pkgs <- c(
  "rmarkdown",
  "tidyverse",
  "ggformula",
  "plotly",
  "tidymodels",
  "pins",
  "reticulate",
  "mosaic",
  "devtools",
  "usethis",
  "keras",
  "nycflights13",
  "skimr",
  "timeDate",
  "qualtRics"
)

# skip package you already have to save time
pkgs <- setdiff(pkgs, installed.packages()[,1])

# install what's left
install.packages(pkgs)
```


We're additionally using these packages for development; they're optional for you.


```r
if (!("emo" %in% installed.packages()[, 1]))
  devtools::install_github("hadley/emo")
```

