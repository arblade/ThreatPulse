import re
import logging
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import markdownify

from .base import BaseFeedHandler

logger = logging.getLogger("checkpointresearch")

class CheckPointResearchHandler(BaseFeedHandler):
    
    name: str = "Check Point Research"
    match_pattern: re.Pattern = re.compile(r".*\.checkpoint.com/")
    
    def __init__(self, url: str) -> "CheckPointResearchHandler":
        super().__init__(url)
        
        # update base headers
        self.headers["Referer"] = "https://research.checkpoint.com/"
        
    def parse(self, content: str):
        soup = BeautifulSoup(content, "html.parser")
        post = soup.find(id="single-post")       
        post_content = post.encode_contents().decode()
        
        # extract iocs
        iocs = [ioc.text for ioc in post.find(id="iocs").findNext("pre").contents if isinstance(ioc, NavigableString)]
        iocs = [ioc for ioc_list in iocs for ioc in ioc_list.split(" ")]
        
        # get article as markdown
        md_text = markdownify.markdownify(post_content)
        with open("res.md", "w") as f:
            f.write(md_text)
        
        return iocs