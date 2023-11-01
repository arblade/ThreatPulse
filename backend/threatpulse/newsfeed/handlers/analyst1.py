import re
import logging
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from .base import BaseFeedHandler
from ..mdconverter import MDConverter

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

        
        # extract iocs
        # iocs = [ioc.text for ioc in post.find(id="iocs").findNext("pre").contents if isinstance(ioc, NavigableString)]
        # iocs = [ioc for ioc_list in iocs for ioc in ioc_list.split(" ")]
        
        # get article as markdown
        md_text = MDConverter(heading_style="ATX").convert_soup(post)
        md_text.strip()
        with open("res.md", "w") as f:
            f.write(md_text)
        
        return ""