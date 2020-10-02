library(tidyverse)

slideSetup <- function() {
  library(xaringanthemer)
  style_mono_accent(
  #  base_color = "#1c5253",
    base_color = "#8C2131",
    #header_font_google = google_font("Josefin Sans"),
    #text_font_google   = google_font("Montserrat", "300", "300i"),
    #text_font_google =   google_font("Domine"),
    code_font_google   = google_font("Fira Mono"),
    header_h1_font_size = "2.75rem",
    header_h2_font_size = "2.5rem",
    text_font_size = "1.5rem",
    code_highlight_color = "#A7D5E8",
    padding = "6px 64px 6px 64px"
  )
  style_extra_css(list(
      ".tiny" = list("font-size" = "40%"),
      ".small" = list("font-size" = "70%"),
      ".large" = list("font-size" = "120%"),
      ".white-pre" = list("white-space" = "pre"),
      "p" = list("padding" = 0, "margin" = 0),
      "h2" = list("margin" = "5px 0")
  ))

  # Below here from dsbox
  # https://github.com/rstudio-education/datascience-box/blob/master/course-materials/slides/setup.Rmd

  options(
    htmltools.dir.version = FALSE,
    dplyr.print_min = 6,
    dplyr.print_max = 6,
    width = 100
  )

    # figure height, width, dpi
  knitr::opts_chunk$set(echo = TRUE,
                        fig.width = 6,
                        fig.asp = 0.5,
                        out.width = "100%",
                        fig.align = "center",
                        dpi = 300,
                        message = FALSE)

    set.seed(1234)
}
