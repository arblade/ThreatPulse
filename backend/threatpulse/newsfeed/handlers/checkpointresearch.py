import re
import logging
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from .base import BaseFeedHandler
from ..mdconverter import MDConverter

logger = logging.getLogger("checkpointresearch")


class CheckPointResearchHandler(BaseFeedHandler):
    
    name: str = "Check Point Research"
    match_pattern: re.Pattern = re.compile(r".*\.checkpoint.com/")
    
    def __init__(self, url: str) -> "CheckPointResearchHandler":
        super().__init__(url)
        self.feed_url = "https://research.checkpoint.com/latest-publications/"
        
        # update base headers
        self.headers["Referer"] = "https://research.checkpoint.com/"
        
    def parse(self, content: str):
        soup = BeautifulSoup(content, "html.parser")
        post = soup.find(id="single-post")
        
        # cleanup
        for div in post.find_all("div", {"class": "aside-box"}):
            div.decompose()
        for div in post.find_all("div", {"class": "back-to-top"}):
            div.decompose()
        for div in post.find_all("div", {"class": "button-wrap"}):
            div.decompose()

        # extract iocs
        # iocs = [ioc.text for ioc in post.find(id="iocs").findNext("pre").contents if isinstance(ioc, NavigableString)]
        # iocs = [ioc for ioc_list in iocs for ioc in ioc_list.split(" ")]
        
        # save the article
        self.save_markdown(post)
        
        return []
    
    def get_latest_news(self) -> list[str]:
        urls = []
        
        res = requests.get(self.feed_url, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        posts = soup.find("section", {"class": "blog-post-wrapper"})
        for link in posts.find_all("div", {"class": "button-wrap"}):
            urls.append(link.find("a")["href"])

        logger.info(f"got {len(urls)} urls from feed")
        return urls