# movie_scorer.py

import pandas as pd
import numpy as np


class MovieScorer:
    """
    A class to calculate trending scores for movies based on various ratings and vote counts.
    """

    def __init__(self):
        """
        Initializes the MovieScorer.
        """
        pass  # No instance variables needed

    def normalize_score(self, score, current_min, current_max):
        """
        Normalizes a score to a 0-100 scale based on current min and max values.
        Handles NaN values and ensures the output is between 0 and 100.
        """
        try:
            score = float(score)
        except (ValueError, TypeError):
            return np.nan

        if pd.isna(score):
            return np.nan
        else:
            normalized = (score - current_min) / (current_max - current_min) * 100
            return np.clip(normalized, 0, 100)

    def normalize_votes(self, votes):
        """
        Normalizes the IMDb vote counts to a 0-100 scale.
        """
        try:
            # Remove commas and convert to integer
            votes = int(votes.replace(',', ''))
        except (ValueError, AttributeError):
            return np.nan

        # Define the min and max votes for normalization
        min_votes = 0
        max_votes = 1_000_000  # Adjust based on your dataset

        normalized = (votes - min_votes) / (max_votes - min_votes) * 100
        return np.clip(normalized, 0, 100)

    def process_ratings(self, row):
        """
        Processes and normalizes all ratings for a single row.
        """
        ratings = {}

        # IMDb Rating (scale of 0-10)
        imdb_rating = row.get('IMDb Rating', np.nan)
        imdb_normalized = self.normalize_score(imdb_rating, 0, 10)

        # Rotten Tomatoes Rating (percentage)
        rt_rating = row.get('Rotten Tomatoes Rating', np.nan)
        if isinstance(rt_rating, str) and rt_rating.endswith('%'):
            rt_rating = rt_rating.strip('%')
        rt_normalized = self.normalize_score(rt_rating, 0, 100)

        # Metacritic Rating (scale of 0-100 or formatted as '67/100')
        metacritic_rating = row.get('Metacritic Rating', np.nan)
        if isinstance(metacritic_rating, str) and '/' in metacritic_rating:
            metacritic_rating = metacritic_rating.split('/')[0]
        metacritic_normalized = self.normalize_score(metacritic_rating, 0, 100)

        # Metascore (scale of 0-100)
        metascore = row.get('Metascore', np.nan)
        metascore_normalized = self.normalize_score(metascore, 0, 100)

        # IMDb Votes (normalized)
        imdb_votes = row.get('IMDb Votes', np.nan)
        votes_normalized = self.normalize_votes(imdb_votes)

        # Collect normalized ratings
        ratings['IMDb'] = imdb_normalized
        ratings['Rotten Tomatoes'] = rt_normalized
        ratings['Metacritic'] = metacritic_normalized
        ratings['Metascore'] = metascore_normalized
        ratings['IMDb Votes'] = votes_normalized

        return ratings

    def calculate_trend_score(self, row):
        """
        Calculates the trending score for a single row in the movie DataFrame.

        Weights:
        - IMDb Rating (25%)
        - Rotten Tomatoes Rating (25%)
        - Metacritic Rating (15%)
        - IMDb Votes (25%)
        - Metascore (10%)
        """
        ratings = self.process_ratings(row)

        # Calculate weighted trending score
        components = [
            (ratings['IMDb'], 0.25),
            (ratings['Rotten Tomatoes'], 0.30),
            (ratings['Metacritic'], 0.15),
            (ratings['IMDb Votes'], 0.20),
            (ratings['Metascore'], 0.10),
        ]

        total_score = 0
        total_weight = 0
        for score, weight in components:
            if not pd.isna(score):
                total_score += score * weight
                total_weight += weight

        if total_weight > 0:
            trending_score = total_score / total_weight
            return round(trending_score, 2)
        else:
            return np.nan

    def score_movies(self, movie_df):
        """
        Applies the trend scoring function to each movie in the DataFrame and adds a new column.

        :param movie_df: DataFrame containing movie data.
        :return: DataFrame with the 'Trending Score' column added.
        """
        movie_df['Trending Score'] = movie_df.apply(self.calculate_trend_score, axis=1)
        return movie_df
