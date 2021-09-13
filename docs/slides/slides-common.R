install_github_if_missing <- function(repo) {
  parts <- strsplit(repo, '/')[[1]]
  user <- parts[1]
  pkg <- parts[2]
  # Approach from https://hohenfeld.is/posts/check-if-a-package-is-installed-in-r/
  if (!nzchar(system.file(package = pkg))) {
    remotes::install_github(repo)
  }
}
install_github_if_missing("gadenbuie/countdown")
install_github_if_missing("gadenbuie/xaringanExtra")
install_github_if_missing("hadley/emo")

calvin_maroon <- "#8C2131"
calvin_gold <- "#F3CD00"
calvin_brightred <- "#C2002F"
calvin_renewblue <- "#71B1C8"
calvin_truegreen <- "#A2D683"

slideSetup <- function() {
  # Some borrowed from https://github.com/sta199-fa21-003/website/blob/master/static/slides/setup.Rmd
  # Code setup.
  library(conflicted)
  conflict_prefer("filter", "dplyr", quiet = TRUE)
  set.seed(1234)

  options(
    htmltools.dir.version = FALSE,
    dplyr.print_min = 6,
    dplyr.print_max = 6,
    tibble.width = 65,
    width = 65
  )

  # figure height, width, dpi
  knitr::opts_chunk$set(echo = TRUE,
                        fig.width = 8,
                        fig.asp = 0.618,
                        out.width = "60%",
                        fig.align = "center",
                        dpi = 300,
                        message = FALSE)
  # ggplot2
  ggplot2::theme_set(ggplot2::theme_gray(base_size = 16))

  # fontawesome
  htmltools::tagList(rmarkdown::html_dependency_font_awesome())


  muted <- scales::muted
  glue <- glue::glue


  library(xaringanthemer)

  style_solarized_dark(
    text_color = "#f6f6f6",                      # gray
    header_color = "#A7D5E8",                    # light-blue
    background_color = "#002b36",                # default bg color
    link_color = "#A7D5E8",                      # light-blue
    text_bold_color = "#E9AFA3",                 # pink
    code_highlight_color = "#A7D5E8",            # light-blue
    code_inline_color = "#A7A7A7",               # gray
    inverse_background_color = "#ffffff",        # white
    inverse_text_color = "#002b36",              # default bg color
    inverse_header_color = "#A7D5E8",            # light-blue
    title_slide_text_color = "#A7D5E8",          # light-blue
    title_slide_background_color = "#002b36",    # default bg color
    left_column_subtle_color = "#586e75",        # some gray
    left_column_selected_color = "#93a1a1",      # some lighter gray
    blockquote_left_border_color = "#e9d968",    # yellow
    table_border_color = "#8A8A8A",              # gray
    table_row_border_color = "#8A8A8A",          # gray
    table_row_even_background_color = "#004a5d", # slightly lighter dark-blue
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
    outfile = "../xaringan-themer.css"
  )

  #xaringanExtra::use_xaringan_extra(c(
  #  "tile_view", "animate_css", "editable", "tachyons", "panelset", "clipboard"))
  library(xaringanExtra)
  xaringanExtra::use_panelset(in_xaringan = TRUE)
  xaringanExtra::use_tile_view()
}
