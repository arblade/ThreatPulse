import sqlite3
import logging

logger = logging.getLogger("db")

class DB:
    def __init__(self, path: str = "db.sqlite"):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        
        # init db with tables
        self.create_tables()
        
    def create_tables(self):
        logger.debug("starting migrations")
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS `articles` (
            `id` INT NOT NULL PRIMARY KEY,
            `url` TEXT NOT NULL,
            `date_scraped` DATE NOT NULL,
            `file_path` TEXT NOT NULL,
            `features` TEXT
        );         
        """)