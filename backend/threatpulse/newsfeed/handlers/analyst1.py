import re
import logging
from bs4 import BeautifulSoup
from bs4.element import NavigableString

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
        with open("res.html", "w") as f:
            f.write(content) 
        # # extract iocs
        # iocs = [ioc.text for ioc in soup.find(id="iocs").findNext("pre").contents if isinstance(ioc, NavigableString)]
        # iocs = [ioc for ioc_list in iocs for ioc in ioc_list.split(" ")]
        
        # return iocs