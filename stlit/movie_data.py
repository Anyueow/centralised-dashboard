# movie_data.py
import pandas as pd
import streamlit as st
from src.scraping.run_scraper import run_scraper, run_scraper_details, add_sentiment_analysis

@st.cache_data
def get_movie_data():
    """
    Scrape movie data and return a DataFrame. Cached to avoid redundant scraping.
    """
    movies = run_scraper()
    details = run_scraper_details(movies)  # Populate details for the movies
    sent = add_sentiment_analysis(details)
    enriched = pd.DataFrame(sent)

    # Ensure 'Audience Score', 'Critic Score', and 'Average Score' are numeric


    enriched['Release Date (Streaming)'] = pd.to_datetime(enriched['Release Date (Streaming)'], errors='coerce').fillna(pd.NaT)
    enriched['Release Date (Theaters)'] = pd.to_datetime(enriched['Release Date (Theaters)'], errors='coerce').fillna(pd.NaT)

    for col in ['Movie Name', 'Director', 'Synopsis', 'Genres']:
        enriched[col] = enriched[col].fillna('N/A')

    return enriched
