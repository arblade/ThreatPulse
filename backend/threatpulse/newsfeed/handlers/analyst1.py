import re
import logging
import requests
from bs4 import BeautifulSoup

from .base import BaseFeedHandler

logger = logging.getLogger("analyst1")

class Analyst1Handler(BaseFeedHandler):
    
    name: str = "Analyst1"
    match_pattern: re.Pattern = re.compile(r"^.*analyst1.com/")
    
    def __init__(self, url: str) -> "Analyst1Handler":
        super().__init__(url)
        self.feed_url = "https://analyst1.com/category/blog/"

        # update base headers
        self.headers["Referer"] = "https://analyst1.com/category/blog/"
        
    def parse(self, content: str):
        soup = BeautifulSoup(content, "html.parser")
        post = soup.findAll("article", {"class": "post"})[0]       
        
        # cleanup the soup
        for div in post.find_all("div", {'class': 'cta'}): 
            div.decompose()
        for el in post.find_all("span", {"class": "ez-toc-title-toggle"}):
            el.decompose()
        for div in post.find_all("div", {"class": "content-single__info"}):
            div.decompose()
        
        # save the article
        md_text = self.save_markdown(post)
        
        return md_text
    
    def get_latest_news(self) -> list[str]:
        urls = []
        
        res = requests.get(self.feed_url, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        for article in soup.find_all("article", {"class": "status-publish"}):
            link = article.find("a")["href"]
            urls.append(link)
        
        logger.info(f"got {len(urls)} urls from feed")
        return urls