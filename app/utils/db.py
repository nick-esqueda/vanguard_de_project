import sqlite3
from pandas import DataFrame


class DB:
    """
    instances of this class are used to create an immediate connection
    to the SQLite database "spotify.db". 
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
        
    def test(self, query: str) -> None:
        """
        runs the given query against the database, and immediately
        prints the results (as a Pandas DataFrame) to the terminal.
        """
        self.execute(query)
        df = DataFrame(self.result())
        print(df)
        
    def close(self) -> None: 
        """
        close the connection to the SQLite database. 
        it is not necessary but highly recommended to close the connection
        after all desired interactions with the DB are done.
        """
        self.conn.close()