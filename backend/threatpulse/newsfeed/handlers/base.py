from abc import ABCMeta, abstractmethod
import re
import requests
import logging
import os
from bs4 import BeautifulSoup

from ..mdconverter import MDConverter

logger = logging.getLogger("basefeedhandler")

class BaseFeedHandler(metaclass=ABCMeta):
    """Base class for news feed handler.
    Each site is supposed to have it's own handler


    """
    
    name: str = "Base"
    match_pattern: re.Pattern = re.compile(r"^.*$")
    headers: dict = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Connection": "keep-alive",
        "Accept-Language": "en-US;q=0.8"
    }
    
    def __init__(self, url: str) -> "BaseFeedHandler":
        self.url = url
    
    def fetch(self) -> str:
        res = requests.get(self.url, headers=self.headers)
        return res.text
    
    def save_markdown(self, soup: BeautifulSoup, data_folder: str = "./data") -> str:
        md_text = MDConverter(self, heading_style="ATX").convert_soup(soup)
        
        # post processing
        md_text = md_text.strip()
        md_text = md_text.replace("\n\n", "\n")
        
        # get name from url
        slug_re = re.findall(r"/([\w-]+)?/", self.url, re.IGNORECASE)
        if slug_re is None:
            logger.error(f"cannot find the slug in {self.url}")
            return None
        slug = slug_re[-1]
        logger.debug(f"save_markdown: slug = {slug}")    
        
        # save the text to the disk
        file_path = os.path.join(data_folder, f"{slug}.md")
        with open(file_path, "w") as f:
            f.write(md_text)
        
        # returrn the path
        return file_path
            
    @abstractmethod
    def parse(self, content: str):
        pass