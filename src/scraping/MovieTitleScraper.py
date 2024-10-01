import requests
from bs4 import BeautifulSoup

class MovieTitleScraper:
    def __init__(self, source_url=None):
        self.source_url = source_url
        self.movies = []

    def scrape_titles(self):
        if not self.source_url:
            raise ValueError("Source URL is not set")

        response = requests.get(self.source_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {self.source_url}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting movie titles and URLs based on the <a> tag with data-qa="discovery-media-list-item-caption"
        movie_tags = soup.find_all('a', attrs={'data-qa': 'discovery-media-list-item-caption'})

        for tag in movie_tags:
            try:
                title = tag.find('span', class_='p--small').get_text(strip=True)  # Extract the movie title
                url = tag['href']  # Extract the relative URL for the movie
                full_url = f"https://www.rottentomatoes.com{url}"
                self.movies.append({"title": title, "url": full_url})  # Append both title and full URL as a dictionary
            except Exception as e:
                print(f"Error extracting movie title or URL: {e}")

        return self.movies

    def get_titles_and_urls(self):
        return self.movies
