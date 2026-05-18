library(dplyr)

df <- read.csv("GoogleReview_data_cleaned.csv")

unique_locations <- unique(df$Location)

print(unique_locations)

df_Penang <- df %>% filter(Location == "Penang")

df_miri <- df %>% filter(Location == "Miri")

df <- read.csv("producer-prices_mys.csv")

unique_foods <- unique(df$Item)

print(unique_foods)
