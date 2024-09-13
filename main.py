from src.scraping.movie_deets import df
from src.scraping.titles import soup


def main():
    # Fetch trending movies from Rotten Tomatoes
    soup()

    print(df)


if __name__ == "__main__":
    main()
