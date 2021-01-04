'''
FilmyPy is a python visualiser for films, movies and other visual entertainment media
'''

# Imports
from imdb import IMDb

# Main Vars
# Instance of IMDB Class
imdb = IMDb()

# Main Functions
def GetMovieInfosets():
    return imdb.get_movie_infoset()

def GetMovieDataFields(mov_id='0133093'):
    movieData = imdb.get_movie(mov_id)
    return list(movieData.keys())

def GetMovieSubDataFields(mov_id='0133093', sub_key='directors'):
    movieData = imdb.get_movie(mov_id)
    return list(movieData[sub_key].keys())

def GetDirectors(mov_id='0133093'):
    movieData = imdb.get_movie(mov_id) # '0133093'
    directorNames = []
    for director in movieData['directors']:
        directorNames.append(director['name'])
    return directorNames

# Driver Code
# Params
movie_id = '0133093'
subField = 'directors'
# Params

# RunCode
# print(GetMovieInfosets())
print(GetMovieDataFields(movie_id))
# print(GetMovieSubDataFields(movie_id, subField))
# print(GetDirectors(movie_id))