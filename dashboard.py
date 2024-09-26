import streamlit as st
import pandas as pd
from src.scraping.movie_deets import movie_df
from src.trends.test import get_trends
from src.trends.trendviz import visualize_trends

# Set page configuration for a fixed-width layout
st.set_page_config(layout="wide")

# Fill missing values for key columns to avoid errors in display
movie_df['Audience Score'] = pd.to_numeric(movie_df['Audience Score'], errors='coerce').fillna(0).astype(int)
movie_df['Critic Score'] = pd.to_numeric(movie_df['Critic Score'], errors='coerce').fillna(0).astype(int)
movie_df['Average Score'] = (movie_df['Audience Score'] + movie_df['Critic Score']) / 2

# Convert 'Release Date (Streaming)' and 'Release Date (Theaters)' to datetime format and fill missing values
movie_df['Release Date (Streaming)'] = pd.to_datetime(movie_df['Release Date (Streaming)'], errors='coerce').fillna(pd.NaT)
movie_df['Release Date (Theaters)'] = pd.to_datetime(movie_df['Release Date (Theaters)'], errors='coerce').fillna(pd.NaT)

# Fill missing or null values for text columns with 'N/A'
for col in ['Movie Name', 'Director', 'Synopsis', 'Genres']:
    movie_df[col] = movie_df[col].fillna('N/A')

# Handle potential mixed types in the 'Director' and 'Genres' columns
movie_df['Director'] = movie_df['Director'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
movie_df['Genres'] = movie_df['Genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Title and description
st.title("Popular Movies Research Dashboard")
st.markdown("Made for Direct TV SEO Optimization project by Ananya Shah for Cartesian Inc.")

# Filter by genre (assuming you have a Genre column)
if 'Genres' in movie_df.columns:
    all_genres = set(movie_df['Genres'].str.split(', ').sum())
    genre_options = sorted(all_genres)
    selected_genres = st.multiselect("Filter by Genre", options=genre_options, default=genre_options)
else:
    selected_genres = []

# Filter by Release Date (Streaming)
st.markdown("### Filter by Release Date (Streaming)")
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

# Apply genre and Release Date (Streaming) filter
if selected_genres:
    filtered_df = movie_df[movie_df['Genres'].apply(lambda genres: any(genre in genres for genre in selected_genres))]
else:
    filtered_df = movie_df.copy()

filtered_df = filtered_df[
    (filtered_df['Release Date (Streaming)'] >= pd.to_datetime(start_date)) &
    (filtered_df['Release Date (Streaming)'] <= pd.to_datetime(end_date))
]

# Get trend data for movies in the filtered dataframe
movies_to_search = filtered_df['Movie Name'].tolist() # Assuming 'Movie Name' column exists in movie_df
print(movies_to_search)
try:
    movie_trends_df = get_trends(movies_to_search, 'Movies')  # Fetch trend data for filtered movies
    trend_figures = visualize_trends(movie_trends_df)  # Create visualizations for the movie trends
except Exception as e:
    st.error(f"Error fetching trends: {e}")
    trend_figures = []  # If trend fetching fails, set empty trend figures

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
        st.markdown(f"**Theater Release Date**: {row['Release Date (Theaters)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Theaters)']) else 'N/A'}")  # Theater release date
        st.markdown(f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")  # Streaming release date
        st.markdown(f"**Average Score**: {row['Average Score']}")
        st.markdown(f"**Genres**: {row['Genres']}")
        st.markdown(f"**Audience Score**: {row['Audience Score']}")
        st.markdown(f"**Critic Score**: {row['Critic Score']}")
        st.markdown(f"**Sentiment Analysis**: *...Feature Pending...*")

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
        st.markdown(f"**Theater Release Date**: {row['Release Date (Theaters)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Theaters)']) else 'N/A'}")  # Theater release date
        st.markdown(f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")  # Streaming release date
        st.markdown(f"**Average Score**: {row['Average Score']}")
        st.markdown(f"**Genres**: {row['Genres']}")
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
