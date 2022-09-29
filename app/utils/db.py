import sqlite3


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
        
    def close(self) -> None: 
        """
        close the connection to the SQLite database. 
        it is not necessary but highly recommended to close the connection
        after all desired interactions with the DB are done.
        """
        self.conn.close()