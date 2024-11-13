import sqlite3
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('remo.db')
        self.cur = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        files = os.listdir('sql')
        for file in files:
            with open(f'sql/{file}', 'r') as f:
                query = f.read()
                self.cur.execute(query)

    def query(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows