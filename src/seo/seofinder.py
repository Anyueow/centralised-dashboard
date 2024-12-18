# MovieSEOKeywordService.py
import os
from serpapi import GoogleSearch
import constants

class SEOKeywordFinder:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_seo_keywords(self, title, num_keywords=2):
        params = {
            "engine": "google",
            "q": f"{title} movie",
            "api_key": self.api_key,
            "gl": "us",    # geo location
            "hl": "en"      # language
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        related_searches = results.get("related_searches", [])
        if not related_searches:
            # Fall back to related questions if no related searches
            related_questions = results.get("related_questions", [])
            possible_keywords = [q.get("question") for q in related_questions if "question" in q]
        else:
            possible_keywords = [search_item.get("query") for search_item in related_searches if "query" in search_item]

        # Clean and return top keywords
        possible_keywords = [kw for kw in possible_keywords if kw]
        return possible_keywords[:num_keywords]


class SEOKeywordService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.keyword_finder = SEOKeywordFinder(api_key)

    def get_keywords_for_movies(self, lst, num_keywords=5):
        """
        Given a list of movie names, return a dictionary keyed by movie title
        with a list of SEO keywords as values.
        """
        results = {}
        for title in lst:
            keywords = self.keyword_finder.get_seo_keywords(title, num_keywords=num_keywords)
            results[title] = keywords
        return results
