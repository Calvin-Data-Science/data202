library(conflicted)
conflicted::conflict_prefer("filter", "dplyr")

library(tidyverse)
library(knitr)
library(glue)

calvin_maroon <- "#8C2131"
calvin_gold <- "#F3CD00"
calvin_brightred <- "#C2002F"
calvin_renewblue <- "#71B1C8"
calvin_truegreen <- "#A2D683"

slideSetup <- function(mark_languages = FALSE) {
  muted <- scales::muted
  library(xaringanthemer)
  style_mono_accent(
    base_color = calvin_maroon,
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
      ".comfortable" = list("font-size" = "1.0rem"),
      ".large" = list("font-size" = "1.8rem"),
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
      ),
      # Improve table sizing (otherwise it's huge)
      ".remark-slide table" = list("font-size" = "0.8rem"),
      ".larger-table table" = list("font-size" = "1.0rem"),
      ".pagedtable-wrapper" = list("font-size" = "0.8rem"),
      ".pagedtable-header-type" = list("font-size" = "0.5rem"),

      # Blocks
      ".question" = list(
        "border-left" = glue("5px solid {muted(calvin_renewblue)}"),
        "padding" = "5px",
        "margin" = "10px",
        "background-color" = calvin_gold
      ),
      ".question p" = list(
        "margin" = "5px"
      ),
      ".scripture" = list(
        "max-width" = "80%",
        "margin" = "10px auto"
      ),
      ".scripture .remark-code" = list(
        "font-family" = '"Noto Sans", sans-serif',
        "font-size" = "1.4rem"
      ),
      ".scripture .ref" = list(
        "display" = "block",
        "margin-top" = "1rem",
        "text-align" = "right"
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

    cat(r"(
remark.macros.scale = function(w) {
  var url = this;
  return '<img src="' + url + '" style="width: ' + w + '" />';
};
remark.macros.maxheight = function(h) {
  var url = this;
  return '<img src="' + url + '" style="max-height: ' + h + '" />';
};
)", file = "macros.js", append = FALSE, sep = "\n")

}

append_extra_css <- function(css, outfile = "xaringan-themer.css") {
  css <- paste0(css, '\n\n')
  cat(css, file = outfile, append = TRUE, sep = "\n")
}
