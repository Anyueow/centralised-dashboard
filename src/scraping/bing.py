import requests


def get_movie_details(movie_name, omdb_api_key):
    # URL-encode the movie name to handle spaces and special characters
    query = requests.utils.quote(movie_name)
    url = f'http://www.omdbapi.com/?t={query}&apikey={omdb_api_key}'

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
            "Title": data.get('Title', 'N/A'),
            "Year": data.get('Year', 'N/A'),
            "Ratings": all_ratings,
            "Actors": actor_list,
            "Plot": data.get('Plot', 'N/A'),
            "Genre": data.get('Genre', 'N/A'),
            "Runtime": data.get('Runtime', 'N/A'),
        }
    else:
        print(f"Error: {data.get('Error')}")
        return None


# Example usage:
if __name__ == "__main__":
    movie_name = input("Enter the movie name: ")
    omdb_api_key = '29168d77'  # Replace with your actual OMDb API key
    movie_details = get_movie_details(movie_name, omdb_api_key)
    if movie_details:
        print(f"\nTitle: {movie_details['Title']} ({movie_details['Year']})")
        print(f"Genre: {movie_details['Genre']}")
        print(f"Runtime: {movie_details['Runtime']}")
        print(f"Plot: {movie_details['Plot']}\n")

        print("Ratings:")
        for source, rating in movie_details['Ratings'].items():
            print(f"  {source}: {rating}")

        print("\nActors:")
        for actor in movie_details['Actors']:
            print(f"  {actor}")
    else:
        print("Movie details could not be retrieved.")
