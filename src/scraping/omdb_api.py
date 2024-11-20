import random
import streamlit as st
import requests
import os


class MovieDetailsFetcher:
    """
    A class to fetch movie details from the OMDb API.
    """

    def __init__(self, api_key=None):
        """
        Initializes the MovieDetailsFetcher with the given OMDb API key.
        If no API key is provided, it attempts to read from environment variable 'OMDB_API_KEY'.

        :param api_key: Your OMDb API key.
        """
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = st.secrets.get('OMDB_API_KEY')
            if not self.api_key:
                raise ValueError("OMDb API key not provided and 'OMDB_API_KEY' not set in st.secrets.")
        self.base_url = 'http://www.omdbapi.com/'

    def get_movie_details(self, movie_name):
        """
        Fetches movie details for the given movie name.

        :param movie_name: The name of the movie to search for.
        :return: A dictionary containing movie details or None if not found.
        """
        # URL-encode the movie name to handle spaces and special characters
        query = requests.utils.quote(movie_name)
        url = f'{self.base_url}?t={query}&apikey={self.api_key}'

        # Send a GET request to the OMDb API
        response = requests.get(url)
        data = response.json()

        # Check if the movie was found
        if data.get('Response') == 'True':
            # Extract ratings from the 'Ratings' list
            ratings = {}
            for rating in data.get('Ratings', []):
                source = rating.get('Source')
                value = rating.get('Value')
                ratings[source] = value

            # Extract Metascore and imdbRating
            metascore = data.get('Metascore', 'N/A')
            imdb_rating = data.get('imdbRating', 'N/A')
            imdb_votes = data.get('imdbVotes', 'N/A')

            # Extract and parse actors
            actors = data.get('Actors', '')
            actor_list = [actor.strip() for actor in actors.split(',')] if actors else []

            # Combine all ratings into a single dictionary
            all_ratings = {
                "Internet Movie Database": ratings.get('Internet Movie Database', 'N/A'),
                "Rotten Tomatoes": ratings.get('Rotten Tomatoes', 'N/A'),
                "Metacritic": ratings.get('Metacritic', 'N/A'),
                "Metascore": metascore,
                "imdbRating": imdb_rating,
                "imdbVotes": imdb_votes,
            }

            return {

                "Ratings": all_ratings,
                "Actors": actor_list,

            }
        else:
            print(f"Error: {data.get('Error')}")
            return None

if __name__ == "__main__":
    # List of random movies
    movie_list = [
        "Inception",
        "The Matrix",
        "Interstellar",
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Pulp Fiction",
        "Fight Club",
        "Forrest Gump",
        "The Lord of the Rings: The Return of the King",
        "Guardians of the Galaxy Vol. 2",
        "The Substance"  # As per your earlier example
    ]

    # Select a random movie
    random_movie = random.choice(movie_list)
    print(f"Selected Movie: {random_movie}")

    # Initialize the MovieDetailsFetcher
    try:
        fetcher = MovieDetailsFetcher()
    except ValueError as e:
        print(e)
        exit(1)

    # Fetch movie details
    details = fetcher.get_movie_details(random_movie)

    # Check if details were fetched successfully
    if details:
        print("\nMovie Details:")
        print(f"Title: {random_movie}")
        print("\nRatings:")
        for source, rating in details['Ratings'].items():
            print(f"  {source}: {rating}")
        print("\nActors:")
        for actor in details['Actors']:
            print(f"  {actor}")
    else:
        print("Movie details could not be retrieved.")