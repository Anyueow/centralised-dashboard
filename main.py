from src.scraping.titles import soup
from src.scraping.movie_deets import df
from src.scraping.rottentomatoes_atrr import test



def main():
    # Fetch trending movies from Rotten Tomatoes
    soup()

    print(df)
if __name__ == "__main__":
    main()
