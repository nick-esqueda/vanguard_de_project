import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("etl/data/spotify.db")
        self.curs = self.conn.cursor()
        
    def execute(self, query):
        with self.conn:
            self.curs.execute(query)
            
    def result(self):
        return self.curs.fetchall()
        
    def close(self): 
        self.conn.close()