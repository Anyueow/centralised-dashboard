import os
import pandas as pd
import streamlit as st
from anthropic import Anthropic
from datetime import datetime

import constants
from src.scoring.add_scores import add_scores
from src.scraping.MovieDataCollector import MovieDataCollector
from src.scraping.MovieTitleScraper import MovieTitleScraper
from src.sentiment.x.grok_client import GrokClient
from src.scraping.omdb_api import MovieDetailsFetcher
from src.seo.seofinder import SEOKeywordService


class MovieDataProcessor:
    def __init__(self):
        """
        Initialize the movie data processor without any caching mechanism.
        """
        pass

    def get_movie_data(self):
        """
        Get fresh movie data by scraping and processing every time.
        """
        movies = self._scrape_movie_titles()
        if not movies:
            raise ValueError("Could not scrape movie data.")

        movie_df = self._collect_movie_details(movies)
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


    # updating df
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

        # Extract movie titles once, reuse for sentiment and SEO
        movie_titles = movie_df['Movie Name'].tolist()

        # Add sentiment analysis
        movie_df = self._add_sentiment_analysis(movie_df, movie_titles)

        # Add SEO Keywords
        movie_df = self._add_seo_keywords(movie_df, movie_titles)


        return movie_df

    def _add_movie_details(self, movie_df):
        """
        Add detailed movie information from OMDb, including ratings, actors, awards, and poster.
        """
        fetcher = MovieDetailsFetcher()
        details_columns = [
            'IMDb Rating', 'Rotten Tomatoes Rating', 'Metacritic Rating', 'Metascore',
            'IMDb Votes', 'Actors', 'Awards', 'Poster'
        ]

        def fetch_movie_details(movie_name):
            details = fetcher.get_movie_details(movie_name)
            if details:
                ratings = details.get('Ratings', {})
                return {
                    'IMDb Rating': ratings.get('IMDb Rating', 'N/A'),
                    'Rotten Tomatoes Rating': ratings.get('Rotten Tomatoes', 'N/A'),
                    'Metacritic Rating': ratings.get('Metacritic', 'N/A'),
                    'Metascore': ratings.get('Metascore', 'N/A'),
                    'IMDb Votes': ratings.get('IMDb Votes', 'N/A'),
                    'Actors': ', '.join(details.get('Actors', [])),
                    'Awards': details.get('Awards', 'N/A'),
                    'Poster': details.get('Poster', 'N/A')  # Poster is the image URL
                }
            return {col: 'N/A' for col in details_columns}

        # Apply the fetch_movie_details function to each movie and expand the results into a DataFrame
        details_df = movie_df['Movie Name'].apply(fetch_movie_details).apply(pd.Series)
        return pd.concat([movie_df, details_df], axis=1)

    def _add_sentiment_analysis(self, movie_df, movie_titles):
        """
        Add sentiment analysis using Anthropic's Grok
        """
        api_key = st.secrets["XAI_API_KEY"]
        client = Anthropic(
            api_key=api_key,
            base_url="https://api.x.ai",
        )

        if client is None:
            raise ValueError("Failed to initialize Anthropic client")

        sentiment_df = GrokClient.process_movies(client, movie_titles)
        return pd.merge(movie_df, sentiment_df, on='Movie Name', how='left')

    def _add_seo_keywords(self, movie_df, movie_titles):
        """
        Add SEO Keywords to the movie DataFrame
        """
        serpapi_key = constants.SERPAPI
        seo_service = SEOKeywordService(api_key=serpapi_key)

        try:
            keywords_dict = seo_service.get_keywords_for_movies(movie_titles, num_keywords=4)

            # Convert keywords list to comma-separated string
            processed_keywords = {
                movie: ', '.join(keywords) for movie, keywords in keywords_dict.items()
            }

            # Create SEO Keywords DataFrame
            seo_df = pd.DataFrame.from_dict(processed_keywords, orient='index', columns=['SEO Keywords'])
            seo_df.index.name = 'Movie Name'
            seo_df.reset_index(inplace=True)

            # Merge with original DataFrame
            merged_df = movie_df.merge(seo_df, on='Movie Name', how='left')
            return merged_df

        except Exception as e:
            print(f"Error in SEO Keyword Processing: {e}")
            return movie_df



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
