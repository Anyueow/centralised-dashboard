import wikipedia

class WikipediaClient:
    def __init__(self, language='en'):
        wikipedia.set_lang(language)

    def get_page(self, title):
        try:
            # Attempt to fetch the page directly
            return wikipedia.page(title)
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation by prioritizing titles containing "(film)" or "movie"
            for option in e.options:
                if "(film)" in option.lower() or "movie" in option.lower():
                    try:
                        return wikipedia.page(option)
                    except wikipedia.exceptions.DisambiguationError:
                        continue
            # If no suitable option is found, print a message
            print(f"Disambiguation error: Multiple options found for '{title}', and none contain '(film)' or 'movie'.")
            return None
        except wikipedia.exceptions.PageError:
            # Handle cases where the page doesn't exist
            print(f"Page '{title}' does not exist.")
            return None
