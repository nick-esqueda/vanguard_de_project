import pandas as pd
import transform
from utils.db import DB
from utils.queries import *


# CREATE TABLES #################################
def create_tables(db: DB) -> None:
    print("Creating tables: artists, albums, tracks, and track_features...")
    
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
    print(f"Finished loading data into {tablename}")

def test(db: DB) -> None:
    db.execute("SELECT * FROM artists LIMIT 5")
    print(db.result())
    
    db.execute("SELECT * FROM albums LIMIT 5")
    print(db.result())
    
    db.execute("SELECT * FROM tracks LIMIT 5")
    print(db.result())
    
    db.execute("SELECT * FROM track_features LIMIT 5")
    print(db.result())


# MAIN ###################################################################
##########################################################################
def main():
    artists, albums, tracks, track_features = transform.main()
    
    db = DB()
    create_tables(db)
    load_data(artists, "artists", db)
    load_data(albums, "albums", db)
    load_data(tracks, "tracks", db)
    load_data(track_features, "track_features", db)
    
    # test(db)
    
    db.close()


if __name__ == "__main__":
    main()