import pandas as pd
import numpy as np


class MovieScorer:
    def __init__(self, movie_df):
        """
        Initializes the MovieScorer with a DataFrame containing movie data.

        movie_df: DataFrame containing columns for 'Movie Name', 'Audience Score',
                  'Critic Score', 'Google Trend Score', and 'Reddit Sentiment Score'.
        """
        self.movie_df = movie_df

    def normalize_score(self, score, min_val=0, max_val=100):
        """
        Normalizes a score to a 0-100 scale based on min and max values.
        If the score is NaN or falls outside the range, it is handled appropriately.
        """
        if pd.isna(score) or score < min_val:
            return min_val
        elif score > max_val:
            return max_val
        else:
            return (score - min_val) / (max_val - min_val) * 100

    def calculate_trend_score(self, row):
        """
        Calculates the trending score for a single row in the movie DataFrame.

        Weights:
        - Rotten Tomato Scores (40%)
        - Google Trends Score (30%)
        - Reddit Sentiment Score (30%)
        """
        # Normalize and calculate Rotten Tomatoes Score (Average of Audience and Critic)
        audience_score = self.normalize_score(row.get('Audience Score', np.nan), 0, 100)
        critic_score = self.normalize_score(row.get('Critic Score', np.nan), 0, 100)
        rotten_tomato_score = np.mean([audience_score, critic_score])

        # Normalize Google Trends Score (Recent average interest)
        google_trend_score = self.normalize_score(row.get('Google Trend Score', np.nan), 0, 100)

        # Normalize Reddit Sentiment Score
        reddit_sentiment_score = self.normalize_score(row.get('Reddit Sentiment Score', np.nan), 0, 100)

        # Calculate the weighted trending score
        trending_score = (
                (rotten_tomato_score * 0.4) +
                (google_trend_score * 0.3) +
                (reddit_sentiment_score * 0.3)
        )

        return round(trending_score, 2)

    def score_movies(self):
        """
        Applies the trend scoring function to each movie in the DataFrame and adds a new column.
        """
        self.movie_df['Trending Score'] = self.movie_df.apply(self.calculate_trend_score, axis=1)
        return self.movie_df[['Movie Name', 'Trending Score']]


# Example Usage
if __name__ == "__main__":
    # Sample movie data with some dummy scores
    sample_data = {
        'Movie Name': ['Movie A', 'Movie B', 'Movie C'],
        'Audience Score': [85, 70, 90],
        'Critic Score': [80, 60, 75],
        'Google Trend Score': [60, 50, 80],
        'Reddit Sentiment Score': [70, 55, 85]
    }

    # Create a DataFrame
    movie_df = pd.DataFrame(sample_data)

    # Initialize the scorer and calculate trending scores
    scorer = MovieScorer(movie_df)
    scored_df = scorer.score_movies()

    # Print out the scored movies
    print(scored_df)
