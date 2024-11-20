import os
import pandas as pd
import streamlit as st
from anthropic import Anthropic
from datetime import datetime, timedelta

from src.scoring.add_scores import add_scores
from src.scraping.MovieDataCollector import MovieDataCollector
from src.scraping.MovieTitleScraper import MovieTitleScraper
from src.sentiment.x.grok_client import GrokClient
from src.scraping.omdb_api import MovieDetailsFetcher


class MovieDataProcessor:
    def __init__(self, cache_dir='./data_cache'):
        """
        Initialize the movie data processor with caching mechanism
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_file = os.path.join(cache_dir, 'movie_data_cache.pkl')

    def _is_cache_valid(self):
        """
        Check if the cached data is from today
        """
        if not os.path.exists(self.cache_file):
            return False

        # Get file modification time
        mod_time = datetime.fromtimestamp(os.path.getmtime(self.cache_file))
        return mod_time.date() == datetime.now().date()

    def _save_cache(self, dataframe):
        """
        Save the dataframe to a pickle file
        """
        dataframe.to_pickle(self.cache_file)

    def _load_cache(self):
        """
        Load the cached dataframe
        """
        return pd.read_pickle(self.cache_file)

    def get_movie_data(self):
        """
        Get movie data, using cache if available or scraping fresh data
        """
        # Check if cache exists and is valid
        if self._is_cache_valid():
            return self._load_cache()

        # Scrape new data
        movies = self._scrape_movie_titles()
        if not movies:
            # If scraping fails and no cache, raise an error
            raise ValueError("Could not scrape movie data and no cache available")

        # Collect and enrich movie data
        movie_df = self._collect_movie_details(movies)

        # Save to cache for future use
        self._save_cache(movie_df)

        return movie_df

    def _scrape_movie_titles(self):
        """
        Scrape movie titles from Rotten Tomatoes
        """
        source_url = "https://www.rottentomatoes.com/browse/movies_at_home/critics:certified_fresh~sort:popular"
        title_scraper = MovieTitleScraper(source_url)

        try:
            print("Scraping movie titles and URLs...")
            return title_scraper.scrape_titles()
        except Exception as e:
            print(f"Error scraping movie titles: {e}")
            return None

    def _collect_movie_details(self, movies):
        """
        Comprehensive method to collect and enrich movie details
        """
        if not movies:
            raise ValueError("No movies to process")

        # Collect basic movie data
        movie_collector = MovieDataCollector()
        movie_collector.get_movie_data(movies)
        movie_df = movie_collector.to_dataframe()

        # Add detailed movie information
        movie_df = self._add_movie_details(movie_df)

        # Add trending scores
        movie_df = add_scores(movie_df)

        # Add sentiment analysis
        movie_df = self._add_sentiment_analysis(movie_df)

        return movie_df

    def _add_movie_details(self, movie_df):
        """
        Add detailed movie information from OMDb
        """
        fetcher = MovieDetailsFetcher()
        details_columns = [
            'IMDb Rating', 'Rotten Tomatoes Rating',
            'Metacritic Rating', 'Metascore',
            'IMDb Votes', 'Actors'
        ]

        # Vectorized approach to fetch movie details
        def fetch_movie_details(movie_name):
            details = fetcher.get_movie_details(movie_name)
            if details:
                ratings = details.get('Ratings', {})
                return {
                    'IMDb Rating': ratings.get('imdbRating', 'N/A'),
                    'Rotten Tomatoes Rating': ratings.get('Rotten Tomatoes', 'N/A'),
                    'Metacritic Rating': ratings.get('Metacritic', 'N/A'),
                    'Metascore': ratings.get('Metascore', 'N/A'),
                    'IMDb Votes': ratings.get('imdbVotes', 'N/A'),
                    'Actors': ', '.join(details.get('Actors', []))
                }
            return {col: 'N/A' for col in details_columns}

        # Apply details fetching
        details_df = movie_df['Movie Name'].apply(fetch_movie_details).apply(pd.Series)

        # Combine original dataframe with new details
        return pd.concat([movie_df, details_df], axis=1)

    def _add_sentiment_analysis(self, movie_df):
        """
        Add sentiment analysis using Anthropic's Grok
        """
        # Initialize the Anthropic client with xAI's base URL
        api_key = st.secrets["XAI_API_KEY"]
        client = Anthropic(
            api_key=api_key,
            base_url="https://api.x.ai",
        )

        if client is None:
            raise ValueError("Failed to initialize Anthropic client")

        movie_titles = movie_df['Movie Name'].tolist()
        sentiment_df = GrokClient.process_movies(client, movie_titles)

        # Merge sentiment data
        return pd.merge(movie_df, sentiment_df, on='Movie Name', how='left')


def get_movie_data():
    """
    Wrapper function to get movie data, can be used in Streamlit
    """
    processor = MovieDataProcessor()
    return processor.get_movie_data()


if __name__ == "__main__":
    try:
        movie_df = get_movie_data()
        print("Enriched Movie DataFrame:")
        print(movie_df.head())
    except Exception as e:
        print(f"Error processing movie data: {e}")