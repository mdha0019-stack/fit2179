df <- read.csv("GoogleReview_data_cleaned.csv")

unique_locations <- unique(df$Location)

print(unique_locations)
