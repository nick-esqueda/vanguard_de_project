import pandas as pd
from utils.db import DB
from utils.queries import *


# VIEWS #########################################
def create_views(db: DB) -> None:
    # drop the views if they had already been created. (this is to "start fresh" every time.)
    db.execute("DROP VIEW IF EXISTS VW_artist_top_songs_by_duration;")
    db.execute("DROP VIEW IF EXISTS VW_top_artists_by_followers;")
    db.execute("DROP VIEW IF EXISTS VW_artist_top_songs_by_tempo;")
    db.execute("DROP VIEW IF EXISTS VW_artist_overview;")
    db.execute("DROP VIEW IF EXISTS VW_artist_style_overview;")
    # (re)create the views in the database.
    db.execute(V_ARTIST_TOP_SONGS_BY_DURATION)
    db.execute(V_TOP_ARTISTS_BY_FOLLOWERS)
    db.execute(V_ARTIST_TOP_SONGS_BY_TEMPO)
    db.execute(V_ARTIST_OVERVIEW)
    db.execute(V_ARTIST_STYLE_OVERVIEW)
    
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
    test_custom_views(db)


if __name__ == "__main__":
    main()