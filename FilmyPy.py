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
    return list(sorted(movieData.keys()))

def GetMovieSubDataFields(mov_id='0133093', sub_key='directors'):
    movieData = imdb.get_movie(mov_id)
    return list(sorted(movieData[sub_key].keys()))

def GetMovieData(mov_id):
    return imdb.get_movie(mov_id)

def GetNames(movieData):
    if 'akas' in movieData.keys():
        return movieData['akas']
    elif 'original title' in movieData.keys():
        return movieData['original title']

def GetDirectors(mov_id='0133093'):
    movieData = imdb.get_movie(mov_id) # '0133093'
    directorNames = []
    for director in movieData['directors']:
        directorNames.append(director['name'])
    return directorNames

# Driver Code
# Params
movie_id = '1112093'
subField = 'directors'
# Params

# RunCode
# print(GetMovieInfosets())
# print(GetMovieDataFields(movie_id))
# print(GetMovieSubDataFields(movie_id, subField))
# print(GetDirectors(movie_id))

movieData = GetMovieData(movie_id)
print(list(movieData.keys()))
print(GetNames(movieData))
print(movieData['directors'])