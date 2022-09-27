import sqlite3
import transform


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# CREATE TABLES #################################
def create_tables():
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
        
        
# INSERTING DATA ################################
def load_data(data):
    data.to_sql("artists", conn, if_exists="replace", index=False)

def test():
    with conn:
        curs.execute("SELECT * FROM artists LIMIT 5")
        test = curs.fetchall()
        print(test)
        
        curs.execute("SELECT * FROM albums LIMIT 5")
        test = curs.fetchall()
        print(test)
        
        curs.execute("SELECT * FROM tracks LIMIT 5")
        test = curs.fetchall()
        print(test)
        
        curs.execute("SELECT * FROM track_features LIMIT 5")
        test = curs.fetchall()
        print(test)




#################################################
def main():
    create_tables()
    
    artists, albums, tracks, track_features = transform.main()
    load_data(artists)
    load_data(albums)
    load_data(tracks)
    load_data(track_features)
    
    test()
    
    conn.close()


if __name__ == "__main__":
    main()
    
    
conn.close()