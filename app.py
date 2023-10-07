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
DEFAULT_PATHS = {
    "missing_poster": "StreamLitGUI/DefaultData/missing_poster.jpg"
}

# Util Vars
CACHE = {}
DEFAULT_DATA = {
    "franchise": {

    },
    "movie": {
        "seen": False
    },
    "series": {
        "seasons": {
            "name": "Season 1",
            "seen": False
        }
    }
}

# Util Functions
def LoadCache():
    global CACHE
    CACHE = json.load(open(CACHE_PATH, "r"))

def SaveCache():
    global CACHE
    json.dump(CACHE, open(CACHE_PATH, "w"), indent=4)

@st.cache
def CACHEFUNC_GetMovieFromID(MOVIE_ID):
    MOVIE_IMDB = None
    try:
        MOVIE_IMDB = IMDB_GetMovieFromID(MOVIE_ID)
    except Exception as e:
        pass
    
    return MOVIE_IMDB

@st.cache
def CACHEFUNC_SearchMovie(name, n_results):
    SEARCH_RESULTS = []
    try:
        SEARCH_RESULTS = IMDB_SearchMovie(name, n_results=n_results)
    except Exception as e:
        SEARCH_RESULTS = None
    
    return SEARCH_RESULTS

@st.cache
def CACHEFUNC_ExtractLetterboxdList(url):
    MOVIES_DATA = []
    try:
        MOVIES_DATA = Letterboxd_ListURL_ExtractData(url)
    except Exception as e:
        MOVIES_DATA = None
    
    return MOVIES_DATA

# Main Functions
def Logs_Load():
    '''
    Logs - Load All Logs Data
    '''
    global DATA
    # Load
    for log_type in DATA["logs"].keys():
        DATA["logs"][log_type] = json.load(open(DATA_PATHS["logs"][log_type], "r"))

def Logs_Save():
    '''
    Logs - Save All Logs Data
    '''
    global DATA
    # Save
    for log_type in DATA["logs"].keys():
        json.dump(DATA["logs"][log_type], open(DATA_PATHS["logs"][log_type], "w"), indent=4)

# UI Functions
def UI_DisplayMovie(MOVIE):
    if MOVIE is None: return
    # Init
    MOVIE_DATA = MOVIE["data"]
    MOVIE_IMDB = MOVIE["imdb"]
    # Title and Poster
    st.markdown("### " + MOVIE_IMDB["title"])
    # Main Info
    INFO_Main = {
        "IMDB-ID": MOVIE_IMDB.movieID,
        "Release Year": MOVIE_IMDB["year"]
    }
    cols = st.columns(2)
    try: cols[0].image(MOVIE_IMDB["full-size cover url"])
    except Exception as e: cols[0].image(DEFAULT_PATHS["missing_poster"])
    cols[1].markdown("Watched: " + ("✅" if MOVIE_DATA["seen"] else "❌"))
    cols[1].write(INFO_Main)
    # Other Info
    OtherInfo = {
        **MOVIE_IMDB,
        **MOVIE_IMDB.__dict__,
    }
    st.json(OtherInfo, expanded=False)

def UI_DisplayMovies(MOVIES):
    for movie in MOVIES:
        UI_DisplayMovie(movie)
        st.markdown("<hr>", unsafe_allow_html=True)

