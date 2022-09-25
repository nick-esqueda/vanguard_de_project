import sqlite3


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# CREATE TABLES #################################
with conn:
    # ARTISTS
    curs.execute("""
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
    curs.execute("""
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
    curs.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER NOT NULL PRIMARY KEY,
            track_id TEXT NOT NULL,
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
    curs.execute("""
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
        
    
conn.close()