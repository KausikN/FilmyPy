"""
FilmyPy is a python visualiser for films, movies and other visual entertainment media
"""

# Imports
import requests
from imdb import Cinemagoer
from bs4 import BeautifulSoup

# Main Vars
# Instance of IMDB Class
IMDB = Cinemagoer()

# Main Functions
## IMDB
def IMDB_SearchMovie(name, n_results=2):
    '''
    IMDB - Search Movie by name
    '''
    return IMDB.search_movie(name, results=n_results)

def IMDB_GetMovieFromID(mov_id):
    '''
    IMDB - Get Movie Data by ID
    '''
    return IMDB.get_movie(mov_id)

## Letterboxd
def Letterboxd_ListURL_ExtractData(url):
    '''
    Letterboxd - List URL - Extract Movies Data
    '''
    # Read URL HTML
    DETAILED_URL = url if url.endswith("/detail/") else url + "/detail/"
    DATA_DETAILED = requests.get(DETAILED_URL)
    # Parse HTML
    HTML_TEXT_DETAILED = DATA_DETAILED.text
    SOUP_DETAILED = BeautifulSoup(HTML_TEXT_DETAILED, "html.parser")
    # Extract Movies Data
    ## Find all li elements with class as "film-detail"
    MOVIES_DETAILED = SOUP_DETAILED.find_all("li", class_="film-detail")
    MOVIES_DATA = []
    for movie_li in MOVIES_DETAILED:
        ### Movie Details Div
        movie_details_div = movie_li.find("div", class_="film-detail-content")
        ### Title
        movie_title_h2 = movie_details_div.find("h2", class_="headline-2 prettify")
        movie_title_a = movie_title_h2.find("a", recursive=False)
        title = movie_title_a.text
        ### Year
        movie_year_small = movie_title_h2.find("small", recursive=False)
        movie_year_a = movie_year_small.find("a", recursive=False)
        year = int(movie_year_a.text)
        ### Rating
        span_rating = movie_details_div.find("span", class_="rating")
        rating = None
        for rc in span_rating.__dict__["attrs"]["class"]:
            if rc.startswith("rated-"): rating = int(rc.split("-")[-1]) / 10
        ### Record
        MOVIES_DATA.append({
            "title": title,
            "year": year,
            "rating": rating
        })

    return MOVIES_DATA