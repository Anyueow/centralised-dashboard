import pandas as pd
import plotly.graph_objects as go


class TrendVisualizer:
    def __init__(self, df):
        """
        Initialize the TrendVisualizer with a DataFrame.

        :param df: DataFrame containing trend data.
        """
        self.df = df
        self.figures = []

    def preprocess_data(self):
        """
        Preprocess the input DataFrame by removing the 'isPartial' column if it exists.

        :return: A tuple of DataFrame (cleaned) and isPartial series.
        """
        if 'isPartial' in self.df.columns:
            is_partial = self.df['isPartial']
            self.df = self.df.drop(columns=['isPartial'])
        else:
            is_partial = pd.Series([False] * len(self.df))

        return self.df, is_partial

    def visualize_trends(self):
        """
        Create separate plots for each movie/genre in the input DataFrame.

        :return: A list of Plotly figure objects.
        """
        # Preprocess the data
        df, is_partial = self.preprocess_data()

        # Create a separate plot for each movie/genre
        for column in df.columns:
            # Create the plot
            fig = go.Figure()

            # Add the main trend line
            fig.add_trace(
                go.Scatter(x=df.index, y=df[column], name="Search Interest",
                           line=dict(color='blue'))  # Default line color
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

            # Store the figure in the list of figures
            self.figures.append(fig)

        return self.figures
