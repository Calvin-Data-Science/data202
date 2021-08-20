# remotes::install_github('yihui/xaringan')
# remotes::install_github("gadenbuie/countdown")
# remotes::install_github("gadenbuie/xaringanExtra")

calvin_maroon <- "#8C2131"
calvin_gold <- "#F3CD00"
calvin_brightred <- "#C2002F"
calvin_renewblue <- "#71B1C8"
calvin_truegreen <- "#A2D683"

slideSetup <- function(mark_languages = FALSE) {
  muted <- scales::muted
  glue <- glue::glue
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

  xaringanExtra::use_xaringan_extra(c("tile_view", "animate_css", "editable", "tachyons"))


}
