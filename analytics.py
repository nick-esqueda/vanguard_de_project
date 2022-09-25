import sqlite3


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# TESTING #######################################
with conn:
    curs.execute("""
        SELECT 
            art.artist_name, art.followers, art.popularity,
            alb.album_id, alb.album_name, alb.release_date
        FROM artists art
        JOIN albums alb ON alb.artist_id = art.artist_id
        LIMIT 10;
    """)
    
    for r in curs.fetchall():
        print(r)