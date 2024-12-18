from src.scraping.wikipedia.client_wiki import WikipediaClient
from src.scraping.wikipedia.image_processor import ImageProcessor


class Wiki:
    def __init__(self):
        self.wiki_client = WikipediaClient()
        self.image_processor = ImageProcessor()

    def process_movie(self, title):
        try:
            page = self.wiki_client.get_page(title)
            if page:
                image_url = self.image_processor.extract_image_url(page)
                if image_url:
                    print(f"Main image URL for '{title}': {image_url}")
                    image = self.image_processor.fetch_and_resize_image(image_url)
                    if image:
                        image.show()
                    else:
                        print(f"Failed to process image for '{title}'.")
                else:
                    print(f"No valid image found for '{title}'.")
            else:
                print(f"No page found for '{title}'.")
        except Exception as e:
            print(f"An error occurred for '{title}': {e}")


if __name__ == "__main__":
    movies = ["Red One", "Gladiator"]
    movie_processor = MovieProcessor()

    for movie in movies:
        movie_processor.process_movie(movie)
