"""
FilmyPy is a python visualiser for films, movies and other visual entertainment media
"""

# Imports
from imdb import IMDb

# Main Vars
# Instance of IMDB Class
IMDB = IMDb(accessSystem="http")

# Main Functions
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