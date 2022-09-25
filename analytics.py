import sqlite3


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# TESTING #######################################
with conn:
    curs.execute("""
        SELECT 
            art.artist_name, alb.album_name,
            t.song_name, t.duration_ms,
            tf.danceability, tf.energy, tf.loudness
        FROM artists art
        JOIN albums alb ON art.artist_id = alb.artist_id
        JOIN tracks t ON t.album_id = alb.album_id
        JOIN track_features tf ON tf.track_id = t.track_id
        WHERE tf.loudness > -3
        LIMIT 20;
    """)
    
    for r in curs.fetchall():
        print(r)