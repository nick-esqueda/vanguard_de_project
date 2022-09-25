import sqlite3


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# CREATE TABLES #################################
with conn:
    # can you use the pandas index as the primary key?
    curs.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER NOT NULL PRIMARY KEY,
            artist_id TEXT NOT NULL UNIQUE,
            artist_name TEXT NOT NULL,
            external_url TEXT,
            genre TEXT,
            image_url TEXT,
            followers INTEGER,
            popularity INTEGER,
            type TEXT,
            artist_uri TEXT NOT NULL UNIQUE,
            PRIMARY KEY (id)
        );""")
        
    # albums are not unique, so you'll have multiple album_ids.
    # this means that album_id cannot be the primary key.
    # this also means that the tracks' foreign key can't connect to albums.
    # does having a composite primary key fix this?
    curs.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER NOT NULL PRIMARY KEY,
            album_id TEXT NOT NULL UNIQUE,
            album_name TEXT NOT NULL,
            external_url TEXT,
            image_url TEXT,
            release_date TEXT,
            total_tracks INTEGER NOT NULL,
            type TEXT,
            album_group TEXT (do you need this or album_type?),
            album_uri TEXT NOT NULL,
            artist_id TEXT,
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
        );""")
    
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
            FOREIGN KEY (album_id) REFERENCES albums(album_id) !!! DUPLICATES
        );""")
        
    curs.execute("""
        CREATE TABLE IF NOT EXISTS track_features (
            id INTEGER NOT NULL PRIMARY KEY,
            track_id TEXT NOT NULL
            danceability REAL
            energy REAL
            instrumentalness REAL
            liveness REAL
            loudness REAL
            speechiness REAL
            tempo REAL
            type TEXT
            valence REAL
            song_uri TEXT NOT NULL
            
        );""")
        
    