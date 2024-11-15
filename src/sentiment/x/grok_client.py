# grok_client.py

import pandas as pd
from anthropic import Anthropic
import streamlit as st


import pandas as pd
import streamlit as st
from anthropic import Anthropic

class GrokClient:


    @staticmethod
    def extract_main_actor(client, movie_title: str) -> str:
        """
        Extracts the main actor of the given movie using Grok's capabilities.
        """

        prompt = f"Who is the main actor in the movie '{movie_title}'?"
        response = client.completions.create(
            model="grok-beta",
            prompt=prompt,
            max_tokens_to_sample=100  # Correct parameter
        )
        return response.completion.strip()

    @staticmethod
    def analyze_sentiment(client, movie_title: str, actor_name: str) -> str:
        """
        Analyzes current user sentiment on X about the given movie and its main actor.
        """
        prompt = (
           f"What are users on X saying about the movie '{movie_title}' and its main actor"
           f" '{actor_name}' right now? Please provide a sentiment overview."

        )
        response = client.completions.create(
            model="grok-beta",
            prompt=prompt,
            max_tokens_to_sample=250  # Correct parameter
        )
        return response.completion.strip()

    @staticmethod
    def process_movie(client, movie_title: str) -> dict:
        """
        Processes a single movie to extract the main actor and analyze sentiment.
        """
        actor_name = GrokClient.extract_main_actor(client, movie_title)
        sentiment = GrokClient.analyze_sentiment(client, movie_title, actor_name)
        return {
            'Movie Name': movie_title,
            'Main Actor': actor_name,
            'Sentiment Analysis': sentiment
        }

    @staticmethod
    def process_movies(client, movie_titles: list) -> pd.DataFrame:
        """
        Processes a list of movies and returns a DataFrame with sentiment analysis.
        """

        results = []
        for title in movie_titles:
            result = GrokClient.process_movie(client, title)
            results.append(result)
        return pd.DataFrame(results)

