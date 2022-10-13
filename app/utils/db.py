import sqlite3
from pandas import DataFrame


class DB:
    """
    instances of this class are used to interact with the SQLite database.
    upon instantiation, an immediate connection to "spotify.db" is made. 
    """
    def __init__(self) -> None:
        self.conn = sqlite3.connect("app/data/spotify.db")
        self.curs = self.conn.cursor()
        
    def execute(self, query: str) -> None:
        """
        this will run the query against the DB. 
        must use self.result() to see the output of that query.
        """
        with self.conn:
            self.curs.execute(query)
            
    def result(self) -> list[tuple]:
        """
        outputs the results of the sql query most recently provided
        to self.execute(). 
        """
        return self.curs.fetchall()
        
    def query(self, query: str) -> DataFrame:
        """
        runs the given query against the database, and returns the results
        (as a Pandas DataFrame).
        a separate query will be run to retrieve the column names from the
        SQLite DB, and those column names will be set on the DataFrame.
        """
        self.execute(query)
        df = DataFrame(self.result())
        curs = self.conn.execute(query)
        df.columns = [col_name[0] for col_name in curs.description]
        return df
                
    def close(self) -> None: 
        """
        close the connection to the SQLite database. 
        it is not necessary but highly recommended to close the connection
        after all desired interactions with the DB are done.
        """
        self.conn.close()