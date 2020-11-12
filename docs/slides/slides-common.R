library(tidyverse)
library(knitr)
library(glue)

slideSetup <- function(mark_languages = FALSE) {
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
      ".tiny" = list("font-size" = "0.4rem"),
      ".small" = list("font-size" = "0.7rem"),
      ".large" = list("font-size" = "1.2rem"),
      ".white-pre" = list("white-space" = "pre"),
      "p" = list("padding" = 0, "margin" = 0),
      "h2, h3, h4" = list("margin" = "5px 0"),
      ".small-code .remark-code" = list("font-size" = "0.5rem"),
      ".floating-source" = list(
        "position" = "absolute",
        "left" = 0,
        "bottom" = 0,
    	  "z-index" = 100,
        "background" = "rgba(255,255,255,.75)",
        "font-size" = "1rem"
      )
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

    if (mark_languages) {
      append_extra_css("
/* Code chunks need to be positioned so that the language markers can float right. */
code.python, code.r {
  position: relative;
  padding-right: 30px; /* makes room for the language marker */
}

/* Here are the language markers. */
code.python::before {
  content: \"(py)\"; display: block; position: absolute; right: 0;
}

code.r::before {
  content: \"(r)\"; display: block; position: absolute; right: 0;
}

/* Also set different background colors. */
code.python { background-color: #f9f5ec !important; }
code.r {      background-color: #75aadb10 !important; }
", )
    }

}

append_extra_css <- function(css, outfile = "xaringan-themer.css") {
  css <- paste0(css, '\n\n')
  cat(css, file = outfile, append = TRUE, sep = "\n")
}
