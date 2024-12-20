import os
import pandas as pd

class CacheManager:
    def __init__(self, cache_dir='./data_cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_file = os.path.join(cache_dir, 'movie_data_cache.pkl')

    def is_cache_valid(self):
        """
        Check if the cache exists
        """
        return os.path.exists(self.cache_file)

    def save_cache(self, dataframe):
        """
        Save the dataframe to a pickle file
        """
        dataframe.to_pickle(self.cache_file)

    def load_cache(self):
        """
        Load the cached dataframe
        """
        return pd.read_pickle(self.cache_file)

# Usage example (if you want to use caching in another script):
# from cache_manager import CacheManager
# cache = CacheManager()
# if cache.is_cache_valid():
#     df = cache.load_cache()
# else:
#     df = get_movie_data()  # from movie_data_processor
#     cache.save_cache(df)