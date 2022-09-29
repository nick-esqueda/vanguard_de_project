from app.extract import *
from app.transform import *
from app.load import *
from app.analytics import create_views
from app.visualizations import *
from app.utils import DB, ARTIST_URLS, write_to_csv


def extract_and_transform_all(write_csv=False):
    artists = extract_artists(ARTIST_URLS)
    artists = clean_artists(artists)
    albums = extract_artists_albums(ARTIST_URLS)
    albums = clean_albums(albums)
    tracks = extract_albums_tracks(albums["album_id"])
    tracks = clean_tracks(tracks, albums, artists)
    track_features = extract_track_features(tracks["track_id"])
    track_features = clean_track_features(track_features, tracks)
    
    if write_csv is True:
        write_to_csv(artists, "data/artists.csv")
        write_to_csv(albums, "data/albums.csv")
        write_to_csv(tracks, "data/tracks.csv")
        write_to_csv(track_features, "data/track_features.csv")
        
    return artists, albums, tracks, track_features
    
def load_all(db, artists, albums, tracks, track_features):
    create_tables(db)
    load_data(artists, "artists", db)
    load_data(albums, "albums", db)
    load_data(tracks, "tracks", db)
    load_data(track_features, "track_features", db)
    
def create_visualizations(db):
    plt.style.use("dark_background") # put this at the top of visualizations.py?
    energy_vs_loudness_tempo(db)
    loudness_vs_danceability(db)
    genre_style_comparison(db)
    subgenre_style_comparison(db)


# RUN PROGRAM ############################################################
##########################################################################
def run():
    # NOTE: add condition to allow user to read from csv's instead of extracting again.
    data = extract_and_transform_all()
    db = DB()
    load_all(db, *data) 
    create_views(db)
    db.close()

run()