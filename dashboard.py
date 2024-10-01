import streamlit as st
import pandas as pd
from run_scraper import run_scraper, run_scraper_details
from run_trends import run_trends
from trend_visualizer import TrendVisualizer


# Use Streamlit's caching to avoid re-scraping and re-fetching the same data
@st.cache_data
def get_movie_data():
    """
    Scrape movie data and return a DataFrame. Cached to avoid redundant scraping.
    """
    movies = run_scraper()
    run_scraper_details(movies)  # Populate details for the movies
    movie_df = pd.DataFrame(movies)

    # Clean and format movie data
    movie_df['Audience Score'] = pd.to_numeric(movie_df['Audience Score'], errors='coerce').fillna(0).astype(int)
    movie_df['Critic Score'] = pd.to_numeric(movie_df['Critic Score'], errors='coerce').fillna(0).astype(int)
    movie_df['Average Score'] = (movie_df['Audience Score'] + movie_df['Critic Score']) / 2
    movie_df['Release Date (Streaming)'] = pd.to_datetime(movie_df['Release Date (Streaming)'], errors='coerce').fillna(
        pd.NaT)
    movie_df['Release Date (Theaters)'] = pd.to_datetime(movie_df['Release Date (Theaters)'], errors='coerce').fillna(
        pd.NaT)

    for col in ['Movie Name', 'Director', 'Synopsis', 'Genres']:
        movie_df[col] = movie_df[col].fillna('N/A')

    return movie_df


@st.cache_data
def get_trend_data(movie_titles):
    """
    Fetch Google Trends data for the given movie titles. Cached to avoid redundant fetching.
    """
    trends_df = run_trends(movie_titles)
    return trends_df


def filter_movie_data(movie_df, selected_genres, start_date, end_date):
    """
    Apply genre and date filters to the movie DataFrame.
    """
    if selected_genres:
        filtered_df = movie_df[
            movie_df['Genres'].apply(lambda genres: any(genre in genres for genre in selected_genres))]
    else:
        filtered_df = movie_df.copy()

    filtered_df = filtered_df[
        (filtered_df['Release Date (Streaming)'] >= pd.to_datetime(start_date)) &
        (filtered_df['Release Date (Streaming)'] <= pd.to_datetime(end_date))
        ]

    return filtered_df


def display_movie_data_and_trends(filtered_df, trend_figures):
    """
    Display the movie details and corresponding trend data side-by-side using Streamlit columns.
    """
    for i, (index, row) in enumerate(filtered_df.iterrows()):
        col1, col2 = st.columns([2, 3])

        # Movie Details in first column
        with col1:
            st.markdown(f"### {row['Movie Name']}")
            st.markdown(f"**Director**: {row['Director']}")
            st.markdown(f"**Synopsis**: {row['Synopsis']}")
            st.markdown(f"**Genres**: {row['Genres']}")
            st.markdown(
                f"**Release Date (Theaters)**: {row['Release Date (Theaters)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Theaters)']) else 'N/A'}")
            st.markdown(
                f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")
            st.markdown(f"**Audience Score**: {row['Audience Score']}")
            st.markdown(f"**Critic Score**: {row['Critic Score']}")
            st.markdown(f"**Average Score**: {row['Average Score']}")

        # Trend Visualization in second column
        with col2:
            if i < len(trend_figures):
                st.plotly_chart(trend_figures[i], use_container_width=True)
            else:
                st.markdown("No trend data available for this movie.")

        # Divider between movies
        st.markdown("---")


def main():
    # Set page layout
    st.set_page_config(layout="wide")
    st.title("Direct TV SEO Movie Research Dashboard")
    st.markdown("By Ananya Shah for Cartesian Inc.")

    # Step 1: Fetch movie data (cached)
    movie_df = get_movie_data()

    # Step 2: Genre and date filtering
    all_genres = set(movie_df['Genres'].str.split(', ').sum())
    selected_genres = st.multiselect("Filter by Genre", options=sorted(all_genres), default=sorted(all_genres))

    start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))

    # Filter movie data based on user input
    filtered_df = filter_movie_data(movie_df, selected_genres, start_date, end_date)

    # Step 3: Fetch trends for filtered movies (cached)
    movie_titles = filtered_df['Movie Name'].tolist()
    trends_df = get_trend_data(movie_titles)

    # Step 4: Visualize trends
    if trends_df is not None:
        visualizer = TrendVisualizer(trends_df)
        trend_figures = visualizer.visualize_trends()
    else:
        trend_figures = []

    # Step 5: Display movie details and trends
    display_movie_data_and_trends(filtered_df, trend_figures)

    # Trending Movies Section
    st.subheader("Trending Movies (Average Score > 90)")
    trending_movies = movie_df[movie_df['Average Score'] > 90]
    display_movie_data_and_trends(trending_movies, trend_figures)


if __name__ == "__main__":
    main()
