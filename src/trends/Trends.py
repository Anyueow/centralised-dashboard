import polars as pl
from datetime import datetime, timedelta

# List of movie titles in Wikipedia format
movie_titles = [
    "Scarface_(1983_film)",
    "The_Godfather",
    "Inception",
    # Add more titles as needed
]

# Calculate start_date as 15 days before now
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=15)

hours_to_fetch = 15 * 24  # 15 days * 24 hours
all_views = []

for i in range(hours_to_fetch):
    # Get the target date for this hour
    current_hour = start_date + timedelta(hours=i)
    formatted = current_hour.strftime("%Y/%Y-%m/pageviews-%Y%m%d-%H0000")

    # Construct the URL for hourly pageview data
    url = f"https://dumps.wikimedia.org/other/pageviews/{formatted}.gz"

    # Read the hourly pageviews into a DataFrame
    try:
        wiki_views = (
            pl.read_csv(
                url,
                separator=" ",
                has_header=False,
                new_columns=["lang", "article", "views", "_"],
            )
            # Filter for English Wikipedia and view count > 4 if desired
            .filter(
                (pl.col("lang") == "en") & (pl.col("views") > 4)
            )
        )
    except Exception as e:
        print(f"[DEBUG] Could not fetch {url}: {e}")
        continue

    # Keep only rows for the movie titles we're interested in
    filtered_views = wiki_views.filter(pl.col("article").is_in(movie_titles))

    # If there are matches, append them to the list
    if filtered_views.shape[0] > 0:
        all_views.append(
            filtered_views.drop(["_"])
            .with_columns(pl.lit(current_hour).alias("date"))
        )

# Concatenate all hourly data into one DataFrame
if all_views:
    df = pl.concat(all_views)
else:
    df = pl.DataFrame({
        "lang": [],
        "article": [],
        "views": [],
        "date": []
    })

# Now you have hourly pageview data for the last 15 days
# For example, to see interest over time for "Scarface_(1983_film)":
scarface_data = df.filter(pl.col("article") == "Scarface_(1983_film)").sort("date")
print(scarface_data)

# You can also group by day to get daily aggregates if hourly granularity is too fine
daily_aggregates = (
    df.with_columns(pl.col("date").dt.truncate("1d"))
    .groupby(["article", "date"])
    .agg(pl.col("views").sum().alias("daily_views"))
    .sort(["article", "date"])
)
print(daily_aggregates)
