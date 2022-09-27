import pandas as pd
from etl.utils.db import DB


# VIEWS #########################################
def create_views(db: DB) -> None:
    # TOP SONGS BY ARTIST IN TERMS OF DURATION_MS
    db.execute("DROP VIEW IF EXISTS VW_artist_top_songs_by_duration;")
    db.execute("""
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
    db.execute("DROP VIEW IF EXISTS VW_top_artists_by_followers;")
    db.execute("""
        CREATE VIEW VW_top_artists_by_followers
        AS
        SELECT artist_name, followers, popularity, genre
        FROM artists
        ORDER BY followers DESC;
    """)
    
    # TOP SONGS BY ARTIST IN TERMS OF TEMPO
    db.execute("DROP VIEW IF EXISTS VW_artist_top_songs_by_tempo;")
    db.execute("""
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
    db.execute("DROP VIEW IF EXISTS VW_artist_overview;")
    db.execute("""
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
    db.execute("DROP VIEW IF EXISTS VW_artist_style_overview;")
    db.execute("""
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
    
def test_prompt_views(db: DB) -> None:
    db.execute("SELECT * FROM VW_artist_top_songs_by_duration;")
    t = pd.DataFrame(db.result())
    print(t.head(10))
    
    db.execute("SELECT * FROM VW_top_artists_by_followers;")
    t = pd.DataFrame(db.result())
    print(t.head(10))
    
    db.execute("SELECT * FROM VW_artist_top_songs_by_tempo;")
    t = pd.DataFrame(db.result())
    print(t.head(10))
    
def test_custom_views(db: DB) -> None:
    db.execute("SELECT * FROM VW_artist_overview;")
    t = pd.DataFrame(db.result())
    print(t.head(10))
    
    db.execute("SELECT * FROM VW_artist_style_overview;")
    t = pd.DataFrame(db.result())
    print(t.head(10))
    
    
# MAIN ###################################################################
##########################################################################
def main():
    db = DB()
    create_views(db)
    
    test_prompt_views(db)


if __name__ == "__main__":
    main()