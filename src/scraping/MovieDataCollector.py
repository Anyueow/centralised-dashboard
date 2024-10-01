import pandas as pd
import requests
from bs4 import BeautifulSoup


class MovieDataCollector:
    def __init__(self):
        self.movie_data = []

    def get_movie_data(self, movies):
        """
        Accepts a list of dictionaries where each dictionary contains 'title' and 'url'.
        """
        for movie in movies:
            title = movie['title']
            url = movie['url']

            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch details for {title}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Collect movie details
            movie_details = {
                "SNo": len(self.movie_data) + 1,
                "Movie Name": title.upper(),

                "Genres": self.get_genres(soup),

                "Synopsis": self.get_synopsis(soup),
                "Director": self.get_director(soup),
                "Rating": self.get_rating(soup),
                "Release Date (Theaters)": self.get_release_theatre(soup),
                "Release Date (Streaming)": self.get_release_streaming(soup),
                "Runtime": self.get_runtime(soup),
                "Box Office": self.get_box_office(soup)
            }

            print(f"Scraped details for {title}: {movie_details}")  # For debugging

            self.movie_data.append(movie_details)


    def get_synopsis(self, soup):
        try:
            return soup.find('div', class_='synopsis-wrap').find_all('rt-text')[-1].get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_director(self, soup):
        try:
            return soup.find('div', class_='category-wrap').find('rt-link').get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_rating(self, soup):
        try:
            return soup.find('rt-text', text='Rating').find_next('rt-text').get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_release_theatre(self, soup):
        try:
            return soup.find('rt-text', text='Release Date (Theaters)').find_next('rt-text').get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_release_streaming(self, soup):
        try:
            return soup.find('rt-text', text='Release Date (Streaming)').find_next('rt-text').get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_runtime(self, soup):
        try:
            return soup.find('rt-text', text='Runtime').find_next('rt-text').get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_box_office(self, soup):
        try:
            return soup.find('rt-text', text='Box Office (Gross USA)').find_next('rt-text').get_text(strip=True)
        except AttributeError:
            return "N/A"

    def get_genres(self, soup):
        try:
            genre_links = soup.find_all('rt-link', href=lambda href: href and 'genres' in href)
            return ', '.join([g.get_text(strip=True) for g in genre_links])
        except AttributeError:
            return "N/A"

    def to_dataframe(self):
        print(f"Collected movie data: {self.movie_data}")  # For debugging
        return pd.DataFrame(self.movie_data)
