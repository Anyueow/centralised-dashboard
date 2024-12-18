from src.scraping.run_scraper import get_movie_data
from src.scraping.cache_manager import CacheManager
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("Script started...")
# Add more debug logs as needed to trace execution.

def main():
    cache = CacheManager()
    logging.debug("cache found")
    # Always get fresh data to ensure updates
    df = get_movie_data()
    logging.debug("found new data")
    cache.save_cache(df)
    logging.debug("Saved chached data")
    print("Cache updated successfully with new data:", df.shape)

if __name__ == "__main__":
    main()