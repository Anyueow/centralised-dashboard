import streamlit as st
import pandas as pd
from src.scraping.movie_deets import df
from src.trends.test import get_trends
from src.trends.trendviz import visualize_trends

# Set page configuration for a fixed-width layout
st.set_page_config(layout="wide")

# Ensure score columns are numeric, converting strings to integers
df['Audience Score'] = pd.to_numeric(df['Audience Score'], errors='coerce').fillna(0).astype(int)
df['Critic Score'] = pd.to_numeric(df['Critic Score'], errors='coerce').fillna(0).astype(int)

# Add an 'Average Score' column (average of Audience and Critic Scores)
df['Average Score'] = (df['Audience Score'] + df['Critic Score']) / 2

# Handle potential mixed types in the 'Director' column
if 'Director' in df.columns:
    df['Director'] = df['Director'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Title and description
st.title("Popular and trending movies scraped from Rotten Tomatoes")
st.markdown(
    "Explore movies, filter by genre, search for specific movies, and see the top trending ones with high scores!")

# Filter by genre (assuming you have a Genre column)
if 'Genres' in df.columns:
    all_genres = set()
    for genres in df['Genres']:
        if isinstance(genres, list):
            all_genres.update(genres)
        else:
            all_genres.add(genres)

    genre_options = sorted(all_genres)
    selected_genres = st.multiselect("Filter by Genre", options=genre_options, default=genre_options)
else:
    selected_genres = []

# Apply genre filter if 'Genres' column exists
if 'Genres' in df.columns and selected_genres:
    def filter_by_genre(genres):
        if isinstance(genres, list):
            return any(genre in genres for genre in selected_genres)
        return genres in selected_genres


    filtered_df = df[df['Genres'].apply(filter_by_genre)]
else:
    filtered_df = df.copy()

# Get trend data for movies in the filtered dataframe
movies_to_search = filtered_df['Movie Name'].tolist()  # Assuming 'Movie Name' column exists in df
movie_trends_df = get_trends(movies_to_search, 'Movies')  # Fetch trend data for filtered movies

# Create visualizations for the movie trends
trend_figures = visualize_trends(movie_trends_df)

# Display movie information and trend graphs in blocks
st.subheader("Movies and Trends")

for i, (index, row) in enumerate(filtered_df.iterrows()):
    # Create a block layout using columns
    col1, col2, col3 = st.columns([2, 3, 2])

    # Movie name and director in the first column
    with col1:
        st.markdown(f"### {row['Movie Name']}")
        st.markdown(f"**Director**: {row['Director']}")
        st.markdown(f"**Average Score**: {row['Average Score']}")
        st.markdown(f"**Genres**: {', '.join(row['Genres']) if isinstance(row['Genres'], list) else row['Genres']}")

    # Sentiment analysis and scores in the second column
    with col2:
        st.markdown(f"**Audience Score**: {row['Audience Score']}")
        st.markdown(f"**Critic Score**: {row['Critic Score']}")
        st.markdown(f"**Sentiment Analysis**: Positive")
        st.markdown(f"**Trends**: See graph on the right.")

    # Trend graph in the third column
    with col3:
        if i < len(trend_figures):
            st.plotly_chart(trend_figures[i], use_container_width=True)
        else:
            st.markdown("No trend data available.")

    # Horizontal divider between movies
    st.markdown("---")

# Trending movies section (with Average Score higher than 90)
st.subheader("Trending movies (with Average Score higher than 90)")
trending_movies = df[df['Average Score'] > 90]

# Display the trending movies in blocks as well
for i, (index, row) in enumerate(trending_movies.iterrows()):
    col1, col2, col3 = st.columns([2, 3, 2])

    # Movie name and director in the first column
    with col1:
        st.markdown(f"### {row['Movie Name']}")
        st.markdown(f"**Director**: {row['Director']}")
        st.markdown(f"**Average Score**: {row['Average Score']}")

    # Sentiment analysis and trends in the second column
    with col2:
        st.markdown(f"**Audience Score**: {row['Audience Score']}")
        st.markdown(f"**Critic Score**: {row['Critic Score']}")
        st.markdown(f"**Sentiment Analysis**: Positive")
        st.markdown(f"**Trends**: See graph on the right.")

    # Trend graph in the third column
    with col3:
        if i < len(trend_figures):
            st.plotly_chart(trend_figures[i], use_container_width=True)
        else:
            st.markdown("No trend data available.")

    # Horizontal divider between movies
    st.markdown("---")
