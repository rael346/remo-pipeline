import sqlite3
from peewee import SqliteDatabase
import os

# Initialize Peewee database
db = SqliteDatabase('remo.db')

class Database:
    def __init__(self):
        self.db = db  # Use Peewee's database instance
        self._init_db()

    def _init_db(self):
        # Connect to the database
        self.db.connect()
        files = os.listdir('sql')
        for file in files:
            with open(f'sql/{file}', 'r') as f:
                query = f.read()
                # Use Peewee's execution method
                self.db.execute_sql(query)

    def query(self, query):
        with self.db.connection_context():  # Peewee's context manager for safe queries
            cursor = self.db.execute_sql(query)
            rows = cursor.fetchall()
            self.db.commit()  # Commit explicitly if needed
            return rows


# Initialize Database
old_db_instance = Database()