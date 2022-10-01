import pandas as pd
from .utils import DB, db_table_names, db_table_queries


# CREATE TABLES #################################
def create_tables(db: DB) -> None:
    """
    this function will create all of the pre-determined set of DB tables, using the
    SQL queries provided by db_tables.py.
    
    NOTE: all tables are dropped before executing the "CREATE TABLE" queries again.
    this is to pick up on any future changes to the tables.
    """
    for t_name in db_table_names:
        db.execute(f"DROP TABLE IF EXISTS {t_name}")
    
    for t_query in db_table_queries:
        db.execute(t_query)
        
# INSERTING DATA ################################
def load_data(data: pd.DataFrame, tablename: str, db: DB) -> None:
    """
    this function inserts the given data into the specified table using the
    DB connection object, and prints a confirmation message to the terminal
    after insertion.
    """
    data.to_sql(tablename, db.conn, if_exists="replace", index=False)
    print(f"Finished loading data into table: {tablename}")

def test_table_creation(db: DB, query: str) -> None:
    db.execute(query)
    print(db.result())
    