from src.scraping.MovieDataCollector import MovieDataCollector
from src.scraping.MovieTitleScraper import MovieTitleScraper

def run_scraper():
    """
    This function scrapes movie titles and URLs using the MovieTitleScraper class.
    Returns a list of scraped movies in the form of dictionaries (with title and URL).
    """
    source_url = "https://www.rottentomatoes.com/browse/movies_at_home/critics:certified_fresh~sort:popular"
    title_scraper = MovieTitleScraper(source_url)

    try:
        print("Scraping movie titles and URLs...")
        movies = title_scraper.scrape_titles()

        return movies
    except Exception as e:
        print(f"Error scraping movie titles: {e}")
        return None

def run_scraper_details(movies):
    """
    This function collects detailed information about each movie using the MovieDataCollector class.
    It requires a list of movies (with title and URL) as input.
    """
    if movies:
        movie_collector = MovieDataCollector()

        try:
            print("Collecting movie details...")
            movie_collector.get_movie_data(movies)
            movie_df = movie_collector.to_dataframe()

            # Output the data to console or save it as needed
            print(movie_df.info())  # Display dataframe information
            return movie_df  # Return the dataframe to be used later

        except Exception as e:
            print(f"Error collecting movie details: {e}")
            return None
    else:
        print("No movies scraped.")
        return None

# Example usage:
movies = run_scraper()  # Scrape movie titles and URLs
if movies is not None:
    movie_df = run_scraper_details(movies)  # Collect movie details
else:
    print("No movies scraped")
