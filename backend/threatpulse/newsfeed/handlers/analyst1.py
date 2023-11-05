import re
import datetime
import logging
import requests
from bs4 import BeautifulSoup

from .base import BaseFeedHandler
from ..features import get_keywords_from_markdown
from ...db.models import Article

logger = logging.getLogger("analyst1")


class Analyst1Handler(BaseFeedHandler):
    name: str = "Analyst1"
    match_pattern: re.Pattern = re.compile(r"^.*analyst1.com/")

    def __init__(self, url: str) -> "Analyst1Handler":
        super().__init__(url)
        self.feed_url = "https://analyst1.com/category/blog/"

        # update base headers
        self.headers["Referer"] = "https://analyst1.com/category/blog/"

    def parse(self, content: str) -> Article:
        soup = BeautifulSoup(content, "html.parser")
        post = soup.findAll("article", {"class": "post"})[0]
        title = soup.findAll("meta", {"property": "og:title"})
        if len(title) > 0:
            title = title[0].get("content", "")

        else:
            title = "Not found"
            logger.warning("[parse] title not found")
        description = soup.findAll("meta", {"property": "og:description"})
        if len(description) > 0:
            description = description[0].get("content", "")
        else:
            description = ""
            logger.warning("[parse] description not found")
        illustration = soup.findAll("meta", {"property": "og:image"})
        if len(illustration) > 0:
            illustration = illustration[0].get("content", "")
            logger.warning("[parse] illustration not found")
        else:
            illustration = "Not found"
        # cleanup the soup
        for div in post.find_all("div", {"class": "cta"}):
            div.decompose()
        for el in post.find_all("span", {"class": "ez-toc-title-toggle"}):
            el.decompose()
        for div in post.find_all("div", {"class": "content-single__info"}):
            div.decompose()

        # save the article
        file_path, md_text = self.save_markdown(post)

        # get keywords
        keywords = get_keywords_from_markdown(md_text, limit=5)
        logger.info(f"Keywords: {keywords}")

        # build the article object
        article = Article(
            id=None,
            title=title,
            description=description,
            illustration=illustration,
            url=self.url,
            date_scraped=datetime.datetime.now(),
            file_path=file_path,
            features=[],
            keywords=keywords,
            source=Analyst1Handler.name,
        )
        return article

    def get_latest_news(self) -> list[str]:
        urls = []

        res = requests.get(self.feed_url, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for article in soup.find_all("article", {"class": "status-publish"}):
            link = article.find("a")["href"]
            urls.append(link)

        logger.info(f"got {len(urls)} urls from feed")
        return urls
