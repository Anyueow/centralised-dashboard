import time
import pandas as pd
from pytrends.request import TrendReq

class PyTrendScraper:
    def __init__(self, namelist=None, timef='today 1-m'):
        self.namelist = namelist
        self.timef = timef
        self.results = {}

    def get_trends(self):
        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)

        # Fetch trends for each item with a delay to prevent rate limiting
        for item in self.namelist:
            # Build payload for the item
            pytrends.build_payload([item], timeframe=self.timef)

            # Get interest over time
            interest_over_time_df = pytrends.interest_over_time()

            # If we got results, add them to our results dictionary
            if not interest_over_time_df.empty:
                self.results[item] = interest_over_time_df[item]

            # Add a delay to avoid hitting the rate limit
            time.sleep(15)  # Adjust the delay as needed (e.g., 5 seconds)

        # Combine all results into a single DataFrame
        combined_df = pd.DataFrame(self.results)

        # Add isPartial column if it exists in the original data
        if not interest_over_time_df.empty and 'isPartial' in interest_over_time_df.columns:
            combined_df['isPartial'] = interest_over_time_df['isPartial']

        return combined_df
