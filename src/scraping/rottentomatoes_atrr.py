import rottentomatoes as rt
from src.scraping.titles import title

test = title[1].lower().strip()

weighted_score = rt.weighted_score(test)


# Using an f-string to insert the variable into the URL
urlx = f"https://www.rottentomatoes.com/m/{test}#media-info"

print(urlx)
print(weighted_score)