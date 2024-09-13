import requests
from bs4 import BeautifulSoup

# Rotten Tomatoes trending page URL
url = "https://www.rottentomatoes.com/browse/movies_at_home/critics:certified_fresh~sort:popular"

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# print(type(soup))

title = []

# Extract movie titles
for movie in soup.find_all('span', {'data-qa': 'discovery-media-list-item-title'}):
    t = movie.get_text(strip=True)
    title.append(t)
# storin
print(title)
