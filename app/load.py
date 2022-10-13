from pandas import DataFrame
from .utils import DB, db_table_names, db_table_queries
from .utils import DB, db_view_names, db_view_queries


# TABLE CREATION ################################
def create_tables(db: DB) -> None:
    """
    this function will create all of the pre-determined set of DB tables,
    using the SQL queries provided by db_tables.py.
    
    NOTE: all tables are dropped before executing the "CREATE TABLE" queries 
    again. this is to pick up on any future changes to the tables.
    """
    for t_name, t_query in zip(db_table_names, db_table_queries):
        db.execute(f"DROP TABLE IF EXISTS {t_name}")
        db.execute(t_query)
        
# INSERTION #####################################
def load_data(data: DataFrame, tablename: str, db: DB) -> None:
    """
    this function inserts the given data into the specified table using the
    DB connection object, and prints a confirmation message to the terminal
    after insertion.
    """
    data.to_sql(tablename, db.conn, if_exists="replace", index=False)
    print(f"Finished loading data into table: {tablename}")

# VIEW CREATION #################################
def create_views(db: DB) -> None:
    """
    this function will create all of the pre-determined set of views, 
    using the SQL queries provided by db_views.py.
    
    NOTE: all views are dropped before executing the "CREATE VIEW" queries 
    again. this is to pick up on any future changes to the views.
    """
    for v_name, v_query in zip(db_view_names, db_view_queries):
        db.execute(f"DROP VIEW IF EXISTS {v_name};")
        db.execute(v_query)
