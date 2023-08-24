# This code should get included using a code chunk like:
# {r setup, include=FALSE, code=xfun::read_utf8('../slide-setup.R')}
#
# That's important so that results are actually evaluated and printed into the Rmd.
# xaringinextra needs this, for example.

install_github_if_missing <- function(user, pkg) {
  # Approach from https://hohenfeld.is/posts/check-if-a-package-is-installed-in-r/
  if (!nzchar(system.file(package = pkg))) {
    remotes::install_github(paste0(user, "/", pkg))
  }
}
install_github_if_missing("gadenbuie", "countdown")
install_github_if_missing("gadenbuie", "xaringanExtra")
install_github_if_missing("hadley", "emo")

# Some manual imports
include_graphics <- knitr::include_graphics
kable <- knitr::kable
glue <- glue::glue

# Include styles.
local({
  linkifnotexist <- function(x) {
    if (!file.exists(x))
      invisible(file.symlink(paste0("../", x), x))
  }
  linkifnotexist("slides.css")
  linkifnotexist("xaringan-themer.css")
})

calvin_maroon <- "#8C2131"
calvin_gold <- "#F3CD00"
calvin_brightred <- "#C2002F"
calvin_renewblue <- "#71B1C8"
calvin_truegreen <- "#A2D683"

# Some borrowed from https://github.com/sta199-fa21-003/website/blob/master/static/slides/setup.Rmd
# Code setup.
library(conflicted)
conflict_prefer("filter", "dplyr", quiet = TRUE)
conflict_prefer("cols", "vroom", quiet = TRUE)
conflict_prefer("col_number", "vroom", quiet = TRUE)
set.seed(1234)

options(
  htmltools.dir.version = FALSE,
  dplyr.print_min = 6,
  dplyr.print_max = 6,
  tibble.width = 65,
  width = 65
)

# figure height, width, dpi
knitr::opts_chunk$set(echo = TRUE, comment = "",
                      fig.width = 8,
                      fig.asp = 0.618,
                      out.width = "90%",
                      fig.align = "center",
                      dpi = 300,
                      message = FALSE)
# ggplot2
ggplot2::theme_set(ggplot2::theme_bw(base_size = 16))

# fontawesome
htmltools::tagList(rmarkdown::html_dependency_font_awesome())


library(xaringanthemer)

style_mono_accent(
  base_color = calvin_maroon,
  blockquote_left_border_color = "#e9d968",    # yellow
  code_highlight_color = "#A7D5E8",            # light-blue
  code_inline_color = "#A7A7A7",               # gray
  table_border_color = "#8A8A8A",              # gray
  table_row_border_color = "#8A8A8A",          # gray
  table_row_even_background_color = "#A7D5E8",            # light-blue
  base_font_size = "28px",
  header_h1_font_size = "2rem",
  header_h2_font_size = "1.75rem",
  header_h3_font_size = "1.5rem",
  text_font_google = google_font("Source Sans Pro"),
  text_font_family = xaringanthemer_font_default("text_font_family"),
  text_font_weight = xaringanthemer_font_default("text_font_weight"),
  text_font_url = xaringanthemer_font_default("text_font_url"),
  text_font_family_fallback = xaringanthemer_font_default("text_font_family_fallback"),
  text_font_base = "sans-serif",
  code_font_google = google_font("Source Code Pro"),
  code_font_family = xaringanthemer_font_default("code_font_family"),
  code_font_size = "20px",
  code_font_url = xaringanthemer_font_default("code_font_url"),
  code_font_family_fallback = xaringanthemer_font_default("code_font_family_fallback"),
  outfile = "xaringan-themer.css"
)

library(xaringanExtra)
xaringanExtra::use_panelset(in_xaringan = TRUE)
xaringanExtra::use_tile_view()

# output number of lines
hook_output <- knitr::knit_hooks$get("output")
knitr::knit_hooks$set(output = function(x, options) {
  lines <- options$output.lines
  if (is.null(lines)) {
    return(hook_output(x, options))  # pass to default hook
  }
  x <- unlist(strsplit(x, "\n"))
  more <- "..."
  if (length(lines)==1) {        # first n lines
    if (length(x) > lines) {
      # truncate the output, but add ....
      x <- c(head(x, lines), more)
    }
  } else {
    x <- c(more, x[lines], more)
  }
  # paste these lines together
  x <- paste(c(x, ""), collapse = "\n")
  hook_output(x, options)
})
