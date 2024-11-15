import pandas as pd
import streamlit as st
from anthropic import Anthropic

from src.scraping.MovieDataCollector import MovieDataCollector
from src.scraping.MovieTitleScraper import MovieTitleScraper
from src.sentiment.x.grok_client import GrokClient

def run_scraper():
    """
    This function scrapes movie titles and URLs using the MovieTitleScraper class.
    Returns a list of scraped movies in the form of dictionaries (with title and URL).
    """
    source_url = "https://www.rottentomatoes.com/browse/movies_at_home/critics:certified_fresh~sort:popular"
    title_scraper = MovieTitleScraper(source_url)

    try:
        print("Scraping movie titles and URLs...")
        movies = title_scraper.scrape_titles()

        return movies
    except Exception as e:
        print(f"Error scraping movie titles: {e}")
        return None

def run_scraper_details(movies):
    """
    This function collects detailed information about each movie using the MovieDataCollector class.
    It requires a list of movies (with title and URL) as input.
    """
    if movies:
        movie_collector = MovieDataCollector()

        try:
            movie_collector.get_movie_data(movies)
            movie_df = movie_collector.to_dataframe()


            return movie_df  # Return the dataframe to be used later

        except Exception as e:
            print(f"Error collecting movie details: {e}")
            return None
    else:
        print("No movies scraped.")
        return None


def add_sentiment_analysis(movie_df):
    # Initialize the Anthropic client with xAI's base URL
    api_key = st.secrets["XAI_API_KEY"]

    client = Anthropic(
        api_key=api_key,
        base_url="https://api.x.ai",
    )
    if client is None:
        st.stop()  # Stop execution if client initialization fails

    movie_titles = movie_df['Movie Name'].tolist()
    sentiment_df = GrokClient.process_movies(client, movie_titles)

    enriched_movie_df = pd.merge(movie_df, sentiment_df, on='Movie Name', how='left')
    return enriched_movie_df


if __name__ == "__main__":
    movies = run_scraper()
    if movies is not None:
        movie_df = run_scraper_details(movies)
        if movie_df is not None:

            enriched_movie_df = add_sentiment_analysis(movie_df)
            print("Enriched Movie DataFrame:")
            print(enriched_movie_df.head())
    else:
        print("No movies scraped.")