import re
import logging
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as xml_ET

from .base import BaseFeedHandler

logger = logging.getLogger("bleepingcomputer")

class BleepingComputer(BaseFeedHandler):
    
    name: str = "Bleeping Computer"
    match_pattern: re.Pattern = re.compile(r"^.*bleepingcomputer.com/")
    
    def __init__(self, url: str) -> "BleepingComputer":
        super().__init__(url)
        self.feed_url = "https://www.bleepingcomputer.com/feed/"

        # update base headers
        self.headers["Referer"] = "https://www.bleepingcomputer.com/news/"
        
    def parse(self, content: str):
        soup = BeautifulSoup(content, "html.parser")
        post = soup.findAll("article")[0]       
        
        # cleanup the soup
        for div in post.find_all("div", {"class": "cz-related-article-wrapp"}):
            div.decompose()
        for div in post.find_all("div", {"class": "cz-news-story-title-section"}):
            div.decompose()
            
        
        # save the article
        file_path = self.save_markdown(post)
        
        return file_path
    
    def get_latest_news(self) -> list[str]:
        urls = []
        
        res = requests.get(self.feed_url, headers=self.headers)
        root = xml_ET.fromstring(res.text)
        for item in root.find("channel").findall("item"):
            urls.append(item.find("link").text)
            
        logger.info(f"got {len(urls)} urls from feed")
        return urls