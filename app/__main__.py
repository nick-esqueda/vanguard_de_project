from app.extract import extract_artists, extract_artists_albums
from app.extract import extract_albums_tracks, extract_track_features
from app.transform import clean_artists, clean_albums, clean_tracks, clean_track_features
from app.load import create_tables, load_data
from app.analytics import create_views
from app.visualizations import energy_vs_loudness_tempo, loudness_vs_danceability
from app.visualizations import genre_style_comparison, subgenre_style_comparison
from app.utils import DB, ARTIST_URLS, write_to_csv, read_all_from_csv


def extract_and_transform_all(write_csv=False):
    print("Extracting artists...")
    artists = extract_artists(ARTIST_URLS)
    artists = clean_artists(artists)
    print("\tartist data has been extracted and transformed!")
    
    print("Extracting albums...")
    albums = extract_artists_albums(ARTIST_URLS)
    albums = clean_albums(albums)
    print("\talbum data has been extracted and transformed!")
    
    print("Extracting tracks...\n\t(this might take a minute... 😳)")
    tracks = extract_albums_tracks(albums["album_id"])
    tracks = clean_tracks(tracks, albums, artists)
    print("\ttrack data has been extracted and transformed!")
    
    print("Extracting track features...")
    track_features = extract_track_features(tracks["track_id"])
    track_features = clean_track_features(track_features, tracks)
    print("\ttrack feature data has been extracted and transformed!")
    
    if write_csv is True:
        write_to_csv(artists, "data/artists.csv")
        write_to_csv(albums, "data/albums.csv")
        write_to_csv(tracks, "data/tracks.csv")
        write_to_csv(track_features, "data/track_features.csv")
        
    return artists, albums, tracks, track_features
    
def load_all(db, artists, albums, tracks, track_features):
    print("Creating tables: artists, albums, tracks, and track_features...")
    create_tables(db)
    load_data(artists, "artists", db)
    load_data(albums, "albums", db)
    load_data(tracks, "tracks", db)
    load_data(track_features, "track_features", db)
    
def run_analytics(db):
    create_views(db)
    print("Database views have been successfully created!")
    
    print("Creating visualization images...")
    energy_vs_loudness_tempo(db)
    loudness_vs_danceability(db)
    genre_style_comparison(db)
    subgenre_style_comparison(db)
    print("\tYour visualizations are ready!\nPlease look in the app/images directory to find your images.")


# RUN PROGRAM ############################################################
##########################################################################
def run():
    # NOTE: add condition to allow user to read from csv's instead of extracting again.
    print("\n******************* EXTRACT AND TRANSFORM *******************")
    data = extract_and_transform_all()
    # data = read_all_from_csv()
    
    print("\n******************* LOAD INTO DATABASE **********************")
    db = DB()
    load_all(db, *data) 
    
    print("\n******************* CREATE ANALYTICS ************************")
    run_analytics(db)
    db.close()
    
    print("\nDONE: exiting successfully.")

run()