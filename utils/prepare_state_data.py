import pandas as pd
# Load CSV
csv_file = "../data/GoogleReview_data_cleaned.csv"
df = pd.read_csv(csv_file)
# Map cities to Malaysian states
location_to_state = {
    "Ipoh": "Perak",
    "Kuala Lumpur": "Kuala Lumpur",
    "George Town": "Penang",
    "Johor Bahru": "Johor",
    "Shah Alam": "Selangor",
    "Petaling Jaya": "Selangor",
    "Kota Kinabalu": "Sabah",
    "Kuching": "Sarawak",
    "Melaka": "Melaka",
    "Seremban": "Negeri Sembilan",
    "Alor Setar": "Kedah",
    "Kuantan": "Pahang",
    "Kuala Terengganu": "Terengganu",
    "Kota Bharu": "Kelantan",
    "Putrajaya": "Putrajaya",
    "Labuan": "Labuan",
    "JB" : "Johor",
    "KL" : "Kuala Lumpur",
    "Penang":"Penang",
    "Langkawi" : "Kedah",
    "Miri" : "Sarawak",

    }

# Convert locations into states
df["State"] = df["Location"].map(location_to_state)
# Remove rows without a matched state
df = df.dropna(subset=["State"])
# Aggregate ratings by state
state_summary = (
df.groupby("State")
.agg(
average_rating=("Rating", "mean"),
total_reviews=("Rating", "count")
)
.reset_index()
)
# Round ratings
state_summary["average_rating"] = state_summary["average_rating"].round(2)
# Save JSON for Vega-Lite
state_summary.to_json(
"malaysia_restaurant_ratings.json",
orient="records",
indent=2
)
print(state_summary)
print("\nSaved malaysia_restaurant_ratings.json")