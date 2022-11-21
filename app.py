"""
Stream lit GUI for hosting FilmyPy
"""

# Imports
import os
import json
import streamlit as st

from FilmyPy import *

# Main Vars
config = json.load(open("./StreamLitGUI/UIConfig.json", "r"))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose one of the following",
        tuple(
            [config["PROJECT_NAME"]] + 
            config["PROJECT_MODES"]
        )
    )
    
    if selected_box == config["PROJECT_NAME"]:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(" ", "_").lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config["PROJECT_NAME"])
    st.markdown("Github Repo: " + "[" + config["PROJECT_LINK"] + "](" + config["PROJECT_LINK"] + ")")
    st.markdown(config["PROJECT_DESC"])

    # st.write(open(config["PROJECT_README"], "r").read())

#############################################################################################################################
# Repo Based Vars
CACHE_PATH = "StreamLitGUI/CacheData/Cache.json"
DATA_PATHS = {
    "logs": {
        "franchises": "Data/Logs_Franchises.json",
        "movies": "Data/Logs_Movies.json",
        "series": "Data/Logs_Series.json"
    }
}
DATA = {
    "logs": {
        "franchises": {},
        "movies": {},
        "series": {}
    }
}

# Util Vars
CACHE = {}

# Util Functions
def LoadCache():
    global CACHE
    CACHE = json.load(open(CACHE_PATH, "r"))

def SaveCache():
    global CACHE
    json.dump(CACHE, open(CACHE_PATH, "w"), indent=4)

# Main Functions
def Logs_Load():
    '''
    Logs - Load All Logs Data
    '''
    global DATA

    for logType in DATA["logs"].keys():
        DATA["logs"][logType] = json.load(open(DATA_PATHS["logs"][logType], "r"))

# UI Functions
def UI_DisplayMovie(MOVIE):
    # Title and Poster
    st.markdown("### " + MOVIE["title"])
    # Main Info
    INFO_Main = {
        "IMDB-ID": MOVIE.movieID,
        "Year": MOVIE["year"]
    }
    cols = st.columns(2)
    cols[0].image(MOVIE["full-size cover url"])
    cols[1].write(INFO_Main)
    # Other Info
    OtherInfo = {
        
    }
    st.write(OtherInfo)

def UI_DisplayMovies(MOVIES):
    for movie in MOVIES:
        UI_DisplayMovie(movie)
        st.markdown("<hr>", unsafe_allow_html=True)

# Repo Based Functions
def movie_search():
    # Title
    st.header("Search Movie")

    # Prereq Loaders
    Logs_Load()

    # Load Inputs
    # Init
    USERINPUT_MovieName = st.text_input("Movie Name", value="Avengers")
    USERINPUT_NResults = st.number_input("Number of Results", value=2, min_value=1, max_value=10)

    # Process Inputs
    SEARCH_RESULTS = []
    try:
        SEARCH_RESULTS = IMDB_SearchMovie(USERINPUT_MovieName, n_results=USERINPUT_NResults)
    except Exception as e:
        st.error("Error in IMDB Module. Please try again later.")

    # Display Outputs
    UI_DisplayMovies(SEARCH_RESULTS)

def movie_logs():
    global DATA
    # Title
    st.header("Movie Logs")

    # Prereq Loaders
    Logs_Load()

    # Load Inputs
    # Load Franchise
    FRANCHISE_IDS = list(DATA["logs"]["franchises"].keys())
    FRANCHISE_NAMES = [DATA["logs"]["franchises"][franchise_id]["name"] for franchise_id in FRANCHISE_IDS]
    USERINPUT_FranchiseName = st.selectbox("Select Franchise", FRANCHISE_NAMES)
    FRANCHISE_ID = FRANCHISE_IDS[FRANCHISE_NAMES.index(USERINPUT_FranchiseName)]
    # Load Movie
    MOVIE_IDS = list(DATA["logs"]["movies"][FRANCHISE_ID].keys())
    MOVIE_NAMES = [DATA["logs"]["movies"][FRANCHISE_ID][movie_id]["name"] for movie_id in MOVIE_IDS]
    USERINPUT_MovieName = st.selectbox("Select Movie", MOVIE_NAMES)
    MOVIE_ID = MOVIE_IDS[MOVIE_NAMES.index(USERINPUT_MovieName)]
    MOVIE = DATA["logs"]["movies"][FRANCHISE_ID][MOVIE_ID]

    # Process Inputs
    MOVIE = IMDB_GetMovieFromID(MOVIE["id"])

    # Display Outputs
    UI_DisplayMovie(MOVIE)

    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()