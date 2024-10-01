from src.trends.TrendVisualizer import TrendVisualizer
from src.trends.Trends import PyTrendScraper



def run_trends(movie_titles):
    """
    Fetch Google Trends data and visualize it for the provided movie titles.
    """
    # Step 1: Fetch Google Trends data using PyTrendScraper
    trend_scraper = PyTrendScraper(namelist=movie_titles)

    try:
        print("Fetching Google Trends data for movies...")
        trends_df = trend_scraper.get_trends()  # Get trends for the movies
        print(trends_df.head())  # Display a sample of the trends data

        if trends_df is not None and not trends_df.empty:
            # Step 2: Visualize the trends data using TrendVisualizer
            visualizer = TrendVisualizer(df=trends_df)
            figures = visualizer.visualize_trends()

            # Display the figures
            for fig in figures:
                fig.show()

    except Exception as e:
        print(f"Error fetching Google Trends data: {e}")
        return

