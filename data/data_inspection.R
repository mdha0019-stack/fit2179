library(dplyr)
library(stringr)

df <- read.csv("GoogleReview_data_cleaned.csv")

unique_locations <- unique(df$Location)

print(unique_locations)

df_Penang <- df %>% filter(Location == "Penang")

df_miri <- df %>% filter(Location == "Miri")

df_p <- read.csv("producer-prices_mys.csv")

unique_foods <- unique(df_p$Item)

print(unique_foods)

df_trip <- read.csv("TripAdvisor_data_cleaned.csv")
unique_locations_trip <- unique(df_trip$Location)

df_nandos <- df_trip %>%
  filter(str_detect(Restaurant, regex("nandos", ignore_case = TRUE)))

top10_restaurants_trip <- df_trip %>%
  group_by(Restaurant) %>%
  summarise(ReviewCount = n()) %>%
  arrange(desc(ReviewCount)) %>%
  slice_head(n = 50)

top10_restaurants_trip

top10_restaurants_google <- df %>%
  group_by(Restaurant) %>%
  summarise(ReviewCount = n())%>%
  arrange(desc(ReviewCount)) %>%
  slice_head(n = 50)

top10_restaurants_google

top10_comparison <- df %>%
  filter(Restaurant %in% top10_restaurants_trip$Restaurant) %>%
  group_by(Restaurant) %>%
  summarise(GoogleReviewCount = n())

top10_comparison

# Summarise TripAdvisor data
trip_summary <- df_trip %>%
  group_by(Restaurant, Location) %>%
  summarise(
    T_Reviews = n(),                # count of reviews
    T_Rating  = mean(Rating, na.rm = TRUE),  # average rating
    .groups = "drop"
  )

# Summarise Google data
google_summary <- df %>%
  group_by(Restaurant, Location) %>%
  summarise(
    G_Reviews = n(),
    G_Rating  = mean(Rating, na.rm = TRUE),
    .groups = "drop"
  )

# Inner join by Restaurant + Location
comparison <- trip_summary %>%
  inner_join(google_summary, by = c("Restaurant", "Location"))

comparison

# Base R option
write.csv(comparison, "TripAdvisor_Google_Comparison.csv", row.names = FALSE)

# Or with readr (tidyverse)
library(readr)
write_csv(comparison, "TripAdvisor_Google_Comparison.csv")


df_survey <- read.csv("food_survey.csv")

df_p_2022 <- df_p %>% filter(Year == "2022")