def UI_LoadFranchise():
    # Init
    st.markdown("## Franchise")
    FRANCHISE_KEYS = list(DATA["logs"]["franchises"].keys())
    FRANCHISE_NAMES = [DATA["logs"]["franchises"][fk]["name"] for fk in FRANCHISE_KEYS]
    FRANCHISE_KEY = None
    # Franchise Operation
    USERINPUT_FranchiseOp = st.selectbox("Select Operation", ["View", "Add", "Remove", "Edit"])
    ## View
    if USERINPUT_FranchiseOp == "View":
        USERINPUT_FranchiseName = st.selectbox("Select Franchise", FRANCHISE_NAMES)
        FRANCHISE_KEY = FRANCHISE_KEYS[FRANCHISE_NAMES.index(USERINPUT_FranchiseName)]
    ## Add
    elif USERINPUT_FranchiseOp == "Add":
        USERINPUT_FranchiseName = st.text_input("Franchise Name")
        if st.button("Add") and not (USERINPUT_FranchiseName == ""):
                ADD_FRANCHISE_KEY = str(len(FRANCHISE_KEYS))
                ### Update Franchise Logs
                DATA["logs"]["franchises"][ADD_FRANCHISE_KEY] = {
                    "name": USERINPUT_FranchiseName,
                    **DEFAULT_DATA["franchise"]
                }
                ### Update Movie Logs
                DATA["logs"]["movies"][ADD_FRANCHISE_KEY] = {}
                ### Save Logs
                Logs_Save()
    ## Remove
    elif USERINPUT_FranchiseOp == "Remove":
        USERINPUT_FranchiseName = st.selectbox("Select Franchise", FRANCHISE_NAMES)
        USERINPUT_FranchiseIndex = FRANCHISE_NAMES.index(USERINPUT_FranchiseName)
        if st.button("Remove") and not (USERINPUT_FranchiseIndex == 0):
            REM_FRANCHISE_KEY = FRANCHISE_KEYS[USERINPUT_FranchiseIndex]
            ### Update Franchise Logs
            del DATA["logs"]["franchises"][REM_FRANCHISE_KEY]
            ### Update Movie Logs
            del DATA["logs"]["movies"][REM_FRANCHISE_KEY]
            ### Save Logs
            Logs_Save()
    ## Edit
    elif USERINPUT_FranchiseOp == "Edit":
        cols = st.columns(2)
        USERINPUT_FranchiseName = cols[0].selectbox("Select Franchise", FRANCHISE_NAMES)
        USERINPUT_NewName = cols[1].text_input("New Name", value=USERINPUT_FranchiseName)
        USERINPUT_FranchiseIndex = FRANCHISE_NAMES.index(USERINPUT_FranchiseName)
        if st.button("Edit") and not (USERINPUT_FranchiseIndex == 0) and not (USERINPUT_NewName == USERINPUT_FranchiseName):
            EDIT_FRANCHISE_KEY = FRANCHISE_KEYS[USERINPUT_FranchiseIndex]
            ### Update Franchise Logs
            DATA["logs"]["franchises"][EDIT_FRANCHISE_KEY]["name"] = USERINPUT_NewName
            ### Save Logs
            Logs_Save()

    return FRANCHISE_KEY

def UI_LoadMovie(FRANCHISE_KEY):
    # Init
    st.markdown("## Movie")
    MOVIE_KEYS = list(DATA["logs"]["movies"][FRANCHISE_KEY].keys())
    MOVIE_NAMES = [DATA["logs"]["movies"][FRANCHISE_KEY][mk]["name"] for mk in MOVIE_KEYS]
    MOVIE_KEY = None
    # Movie Operation
    USERINPUT_MovieOp = st.selectbox("Select Operation", ["View", "Add", "Remove"])
    ## View
    if USERINPUT_MovieOp == "View":
        USERINPUT_MovieName = st.selectbox("Select Movie", MOVIE_NAMES)
        MOVIE_KEY = MOVIE_KEYS[MOVIE_NAMES.index(USERINPUT_MovieName)]
    ## Add
    elif USERINPUT_MovieOp == "Add":
        USERINPUT_MovieAddType = st.selectbox("Select Movie Input Type", ["Name", "ID"])
        if USERINPUT_MovieAddType == "Name":
            USERINPUT_MovieName = st.text_input("Movie Name")
            MOVIE_IMDB = None if USERINPUT_MovieName == "" else CACHEFUNC_SearchMovie(USERINPUT_MovieName, n_results=1)
            if MOVIE_IMDB is None or len(MOVIE_IMDB) < 1:
                MOVIE_IMDB = None
                st.error("Invalid Movie Name")
            else:
                MOVIE_IMDB = MOVIE_IMDB[0]
        else:
            USERINPUT_MovieID = st.text_input("Movie ID")
            MOVIE_IMDB = None if USERINPUT_MovieID == "" else CACHEFUNC_GetMovieFromID(USERINPUT_MovieID)
            if MOVIE_IMDB is None: st.error("Invalid Movie ID")
        if MOVIE_IMDB is not None:
            ### Display Movie to be added
            UI_DisplayMovie({"imdb": MOVIE_IMDB, "data": {**DEFAULT_DATA["movie"]}})
            ### Add Movie to logs
            if st.button("Add"):
                ADD_MOVIE_KEY = str(len(MOVIE_KEYS))
                ### Update Movie Logs
                DATA["logs"]["movies"][FRANCHISE_KEY][ADD_MOVIE_KEY] = {
                    "name": MOVIE_IMDB["title"],
                    "id": MOVIE_IMDB.movieID,
                    **DEFAULT_DATA["movie"]
                }
                ### Save Logs
                Logs_Save()
    ## Remove
    elif USERINPUT_MovieOp == "Remove":
        USERINPUT_MovieName = st.selectbox("Select Movie", MOVIE_NAMES)
        USERINPUT_MovieIndex = MOVIE_NAMES.index(USERINPUT_MovieName)
        if st.button("Remove"):
            REM_MOVIE_KEY = MOVIE_KEYS[USERINPUT_MovieIndex]
            ### Update Movie Logs
            del DATA["logs"]["movies"][FRANCHISE_KEY][REM_MOVIE_KEY]
            ### Save Logs
            Logs_Save()

    return MOVIE_KEY

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
    # Process Check
    USERINPUT_Process = st.checkbox("Stream Process", value=False)
    if not USERINPUT_Process: USERINPUT_Process = st.button("Process")
    if not USERINPUT_Process: st.stop()
    # Process Inputs
    ## Search Movie
    SEARCH_RESULTS = CACHEFUNC_SearchMovie(USERINPUT_MovieName, USERINPUT_NResults)
    if SEARCH_RESULTS is None:
        st.error("Error in IMDB Module. Please try again later.")
        return
    # Display Results
    MOVIES = [{
        "imdb": movie,
        "data": {
            "seen": False
        }
    } for movie in SEARCH_RESULTS]
    UI_DisplayMovies(MOVIES)

