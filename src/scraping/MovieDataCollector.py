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

            movie_details = {
                "SNo": len(self.movie_data) + 1,
                "Movie Name": title.upper(),
                "Audience Score": self.get_audience_score(soup),
                "Genres": self.get_genres(soup),
                "Critic Score": self.get_critic_score(soup),
                "Synopsis": self.get_synopsis(soup),
                "Director": self.get_director(soup),
                "Rating": self.get_rating(soup),
                "Release Date (Theaters)": self.get_release_theatre(soup),
                "Release Date (Streaming)": self.get_release_streaming(soup),
                "Runtime": self.get_runtime(soup),
                "Box Office": self.get_box_office(soup)
            }

            # Print the movie details for debugging
            print(f"Scraped details for {title}: {movie_details}")

            self.movie_data.append(movie_details)

    def get_audience_score(self, soup):
        try:
            score = soup.find('rt-text', attrs={'slot': 'audienceScore'}).get_text(strip=True)
            return score
        except Exception as e:
            print(f"Error fetching audience score: {e}")
            return "N/A"

    def get_critic_score(self, soup):
        try:
            score = soup.find('rt-text', attrs={'slot': 'criticsScore'}).get_text(strip=True)
            return score
        except Exception as e:
            print(f"Error fetching critic score: {e}")
            return "N/A"

    def get_synopsis(self, soup):
        try:
            synopsis = soup.find('div', class_='synopsis-wrap').find('rt-text').find_next_sibling('rt-text').get_text(
                strip=True)
            return synopsis
        except AttributeError:
            return "N/A"

    def get_director(self, soup):
        try:
            director = soup.find('div', class_='category-wrap').find('rt-link').get_text(strip=True)
            return director
        except AttributeError:
            return "N/A"

    def get_rating(self, soup):
        try:
            rating = soup.find('rt-text', text='Rating').find_next('rt-text').get_text(strip=True)
            return rating
        except AttributeError:
            return "N/A"

    def get_release_theatre(self, soup):
        try:
            release_theatre = soup.find('rt-text', text='Release Date (Theaters)').find_next('rt-text').get_text(
                strip=True)
            return release_theatre
        except AttributeError:
            return "N/A"

    def get_release_streaming(self, soup):
        try:
            release_streaming = soup.find('rt-text', text='Release Date (Streaming)').find_next('rt-text').get_text(
                strip=True)
            return release_streaming
        except AttributeError:
            return "N/A"

    def get_runtime(self, soup):
        try:
            runtime = soup.find('rt-text', text='Runtime').find_next('rt-text').get_text(strip=True)
            return runtime
        except AttributeError:
            return "N/A"

    def get_box_office(self, soup):
        try:
            box_office = soup.find('rt-text', text='Box Office (Gross USA)').find_next('rt-text').get_text(strip=True)
            return box_office
        except AttributeError:
            return "N/A"

    def get_genres(self, soup):
        try:
            genres = soup.find('span', class_='genre').get_text(strip=True)
            return genres
        except AttributeError:
            return "N/A"

    def to_dataframe(self):
        # Before returning, print the full movie_data list for debugging
        print(f"Collected movie data: {self.movie_data}")
        return pd.DataFrame(self.movie_data)
