"""
this module is solely to define the functions that will be called from
__main__.py upon running the whole program. each function here describes the
different stages of the ETL process.
"""

from app.extract import extract_artists, extract_artists_albums
from app.extract import extract_albums_tracks, extract_track_features
from app.transform import clean_artists, clean_albums, clean_tracks, clean_track_features
from app.load import create_tables, load_data, create_views
from app.visualizations import energy_vs_loudness_tempo, loudness_vs_danceability
from app.visualizations import genre_style_comparison, subgenre_style_comparison
from app.utils import ARTIST_URLS, write_to_csv


def extract_and_transform_all(write_csv=False):
    """
    this is a top level function that will run all functions necessary
    to extract and load the data from the Spotify API.
    all data is cleaned/transformed immediately after extraction from the API.
    messages will be printed to the terminal to indicate progress.
    """
    # ARTISTS #################################
    print("Extracting artists...")
    artists = extract_artists(ARTIST_URLS)
    artists = clean_artists(artists)
    print("\tartist data has been extracted and transformed!")
    
    # ALBUMS ##################################
    print("Extracting albums...")
    albums = extract_artists_albums(ARTIST_URLS)
    albums = clean_albums(albums)
    print("\talbum data has been extracted and transformed!")
    
    # TRACKS ##################################
    print("Extracting tracks...\n\t(this might take a minute... 😳)")
    tracks = extract_albums_tracks(albums["album_id"])
    tracks = clean_tracks(tracks, albums, artists)
    print("\ttrack data has been extracted and transformed!")
    
    # TRACK FEATURES ##########################
    print("Extracting track features...")
    track_features = extract_track_features(tracks["track_id"])
    track_features = clean_track_features(track_features, tracks)
    print("\ttrack feature data has been extracted and transformed!")
    
    # CSV #####################################
    if write_csv is True:
        write_to_csv(artists, filepath="app/data/artists.csv")
        write_to_csv(albums, filepath="app/data/albums.csv")
        write_to_csv(tracks, filepath="app/data/tracks.csv")
        write_to_csv(track_features, filepath="app/data/track_features.csv")
        
    return artists, albums, tracks, track_features
    
def load_all(db, artists, albums, tracks, track_features):
    """
    this is a top level function that will run the necessary functions to
    load all data into the SQLite database.
    messages will be printed to the terminal to indicate progress.
    """
    print("Creating tables: artists, albums, tracks, and track_features...")
    create_tables(db)
    load_data(artists, "artists", db)
    load_data(albums, "albums", db)
    load_data(tracks, "tracks", db)
    load_data(track_features, "track_features", db)
    
def run_analytics(db):
    """
    this is a top level function that will run the necessary functions to
    create the predefined database views, as well as create the visualizations
    that will reside in the app/images/ directory.
    messages will be printed to the terminal to indicate progress.
    """
    create_views(db)
    print("Database views have been successfully created!")
    
    print("Creating visualization images...")
    energy_vs_loudness_tempo(db)
    loudness_vs_danceability(db)
    genre_style_comparison(db)
    subgenre_style_comparison(db)
    print("\tYour visualizations are ready!\nPlease look in the app/images directory to find your images.")
