import pandas as pd
from .utils import DB
from .utils import CREATE_ARTISTS, CREATE_ALBUMS, CREATE_TRACKS, CREATE_TRACK_FEATURES


# CREATE TABLES #################################
def create_tables(db: DB) -> None:
    # drop the tables if they had already been created. (this is to "start fresh" every time.)
    db.execute("DROP TABLE IF EXISTS artists")
    db.execute("DROP TABLE IF EXISTS albums")
    db.execute("DROP TABLE IF EXISTS tracks")
    db.execute("DROP TABLE IF EXISTS track_features")
    # (re)create the tables in the database.
    db.execute(CREATE_ARTISTS)
    db.execute(CREATE_ALBUMS)
    db.execute(CREATE_TRACKS)
    db.execute(CREATE_TRACK_FEATURES)
        
# INSERTING DATA ################################
def load_data(data: pd.DataFrame, tablename: str, db: DB) -> None:
    data.to_sql(tablename, db.conn, if_exists="replace", index=False)
    print(f"Finished loading data into table: {tablename}")

def test_table_creation(db: DB, query: str) -> None:
    db.execute(query)
    print(db.result())
    