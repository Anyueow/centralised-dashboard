import streamlit as st
import pandas as pd
from src.scraping.movie_deets import movie_df
from src.trends.test import get_trends
from src.trends.trendviz import visualize_trends

# Set page configuration for a fixed-width layout
st.set_page_config(layout="wide")

# Ensure score columns are numeric, converting strings to integers
movie_df['Audience Score'] = pd.to_numeric(movie_df['Audience Score'], errors='coerce').fillna(0).astype(int)
movie_df['Critic Score'] = pd.to_numeric(movie_df['Critic Score'], errors='coerce').fillna(0).astype(int)

# Add an 'Average Score' column (average of Audience and Critic Scores)
movie_df['Average Score'] = (movie_df['Audience Score'] + movie_df['Critic Score']) / 2

# Convert 'Release Date (Streaming)' to datetime format
movie_df['Release Date (Streaming)'] = pd.to_datetime(movie_df['Release Date (Streaming)'], errors='coerce')

# Handle potential mixed types in the 'Director' column
if 'Director' in movie_df.columns:
    movie_df['Director'] = movie_df['Director'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Title and description
st.title("Popular Movies Research Dashboard")
st.markdown(
    "Made for Direct TV SEO Optimization project by Ananya Shah for Cartesian Inc.")

# Filter by genre (assuming you have a Genre column)
if 'Genres' in movie_df.columns:
    all_genres = set()
    for genres in movie_df['Genres']:
        if isinstance(genres, list):
            all_genres.update(genres)
        else:
            all_genres.add(genres)

    genre_options = sorted(all_genres)
    selected_genres = st.multiselect("Filter by Genre", options=genre_options, default=genre_options)
else:
    selected_genres = []

# Filter by Release Date (Streaming)
st.markdown("### Filter by Release Date (Streaming)")
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

# Apply genre and Release Date (Streaming) filter if 'Genres' and 'Release Date (Streaming)' columns exist
if 'Genres' in movie_df.columns and selected_genres:
    def filter_by_genre(genres):
        if isinstance(genres, list):
            return any(genre in genres for genre in selected_genres)
        return genres in selected_genres


    filtered_df = movie_df[movie_df['Genres'].apply(filter_by_genre)]
else:
    filtered_df = movie_df.copy()

# Apply the Release Date (Streaming) filter
if 'Release Date (Streaming)' in movie_df.columns:
    filtered_df = filtered_df[
        (filtered_df['Release Date (Streaming)'] >= pd.to_datetime(start_date)) &
        (filtered_df['Release Date (Streaming)'] <= pd.to_datetime(end_date))
        ]

# Get trend data for movies in the filtered dataframe
movies_to_search = filtered_df['Movie Name'].tolist()  # Assuming 'Movie Name' column exists in movie_df
movie_trends_df = get_trends(movies_to_search, 'Movies')  # Fetch trend data for filtered movies

# Create visualizations for the movie trends
trend_figures = visualize_trends(movie_trends_df)

# Display movie information and trend graphs in blocks
st.subheader("Movies and Trends")

for i, (index, row) in enumerate(filtered_df.iterrows()):
    # Create a block layout using columns
    col1, col2 = st.columns([2, 3])  # Adjusted to two columns

    # Movie name, synopsis, and director in the first column
    with col1:
        st.markdown(f"### {row['Movie Name']}")
        st.markdown(f"**Director**: {row['Director']}")
        st.markdown(f"**Synopsis**: {row['Synopsis']}")  # Display synopsis
        st.markdown(f"**Theater Release Date**: {row['Release Date (Theaters)']}")  # Display theater release date
        st.markdown(
            f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")  # Release Date (Streaming)
        st.markdown(f"**Average Score**: {row['Average Score']}")
        st.markdown(f"**Genres**: {', '.join(row['Genres']) if isinstance(row['Genres'], list) else row['Genres']}")
        st.markdown(f"**Audience Score**: {row['Audience Score']}")
        st.markdown(f"**Critic Score**: {row['Critic Score']}")
        st.markdown(f"**Sentiment Analysis**: *...Feature Pending....*")

    # Trend graph in the second column
    with col2:
        if i < len(trend_figures):
            st.plotly_chart(trend_figures[i], use_container_width=True)  # Display the plotly graph within the column
        else:
            st.markdown("No trend data available.")

    # Horizontal divider between movies
    st.markdown("---")

# Trending movies section (with Average Score higher than 90)
st.subheader("Trending movies (with Average Score higher than 90)")
trending_movies = movie_df[movie_df['Average Score'] > 90]

# Display the trending movies in blocks as well
for i, (index, row) in enumerate(trending_movies.iterrows()):
    col1, col2 = st.columns([2, 3])  # Adjusted to two columns

    # Movie name, synopsis, and director in the first column
    with col1:
        st.markdown(f"### {row['Movie Name']}")
        st.markdown(f"**Director**: {row['Director']}")
        st.markdown(f"**Synopsis**: {row['Synopsis']}")  # Display synopsis
        st.markdown(f"**Theater Release Date**: {row['Theater Release Date']}")  # Display theater release date
        st.markdown(
            f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")  # Release Date (Streaming)
        st.markdown(f"**Average Score**: {row['Average Score']}")
        st.markdown(f"**Genres**: {', '.join(row['Genres']) if isinstance(row['Genres'], list) else row['Genres']}")
        st.markdown(f"**Audience Score**: {row['Audience Score']}")
        st.markdown(f"**Critic Score**: {row['Critic Score']}")
        st.markdown(f"**Sentiment Analysis**: Positive")

    # Trend graph in the second column
    with col2:
        if i < len(trend_figures):
            st.plotly_chart(trend_figures[i], use_container_width=True)  # Display the plotly graph within the column
        else:
            st.markdown("No trend data available.")

    # Horizontal divider between movies
    st.markdown("---")
