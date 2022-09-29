# this file is to store all table creation queries to keep code more concise.


CREATE_ARTISTS = """
    CREATE TABLE artists (
        artist_id TEXT NOT NULL PRIMARY KEY,
        artist_name TEXT NOT NULL,
        external_url TEXT,
        genre TEXT,
        image_url TEXT,
        followers INTEGER,
        popularity INTEGER,
        type TEXT,
        artist_uri TEXT NOT NULL UNIQUE
    );
"""

CREATE_ALBUMS = """
    CREATE TABLE albums (
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
    );
"""

CREATE_TRACKS = """
    CREATE TABLE tracks (
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
    );
"""

CREATE_TRACK_FEATURES = """
    CREATE TABLE track_features (
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
    );
"""