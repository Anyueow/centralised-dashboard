import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta


def get_trends(input_data, column_name=None, timeframe='today 1-m'):
    """
    Fetch Google Trends data for a list of items or a DataFrame column.

    :param input_data: List of items or DataFrame containing items
    :param column_name: Name of the column in DataFrame (if input_data is a DataFrame)
    :param timeframe: Time frame for the trend data (default: 'today 1-m')
    :return: DataFrame containing trend data for all items
    """
    # Initialize pytrends
    pytrends = TrendReq(hl='en-US', tz=360)

    # Determine the list of items to search
    if isinstance(input_data, pd.DataFrame):
        if column_name is None:
            raise ValueError("column_name must be specified when input_data is a DataFrame")
        items = input_data[column_name].unique().tolist()
    elif isinstance(input_data, list):
        items = input_data
    else:
        raise ValueError("input_data must be either a DataFrame or a list")

    # Initialize a dictionary to store results
    results = {}

    # Fetch trends for each item
    for item in items:
        # Build payload
        pytrends.build_payload([item], timeframe=timeframe)

        # Get interest over time
        interest_over_time_df = pytrends.interest_over_time()

        # If we got results, add them to our results dictionary
        if not interest_over_time_df.empty:
            results[item] = interest_over_time_df[item]

    # Combine all results into a single DataFrame
    combined_df = pd.DataFrame(results)

    # Add isPartial column if it exists in the original data
    if 'isPartial' in interest_over_time_df.columns:
        combined_df['isPartial'] = interest_over_time_df['isPartial']

    return combined_df

# Assuming you have a dataframe named 'movies_df' with columns 'movie_name' and 'genre'
# Example usage:
