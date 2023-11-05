import re
import datetime
import logging
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as xml_ET


from ..features import get_keywords_from_markdown
from ...db.models import Article
from .base import BaseFeedHandler

logger = logging.getLogger("sekoia")


class SekoiaHandler(BaseFeedHandler):
    name: str = "Sekoia"
    match_pattern: re.Pattern = re.compile(r"^.*blog.sekoia.io/")

    def __init__(self, url: str) -> "SekoiaHandler":
        super().__init__(url)
        self.feed_url = "https://blog.sekoia.io/"

        # update base headers
        self.headers["Referer"] = "https://blog.sekoia.io/"

    def parse(self, content: str):
        soup = BeautifulSoup(content, "html.parser")
        post_title = soup.find("h1", ["class", "notizia-headline"])
        post = soup.find("div", {"class": "notizia-single-main-content-container"})
        
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
        for div in post.find_all("ul", {"class": "wp-block-yoast-seo-related-links"}):
            div.decompose()
        for div in post.find_all("div", {"class": "notizia-end-share-panel"}):
            div.decompose()
        for div in post.find_all("div", {"class": "notizia-sharing-label"}):
            div.decompose()
        for div in post.find_all("p")[-2:]:
            div.decompose()

        # save the article
        res = soup.new_tag("res")
        res.append(post_title)
        res.append(post)
        file_path, md_text = self.save_markdown(res)

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
            source=SekoiaHandler.name,
        )
        return article

    def get_latest_news(self) -> list[str]:
        urls = []

        res = requests.get(self.feed_url, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        posts = soup.find_all("article", {"class": "type-post"})
        for post in posts:
            urls.append(post.find("a")["href"])

        logger.info(f"got {len(urls)} urls from feed")
        return urls