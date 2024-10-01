# trend_data.py
import streamlit as st
from src.trends.run_trends_and_viz import run_trends

@st.cache_data
def get_trend_data(movie_titles):
    """
    Fetch Google Trends data for the given movie titles. Cached to avoid redundant fetching.
    """
    trends_df = run_trends(movie_titles)
    return trends_df
