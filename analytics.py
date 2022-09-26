import sqlite3
import pandas as pd


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# VIEWS #########################################
with conn:       
    # TOP SONGS BY ARTIST IN TERMS OF DURATION_MS
    curs.execute("DROP VIEW IF EXISTS VW_artist_top_songs_by_duration;")
    curs.execute("""
        CREATE VIEW VW_artist_top_songs_by_duration
        AS
        SELECT * FROM (
            SELECT
                art.artist_name,
                art.followers,
                t.song_name,
                t.duration_ms,
                RANK() OVER(PARTITION BY art.artist_name ORDER BY t.duration_ms DESC) rnk 
            FROM artists art
            JOIN albums alb ON alb.artist_id = art.artist_id
            JOIN tracks t ON t.album_id = alb.album_id) subq
        WHERE rnk <= 3;
    """)
    
    # TOP ARTISTS BY NUMBER OF FOLLOWERS
    curs.execute("DROP VIEW IF EXISTS VW_top_artists_by_followers;")
    curs.execute("""
        CREATE VIEW VW_top_artists_by_followers
        AS
        SELECT artist_name, followers, popularity, genre
        FROM artists
        ORDER BY followers DESC;
    """)
    
    # TOP SONGS BY ARTIST IN TERMS OF TEMPO
    curs.execute("DROP VIEW IF EXISTS VW_artist_top_songs_by_tempo;")
    curs.execute("""
        CREATE VIEW VW_artist_top_songs_by_tempo
        AS
        SELECT * FROM (
            SELECT
                art.artist_name,
                art.followers,
                t.song_name,
                tf.tempo,
                RANK() OVER(PARTITION BY art.artist_name ORDER BY tf.tempo DESC) rnk 
            FROM artists art
            JOIN albums alb ON alb.artist_id = art.artist_id
            JOIN tracks t ON t.album_id = alb.album_id
            JOIN track_features tf ON tf.track_id = t.track_id) subq
        WHERE rnk <= 3;
    """)
    
    # ARTIST OVERVIEW
    curs.execute("DROP VIEW IF EXISTS VW_artist_overview;")
    curs.execute("""
        CREATE VIEW VW_artist_overview
        AS
        SELECT 
            art.artist_name,
            art.followers,
            art.genre,
            COUNT(*) total_albums,
            SUM(alb.total_tracks) total_tracks
        FROM artists art
        JOIN albums alb ON alb.artist_id = art.artist_id
        GROUP BY 1, 2, 3
        ORDER BY total_albums DESC, total_tracks DESC;
    """)
    
    # ARTIST STYLE OVERVIEW
    curs.execute("DROP VIEW IF EXISTS VW_artist_style_overview;")
    curs.execute("""
        CREATE VIEW VW_artist_style_overview
        AS
        SELECT 
            art.artist_name,
            art.popularity,
            art.genre,
            ROUND(AVG(tf.danceability), 4) avg_danceability,
            ROUND(AVG(tf.energy), 4) avg_energy,
            CAST(AVG(tf.tempo) AS INTEGER) avg_tempo,
            ROUND(AVG(tf.loudness), 2) avg_loudness
        FROM artists art
        JOIN albums alb ON alb.artist_id = art.artist_id
        JOIN tracks t ON t.album_id = alb.album_id
        JOIN track_features tf ON t.track_id = tf.track_id
        GROUP BY 1, 2, 3
        ORDER BY 1;
    """)
    
    curs.execute("SELECT * FROM VW_artist_style_overview;")
    t = pd.DataFrame(curs.fetchall())
    print(t.head(50))
    
    