def movie_logs():
    global DATA
    # Title
    st.header("Movie Logs")

    # Prereq Loaders
    Logs_Load()

    # Load Inputs
    # Franchise
    FRANCHISE_KEY = UI_LoadFranchise()
    if FRANCHISE_KEY is None:
        # st.experimental_rerun()
        return
    # Load Movie
    MOVIE_KEY = UI_LoadMovie(FRANCHISE_KEY)
    if MOVIE_KEY is None:
        # st.experimental_rerun()
        return
    MOVIE_DATA = DATA["logs"]["movies"][FRANCHISE_KEY][MOVIE_KEY]
    MOVIE_IMDB = CACHEFUNC_GetMovieFromID(MOVIE_DATA["id"])
    if MOVIE_IMDB is None:
        st.error("Error in IMDB Module. Please try again later.")
        return
    # Display Movie
    MOVIE = {
        "imdb": MOVIE_IMDB,
        "data": MOVIE_DATA
    }
    UI_DisplayMovie(MOVIE)
    # Operations
    cols = st.columns(2)
    LogsOperations = {
        "delete": cols[0].button("Delete"),
        "edit_seen": cols[1].button("Mark as Seen" if not MOVIE_DATA["seen"] else "Mark as Not Seen")
    }

    # Process Inputs
    if LogsOperations["delete"]:
        DATA["logs"]["movies"][FRANCHISE_KEY].pop(MOVIE_KEY)
        Logs_Save()
        st.success("Movie deleted from logs.")
        st.experimental_rerun()
    if LogsOperations["edit_seen"]:
        DATA["logs"]["movies"][FRANCHISE_KEY][MOVIE_KEY]["seen"] = not DATA["logs"]["movies"][FRANCHISE_KEY][MOVIE_KEY]["seen"]
        Logs_Save()
        st.success("Movie marked as " + ("seen" if DATA["logs"]["movies"][FRANCHISE_KEY][MOVIE_KEY]["seen"] else "not seen") + ".")
        st.experimental_rerun()

def letterboxd_list():
    # Title
    st.header("Letterboxd List")

    # Load Inputs
    USERINPUT_ListURL = st.text_input("List URL")

    # Process Check
    USERINPUT_Process = st.checkbox("Stream Process", value=False)
    if not USERINPUT_Process: USERINPUT_Process = st.button("Process")
    if not USERINPUT_Process: st.stop()
    # Process Inputs
    ## Extract Movies Data
    # MOVIES_DATA = CACHEFUNC_ExtractLetterboxdList(USERINPUT_ListURL)
    MOVIES_DATA = Letterboxd_ListURL_ExtractData(USERINPUT_ListURL)
    if MOVIES_DATA is None:
        st.error("Invalid URL.")
        return
    
    # Display Outputs
    st.write(MOVIES_DATA)

#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()