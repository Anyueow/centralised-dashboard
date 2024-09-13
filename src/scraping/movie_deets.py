import pandas as pd
import requests
import rottentomatoes as rt
from bs4 import BeautifulSoup

from src.scraping.titles import title

# List to hold all movie data
movie_data = []


def a_error(movie_title):
    movie_title = rt.audience_score()
    if movie_title == "error detected":
        raise ValueError("invalid literal for int() with base 10: ''")
    return 'NA'  # Example score


for t in title:

    test = t.lower().strip()
    print(test)
    try:
        audience_score = rt.audience_score(test)
    except Exception as e:
        audience_score = "N/AA"
        print(f"Error fetching audience score for {test}: {e}")

    try:
        critic_score = rt.tomatometer(test)
    except Exception as e:
        critic_score = "N/A"
        print(f"Error fetching critic score for {test}: {e}")

    test_url = t.lower().strip().replace(' ', '_')
    print(test_url)
    # Using an f-string to insert the variable into the URL
    url = f"https://www.rottentomatoes.com/m/{test}#media-info"

    # Fetch the page content
    response = requests.get(url)
    soup2 = BeautifulSoup(response.text, 'html.parser')

    # Extracting the required details
    try:
        synopsis = soup2.find('div', class_='synopsis-wrap').find('rt-text').find_next_sibling('rt-text').get_text(
            strip=True)
    except AttributeError:
        synopsis = "N/A"

    try:
        director = soup2.find('div', class_='category-wrap').find('rt-link').get_text(strip=True)
    except AttributeError:
        director = "N/A"

    try:
        rating = soup2.find('rt-text', text='Rating').find_next('rt-text').get_text(strip=True)
    except AttributeError:
        rating = "N/A"

    try:
        release_theatre = soup2.find('rt-text', text='Release Date (Theaters)').find_next('rt-text').get_text(
            strip=True)
    except AttributeError:
        release_theatre = "N/A"

    try:
        release_streaming = soup2.find('rt-text', text='Release Date (Streaming)').find_next('rt-text').get_text(
            strip=True)
    except AttributeError:
        release_streaming = "N/A"

    try:
        runtime = soup2.find('rt-text', text='Runtime').find_next('rt-text').get_text(strip=True)
    except AttributeError:
        runtime = "N/A"

    try:
        box_office = soup2.find('rt-text', text='Box Office (Gross USA)').find_next('rt-text').get_text(strip=True)
    except AttributeError:
        box_office = "N/A"

    # Appending movie data to the list
    movie_data.append({
        "SNo": len(movie_data) + 1,
        "Movie Name": t,
        "Audience Score": audience_score,
        "Critic Score": critic_score,
        "Synopsis": synopsis,
        "Director": director,
        "Rating": rating,
        "Release Date (Theaters)": release_theatre,
        "Release Date (Streaming)": release_streaming,
        "Runtime": runtime,
        "Box Office": box_office
    })

# Creating a DataFrame from the movie data
df = pd.DataFrame(movie_data)

print(df.head())
