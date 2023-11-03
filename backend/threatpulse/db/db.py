import sqlite3
import logging

logger = logging.getLogger("db")

class DB:
    def __init__(self, path: str = "db.sqlite"):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        
    def create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXIST articles
        
        ;              
        """)