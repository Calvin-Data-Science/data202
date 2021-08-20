Lab 09: Over-fitting
================

Data
----

We’ll again be using the Ames home sales dataset. Again, see [Data
dictionary](http://jse.amstat.org/v19n3/decock/DataDocumentation.txt).
And again, we use a subset of the original data as suggested by the
[original paper](http://jse.amstat.org/v19n3/decock.pdf).

We’ll also scale the sale price to be in units of $1000, to keep the
numbers more manageable.

    data(ames, package = "modeldata")
    ames_all <- ames %>%
      filter(Gr_Liv_Area < 4000, Sale_Condition == "Normal") %>%
      mutate(across(where(is.integer), as.double)) %>%
      mutate(Sale_Price = Sale_Price / 1000)
    rm(ames)

We’ll use the same train-test split that we have been using:

    set.seed(10) # Seed the random number generator
    ames_split <- initial_split(ames_all, prop = 2 / 3) # Split our data randomly
    ames_train <- training(ames_split)
    ames_test <- testing(ames_split)

Constructing Models
-------------------

### Visualizing the predictions in “data space”

Make a grid that roughly covers the city of Ames.

    lat_long_grid <- expand_grid(
      Latitude  = modelr::seq_range(ames_train$Latitude,  n = 200, expand = .05),
      Longitude = modelr::seq_range(ames_train$Longitude, n = 200, expand = .05),
    )

We start by defining a utility function that takes a data frame and adds
a model’s predictions onto it.

    add_predictions <- function(data, model, variable_name = ".pred", model_name = deparse(substitute(model))) {
      model %>%
        predict(data) %>%
        rename(!!enquo(variable_name) := .pred) %>%
        mutate(model = model_name) %>%
        bind_cols(data)
    }

And here’s another utility function, to show a model’s predictions:

    show_latlong_model <- function(dataset, model, model_name = deparse(substitute(model))) {
      ggplot(dataset, aes(x = Longitude, y = Latitude)) +
        geom_raster(
          data = lat_long_grid %>% add_predictions(model, model_name = model_name),
          mapping = aes(fill = .pred)
        ) +
        geom_point(aes(color = Sale_Price), size = .5) +
        scale_color_viridis_c(aesthetics = c("color", "fill")) +
        coord_equal() +
        labs(title = model_name)
    }

Validation
----------
