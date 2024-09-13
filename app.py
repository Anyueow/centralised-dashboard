import streamlit as st
import pandas as pd
from src.scraping.movie_deets import df

# Set page configuration for a fixed-width layout
st.set_page_config(layout="wide")

# Ensure score columns are numeric, converting strings to integers
df['Audience Score'] = pd.to_numeric(df['Audience Score'], errors='coerce').fillna(0).astype(int)
df['Critic Score'] = pd.to_numeric(df['Critic Score'], errors='coerce').fillna(0).astype(int)

# Add an 'Average Score' column (average of Audience and Critic Scores)
df['Average Score'] = (df['Audience Score'] + df['Critic Score']) / 2

# Style adjustments for table display
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            max-width: 100%;
            padding-top: 2rem;
        }
        table {
            table-layout: fixed;
            width: 100%;
        }
        td {
            word-wrap: break-word;
            white-space: normal;
        }
        thead th {
            background-color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("Most Popular / Trending Movie Details Scraped from Rotten Tomatoes")
st.markdown("Explore movies, filter by genre, search for specific movies, and see the top trending ones with high scores!")

# Flatten the genre list and extract unique genres
if 'Genres' in df.columns:
    all_genres = set()
    for genres in df['Genres']:
        if isinstance(genres, list):
            all_genres.update(genres)  # Flatten the lists of genres
        else:
            all_genres.add(genres)  # For single genres

    genre_options = sorted(all_genres)
    selected_genres = st.multiselect("Filter by Genre", options=genre_options, default=genre_options)
else:
    selected_genres = []

# Apply genre filter if 'Genre' column exists
if 'Genres' in df.columns and selected_genres:
    def filter_by_genre(genres):
        if isinstance(genres, list):
            return any(genre in genres for genre in selected_genres)
        return genres in selected_genres

    filtered_df = df[df['Genres'].apply(filter_by_genre)]
else:
    filtered_df = df.copy()

# Display the filtered movie data
st.subheader("Filtered Movie Data")
st.dataframe(filtered_df, height=600)  # Increased table height for better display

# Trending movies (with Average Score higher than 90)
trending_genres = df[df['Average Score'] > 90]

# Show trending movies in a chart
st.subheader("Trending Genres (Average Score > 90)")
if not trending_genres.empty:
    st.bar_chart(trending_genres[['Movie Name']].set_index('Movie Name'))
else:
    st.write("No trending genres with an average score higher than 90.")

# Display the DataFrame with Average Score included
st.subheader("Movie Data with Average Score")
st.dataframe(df, height=600)
