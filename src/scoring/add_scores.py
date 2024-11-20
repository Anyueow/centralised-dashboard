# add_scores.py

from src.scoring.scoring import MovieScorer

def add_scores(movie_df):
    """
    Adds trending scores to the movie DataFrame using the MovieScorer class.

    :param movie_df: DataFrame containing movie data including ratings and votes.
    :return: DataFrame with an additional 'Trending Score' column.
    """
    scorer = MovieScorer()
    scored_df = scorer.score_movies(movie_df)
    return scored_df
