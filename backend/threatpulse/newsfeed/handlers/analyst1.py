import re
import logging
from bs4 import BeautifulSoup

from .base import BaseFeedHandler

logger = logging.getLogger("analyst1")

class Analyst1Handler(BaseFeedHandler):
    
    name: str = "Analyst1"
    match_pattern: re.Pattern = re.compile(r"^.*analyst1.com/")
    
    def __init__(self, url: str) -> "Analyst1Handler":
        super().__init__(url)

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
        
        # save the article
        file_path = self.save_markdown(post)
        
        return file_path