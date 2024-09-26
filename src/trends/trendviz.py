import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.trends.test import get_trends


def visualize_trends(df):
    """
    Create separate plots for each movie/genre in the input DataFrame.

    :param df: DataFrame containing trend data, output from get_trends function
    :return: A list of Plotly figure objects
    """
    # Remove 'isPartial' column if it exists
    if 'isPartial' in df.columns:
        is_partial = df['isPartial']
        df = df.drop(columns=['isPartial'])
    else:
        is_partial = pd.Series([False] * len(df))

    # List to store all figures
    figures = []

    # Color for the line
    color = 'blue'

    # Create a separate plot for each movie/genre
    for column in df.columns:
        # Create the plot
        fig = go.Figure()

        # Add the main trend line
        fig.add_trace(
            go.Scatter(x=df.index, y=df[column], name="Search Interest",
                       line=dict(color=color))
        )

        # Add markers for partial data
        partial_data = df[is_partial]
        if not partial_data.empty:
            fig.add_trace(
                go.Scatter(x=partial_data.index, y=partial_data[column], name="Partial Data",
                           mode='markers', marker=dict(color='red', size=10, symbol='star'))
            )

        # Customize the layout
        fig.update_layout(
            title=f"Search Interest for '{column}' Over Time",
            xaxis_title="Date",
            yaxis_title="Relative Search Interest",
            legend_title="Legend",
            hovermode="x unified"
        )

        fig.update_yaxes(range=[0, 105])  # Set y-axis range from 0 to slightly above 100

        figures.append(fig)

    return figures
