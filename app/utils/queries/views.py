# this file is to store all view creation queries to keep code more concise.


V_ARTIST_TOP_SONGS_BY_DURATION = """
    CREATE VIEW V_artist_top_songs_by_duration
    AS
    WITH rankings AS (
        SELECT
            art.artist_name,
            art.followers,
            t.song_name,
            ROUND((CAST(t.duration_ms AS REAL) / 1000) / 60, 2)
                AS duration_mins,
            RANK() OVER(PARTITION BY art.artist_name ORDER BY t.duration_ms DESC) rnk 
        FROM artists art
        JOIN albums alb ON alb.artist_id = art.artist_id
        JOIN tracks t ON t.album_id = alb.album_id)
        
    SELECT artist_name, followers, song_name, duration_mins 
    FROM rankings
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
    WITH rankings AS (
        SELECT
            art.artist_name,
            art.followers,
            t.song_name,
            CAST(CAST(tf.tempo AS INTEGER) AS TEXT) || ' BPM' AS tempo,
            RANK() OVER(PARTITION BY art.artist_name ORDER BY tf.tempo DESC) rnk 
        FROM artists art
        JOIN albums alb ON alb.artist_id = art.artist_id
        JOIN tracks t ON t.album_id = alb.album_id
        JOIN track_features tf ON tf.track_id = t.track_id)
        
    SELECT artist_name, followers, song_name, tempo 
    FROM rankings
    WHERE rnk <= 10;
"""

V_ARTIST_OVERVIEW = """
    CREATE VIEW V_artist_overview
    AS
    SELECT 
        art.artist_name,
        art.followers,
        art.popularity,
        art.genre,
        COUNT(*) total_albums,
        SUM(alb.total_tracks) total_tracks
    FROM artists art
    JOIN albums alb ON alb.artist_id = art.artist_id
    GROUP BY 1, 2, 3
    ORDER BY genre, artist_name;
"""

V_POPULAR_ARTIST_FEATURES = """
    CREATE VIEW V_popular_artist_features
    AS
    SELECT 
        art.artist_name,
        art.popularity,
        art.genre,
        ROUND(AVG(tf.danceability), 4) avg_danceability,
        ROUND(AVG(tf.energy), 4) avg_energy,
        CAST(CAST(AVG(tf.tempo) AS INTEGER) AS TEXT) || ' BPM' AS avg_tempo,
        ROUND(AVG(tf.loudness), 2) avg_loudness
    FROM artists art
    JOIN albums alb ON alb.artist_id = art.artist_id
    JOIN tracks t ON t.album_id = alb.album_id
    JOIN track_features tf ON t.track_id = tf.track_id
    GROUP BY 1, 2, 3
    ORDER BY 2 DESC;
"""

V_GENRE_FEATURES = """
    CREATE VIEW V_genre_features
    AS
    SELECT
        art.genre,
        AVG(tf.danceability) danceability,
        AVG(tf.energy) energy,
        AVG(tf.instrumentalness) instrumentalness,
        AVG(tf.liveness) liveness,
        AVG(tf.loudness) loudness,
        AVG(tf.speechiness) speechiness,
        AVG(tf.tempo) tempo,
        AVG(tf.valence) valence
    FROM artists art
    JOIN albums alb ON alb.artist_id = art.artist_id
    JOIN tracks tr ON tr.album_id = alb.album_id
    JOIN track_features tf ON tf.track_id = tr.track_id
    GROUP BY 1
    ORDER BY 2 DESC, 3 DESC;
"""

V_GENRE_RELEASE_PATTERNS = """
    CREATE VIEW V_genre_release_patterns
    AS
    WITH genre_stats AS (
        SELECT 
            art.genre,
            CAST(AVG(art.popularity) AS INTEGER) avg_popularity,
            SUM(CASE WHEN alb.album_group = 'album' THEN 1 ELSE 0 END)
                AS total_albums,
            SUM(CASE WHEN alb.album_group = 'single' THEN 1 ELSE 0 END)
                AS total_singles,
            AVG(CASE WHEN alb.album_group = 'album' THEN tr.duration_ms ELSE NULL END) 
                AS avg_album_track_duration,
            AVG(CASE WHEN alb.album_group = 'single' THEN tr.duration_ms ELSE NULL END) 
                AS avg_single_track_duration
        FROM artists art
        JOIN albums alb ON alb.artist_id = art.artist_id
        JOIN tracks tr ON tr.album_id = alb.album_id
        GROUP BY 1)
    
    SELECT
        genre, 
        avg_popularity,
        ROUND((CAST(total_singles AS REAL) / (total_albums + total_singles)) * 100, 2)
            AS percentage_of_singles,
        ROUND((COALESCE(avg_album_track_duration, 0.0) / 1000) / 60, 2)
            AS avg_album_track_duration_mins,
        ROUND((COALESCE(avg_single_track_duration, 0.0) / 1000) / 60, 2)
            AS avg_single_track_duration_mins
    FROM genre_stats
    ORDER BY 3;
"""