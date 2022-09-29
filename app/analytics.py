import pandas as pd
from .utils import DB
from .utils import V_ARTIST_TOP_SONGS_BY_DURATION, V_TOP_ARTISTS_BY_FOLLOWERS
from .utils import V_ARTIST_TOP_SONGS_BY_TEMPO, V_ARTIST_OVERVIEW
from .utils import V_POPULAR_ARTIST_FEATURES, V_GENRE_FEATURES, V_GENRE_RELEASE_PATTERNS


# VIEWS #########################################
def create_views(db: DB) -> None:
    # drop the views if they had already been created. (this is to "start fresh" every time.)
    db.execute("DROP VIEW IF EXISTS V_artist_top_songs_by_duration;")
    db.execute("DROP VIEW IF EXISTS V_top_artists_by_followers;")
    db.execute("DROP VIEW IF EXISTS V_artist_top_songs_by_tempo;")
    db.execute("DROP VIEW IF EXISTS V_artist_overview;")
    db.execute("DROP VIEW IF EXISTS V_popular_artist_features;")
    db.execute("DROP VIEW IF EXISTS V_genre_features;")
    db.execute("DROP VIEW IF EXISTS V_genre_release_patterns;")
    # (re)create the views in the database.
    db.execute(V_ARTIST_TOP_SONGS_BY_DURATION)
    db.execute(V_TOP_ARTISTS_BY_FOLLOWERS)
    db.execute(V_ARTIST_TOP_SONGS_BY_TEMPO)
    db.execute(V_ARTIST_OVERVIEW)
    db.execute(V_POPULAR_ARTIST_FEATURES)
    db.execute(V_GENRE_FEATURES)
    db.execute(V_GENRE_RELEASE_PATTERNS)
    
def test_view(db: DB, view_name: str) -> None:
    db.execute(view_name)
    t = pd.DataFrame(db.result())
    print(t.head(50))
