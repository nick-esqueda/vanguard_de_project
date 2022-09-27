import pandas as pd
import transform
from utils.db import DB


# CREATE TABLES #################################
def create_tables(db: DB) -> None:
    print("Creating tables: artists, albums, tracks, and track_features...")
    # ARTISTS
    db.execute("DROP TABLE IF EXISTS artists")
    db.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            artist_id TEXT NOT NULL PRIMARY KEY,
            artist_name TEXT NOT NULL,
            external_url TEXT,
            genre TEXT,
            image_url TEXT,
            followers INTEGER,
            popularity INTEGER,
            type TEXT,
            artist_uri TEXT NOT NULL UNIQUE
        );""")
        
    # ALBUMS
    db.execute("DROP TABLE IF EXISTS albums")
    db.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            album_id TEXT NOT NULL PRIMARY KEY,
            album_name TEXT NOT NULL,
            external_url TEXT,
            image_url TEXT,
            release_date TEXT,
            total_tracks INTEGER NOT NULL,
            type TEXT,
            album_group TEXT,
            album_uri TEXT NOT NULL,
            artist_id TEXT,
            FOREIGN KEY (album_id) REFERENCES artists(artist_id)
        );""")
    
    # TRACKS
    db.execute("DROP TABLE IF EXISTS tracks")
    db.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT NOT NULL PRIMARY KEY,
            song_name TEXT NOT NULL,
            external_url TEXT,
            duration_ms INTEGER NOT NULL,
            explicit INTEGER,
            disc_number INTEGER,
            type TEXT,
            song_uri TEXT NOT NULL,
            album_id TEXT NOT NULL,
            FOREIGN KEY (album_id) REFERENCES albums(album_id)
        );""")
        
    # TRACK FEATURES
    db.execute("DROP TABLE IF EXISTS track_features")
    db.execute("""
        CREATE TABLE IF NOT EXISTS track_features (
            track_id TEXT NOT NULL PRIMARY KEY,
            danceability REAL,
            energy REAL,
            instrumentalness REAL,
            liveness REAL,
            loudness REAL,
            speechiness REAL,
            tempo REAL,
            type TEXT,
            valence REAL,
            song_uri TEXT NOT NULL,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id)
        );""")
        
        
# INSERTING DATA ################################
def load_data(data: pd.DataFrame, tablename: str, db: DB) -> None:
    data.to_sql(tablename, db.conn, if_exists="replace", index=False)
    print(f"Finished loading data into {tablename}")

def test(db):
    db.execute("SELECT * FROM artists LIMIT 5")
    print(db.result())
    
    db.execute("SELECT * FROM albums LIMIT 5")
    print(db.result())
    
    db.execute("SELECT * FROM tracks LIMIT 5")
    print(db.result())
    
    db.execute("SELECT * FROM track_features LIMIT 5")
    print(db.result())


# MAIN ###################################################################
##########################################################################
def main():
    artists, albums, tracks, track_features = transform.main()
    
    db = DB()
    create_tables(db)
    load_data(artists, "artists", db)
    load_data(albums, "albums", db)
    load_data(tracks, "tracks", db)
    load_data(track_features, "track_features", db)
    
    # test(db)
    
    db.close()


if __name__ == "__main__":
    main()