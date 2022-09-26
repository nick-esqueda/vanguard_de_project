import sqlite3
import pandas as pd


conn = sqlite3.connect("spotify.db")
curs = conn.cursor()

# TESTING #######################################
with conn:
    # get the top 3 longest songs for every artist
    # turn ms to seconds
    # rank by seconds ms
    curs.execute("""
        WITH t1 AS (
            SELECT
                art.artist_name,
                art.artist_id,
                art.followers,
                art.popularity,
                t.song_name,
                t.duration_ms,
                RANK() OVER(PARTITION BY art.artist_name ORDER BY t.duration_ms DESC) rnk 
            FROM artists art
            JOIN albums alb ON alb.artist_id = art.artist_id
            JOIN tracks t ON t.album_id = alb.album_id)
            
        SELECT * FROM t1
        WHERE rnk <= 3;
    """)
    
    # for r in curs.fetchall():
    #     print(r)
    
    t = pd.DataFrame(curs.fetchall())
    print(t)
        
        
    # curs.execute("""
    #     DROP VIEW IF EXISTS VW_artist_top_songs_by_duration;
    #     CREATE VIEW VW_artist_top_songs_by_duration AS
        
        
    #     ;
    # """)