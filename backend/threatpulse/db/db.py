import sqlite3
import logging

from .models import Article

logger = logging.getLogger("db")


class DB:
    def __init__(self, path: str = "db.sqlite"):
        self.path = path
        self.conn = sqlite3.connect(self.path)

        # init db with tables
        self.create_tables()

    def create_tables(self):
        logger.debug("starting migrations")
        self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS `articles` (
            `id` INTEGER PRIMARY KEY,
            `title` TEXT NOT NULL,
            `description` TEXT,
            `illustration` TEXT,
            `url` TEXT NOT NULL,
            `date_scraped` DATE NOT NULL,
            `file_path` TEXT NOT NULL,
            `features` TEXT,
            `keywords` TEXT,
            `source` TEXT NOT NULL
        );         
        """
        )

    def add_article(self, article: Article):
        logger.debug("adding article to db")

        # check the url is not already in the db
        cursor = self.conn.cursor()
        if (
            cursor.execute(
                f"SELECT url FROM articles WHERE url='{article.url}';"
            ).fetchall()
            != []
        ):
            logger.warning(f"article with url: {article.url} already in the DB")
            return

        query = """
        INSERT INTO articles (url, title, description, illustration, date_scraped, file_path, features, keywords, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(
            query,
            (
                article.url,
                article.title,
                article.description,
                article.illustration,
                article.date_scraped,
                article.file_path,
                article.serialize_features(),
                article.serialize_keywords(),
                article.source,
            ),
        )
        self.conn.commit()

    def get_articles(self, limit: int = 10) -> list[Article]:
        logger.debug("fetching articles from db")

        cursor = self.conn.cursor()
        rows = cursor.execute(
            f"SELECT * FROM articles ORDER BY date_scraped DESC LIMIT {limit};"
        )
        articles = [Article.from_row(row) for row in rows]
        return articles

    def get_article(self, id: int) -> Article:
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT * FROM articles WHERE id='{id}'").fetchone()

        if row is None:
            logger.error(f"article with with {id} not found")
            return None

        return Article.from_row(row)

    def get_article_text(self, id: int) -> str:
        article = self.get_article(id)
        if article is None:
            return None

        return article.get_text()

    def is_url_in_db(self, url: str) -> bool:
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT * FROM articles WHERE url='{url}';").fetchone()
        return row is not None
