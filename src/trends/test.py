from pytrends.request import TrendReq
from src.scraping.movie_deets import df

pytrends = TrendReq(hl='en-US', tz = 360)
keyword_list = ['thriller']
pytrends.build_payload(keyword_list, cat=0, timeframe='today 1-y', geo='', gprop='')