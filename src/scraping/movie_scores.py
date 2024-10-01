from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd


class CriticAudienceScoreCollectorSelenium:
    def __init__(self):
        self.scores_data = []

    def get_scores_data(self, movies):
        """
        Accepts a list of dictionaries where each dictionary contains 'title' and 'url'.
        Scrapes the critic and audience scores from the movie URL's #critics-reviews section using Selenium.
        """
        # Path to your ChromeDriver executable
        service = Service('C:\Users\AnanyaShah\PycharmProjects\DirectTV_SEO_Automation\chromedriver_win32\chromedriver.exe')

        # Create a new instance of Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode to prevent a visible browser
        driver = webdriver.Chrome(service=service, options=options)

        for movie in movies:
            title = movie['title']
            url = movie['url'] + "#critics-reviews"  # Append the critics-reviews section

            # Open the page in the browser
            driver.get(url)

            # Allow the page to fully load
            time.sleep(3)

            # Get the shadow DOM root (You might have to tweak this based on the actual structure)
            shadow_host = driver.find_element(By.CSS_SELECTOR, 'media-scorecard-overlay')

            # Access shadow root (for accessing the shadow DOM)
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)

            scores_details = {
                "Movie Name": title.upper(),
                "Tomatometer Score": self.get_critic_score(shadow_root),
                "Audience Score": self.get_audience_score(shadow_root)
            }

            self.scores_data.append(scores_details)

        driver.quit()  # Close the browser

    def get_critic_score(self, shadow_root):
        """
        Extract the critic score from the shadow DOM.
        """
        try:
            critic_score = shadow_root.find_element(By.CSS_SELECTOR, 'rt-text[slot="criticsScore"]').text
            return critic_score
        except Exception as e:
            print(f"Error fetching critic score: {e}")
            return "N/A"

    def get_audience_score(self, shadow_root):
        """
        Extract the audience score from the shadow DOM.
        """
        try:
            audience_score = shadow_root.find_element(By.CSS_SELECTOR, 'rt-text[slot="audienceScore"]').text
            return audience_score
        except Exception as e:
            print(f"Error fetching audience score: {e}")
            return "N/A"

    def to_dataframe(self):
        """
        Converts the scores data to a DataFrame.
        """
        return pd.DataFrame(self.scores_data)


# Example usage:
if __name__ == "__main__":
    # Example list of movies with title and URL
    movies = [
        {"title": "Blink Twice", "url": "https://www.rottentomatoes.com/m/blink_twice"}
        # Add more movies as needed
    ]

    score_collector = CriticAudienceScoreCollectorSelenium()
    score_collector.get_scores_data(movies)
    scores_df = score_collector.to_dataframe()

    # Display or save the resulting scores DataFrame
    print(scores_df)
