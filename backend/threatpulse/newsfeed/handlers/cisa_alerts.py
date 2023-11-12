import re
import logging
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import BaseFeedHandler
from ..features import get_keywords_from_markdown
from ...db.models import Article

logger = logging.getLogger("cisa_alerts")


class CISAAlertsHandler(BaseFeedHandler):
    name: str = "CISA Alerts"
    match_pattern: re.Pattern = re.compile(r".*\.cisa.gov/")

    def __init__(self, url: str) -> "CISAAlertsHandler":
        super().__init__(url)
        self.feed_url = "https://www.cisa.gov/stopransomware/official-alerts-statements-cisa"

        # update base headers
        self.headers["Referer"] = "https://www.cisa.gov/stopransomware/official-alerts-statements-cisa"

    def parse(self, content: str):
        soup = BeautifulSoup(content, "html.parser")

        # title ans illustration extraction        
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
            
        post = soup.find(id="main")
        
        # cleanup
        cleanup_classes = ["c-page-title__meta", "l-full__footer"]
        for cleanup_class in cleanup_classes:
            try:
                for div in post.find_all("div", {"class": cleanup_class}):
                    div.decompose()
            except:
                pass

        if post is None:
            logger.error("Could not find the post in the page")

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
            source=CISAAlertsHandler.name,
        )
        return article

    def get_latest_news(self) -> list[str]:
        urls = []

        res = requests.get(self.feed_url, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        posts = soup.find("div", {"class": "l-sidebar__main"}).find("ul")
        for link in posts.find_all("strong"):
            if link.find("a") is None:
                logger.warn("No url found in link")
                continue
            
            url = link.find("a")["href"]
             
            # if the url is relative
            if not url.startswith("http://") or not url.startswith("https://"):
                url = urljoin(self.feed_url, url)
                
            # check that the handler can handle this url
            if not self.match_pattern.match(url):
                logger.warning(f"Handler cannot handle this url: {url}")
                continue
            
            # TODO: remove
            # continue if PDF
            if url.lower().endswith(".pdf"):
                continue
            
            urls.append(url)

        logger.info(f"got {len(urls)} urls from feed")
        return urls
