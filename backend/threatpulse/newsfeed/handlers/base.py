from abc import ABCMeta, abstractmethod
import re
import requests
import logging

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
    
    def fetch(self):
        res = requests.get(self.url, headers=self.headers)
        return res.text
            
    @abstractmethod
    def parse(self, content: str):
        pass