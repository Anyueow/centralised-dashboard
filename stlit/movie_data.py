# movie_data.py
import pandas as pd
import streamlit as st
from src.scraping.run_scraper import run_scraper, run_scraper_details

@st.cache_data
def get_movie_data():
    """
    Scrape movie data and return a DataFrame. Cached to avoid redundant scraping.
    """
    movies = run_scraper()
    details = run_scraper_details(movies)  # Populate details for the movies
    movie_df = pd.DataFrame(details)

    # Ensure 'Audience Score', 'Critic Score', and 'Average Score' are numeric


    movie_df['Release Date (Streaming)'] = pd.to_datetime(movie_df['Release Date (Streaming)'], errors='coerce').fillna(pd.NaT)
    movie_df['Release Date (Theaters)'] = pd.to_datetime(movie_df['Release Date (Theaters)'], errors='coerce').fillna(pd.NaT)

    for col in ['Movie Name', 'Director', 'Synopsis', 'Genres']:
        movie_df[col] = movie_df[col].fillna('N/A')

    return movie_df
