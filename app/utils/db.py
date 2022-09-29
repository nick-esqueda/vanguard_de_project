import sqlite3


class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("app/data/spotify.db")
        self.curs = self.conn.cursor()
        
    def execute(self, query: str) -> None:
        with self.conn:
            self.curs.execute(query)
            
    def result(self) -> list[tuple]:
        return self.curs.fetchall()
        
    def close(self) -> None: 
        self.conn.close()