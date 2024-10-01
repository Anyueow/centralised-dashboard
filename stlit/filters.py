# filters.py
import pandas as pd

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
