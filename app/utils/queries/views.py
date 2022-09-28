# this file is to store all view creation queries to keep code more concise.


V_ARTIST_TOP_SONGS_BY_DURATION = """
    CREATE VIEW V_artist_top_songs_by_duration
    AS
    SELECT artist_name, followers, song_name, duration_mins 
    FROM (SELECT
              art.artist_name,
              art.followers,
              t.song_name,
              ROUND((CAST(t.duration_ms AS REAL) / 1000) / 60, 2)
                  AS duration_mins,
              RANK() OVER(PARTITION BY art.artist_name ORDER BY t.duration_ms DESC) rnk 
          FROM artists art
          JOIN albums alb ON alb.artist_id = art.artist_id
          JOIN tracks t ON t.album_id = alb.album_id) subq
    WHERE rnk <= 10;
"""

V_TOP_ARTISTS_BY_FOLLOWERS = """
    CREATE VIEW V_top_artists_by_followers
    AS
    SELECT artist_name, followers, popularity, genre
    FROM artists
    ORDER BY followers DESC;
"""

V_ARTIST_TOP_SONGS_BY_TEMPO = """
    CREATE VIEW V_artist_top_songs_by_tempo
    AS
    SELECT artist_name, followers, song_name, tempo 
    FROM (SELECT
              art.artist_name,
              art.followers,
              t.song_name,
              CAST(CAST(tf.tempo AS INTEGER) AS TEXT) || ' BPM' AS tempo,
              RANK() OVER(PARTITION BY art.artist_name ORDER BY tf.tempo DESC) rnk 
          FROM artists art
          JOIN albums alb ON alb.artist_id = art.artist_id
          JOIN tracks t ON t.album_id = alb.album_id
          JOIN track_features tf ON tf.track_id = t.track_id) subq
    WHERE rnk <= 10;
"""

V_ARTIST_OVERVIEW = """
    CREATE VIEW V_artist_overview
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
"""

V_ARTIST_STYLE_OVERVIEW = """
    CREATE VIEW V_artist_style_overview
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
"""