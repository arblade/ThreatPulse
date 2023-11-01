import logging

from .handlers import HANDLERS
from .handlers.base import BaseFeedHandler

logger = logging.getLogger("newsfeed")

def find_handler(url: str) -> BaseFeedHandler:
    # iterate over the handlers
    for HandlerClass in HANDLERS:
        if HandlerClass.match_pattern.match(url):
            logger.debug(f"Found handler: \"{HandlerClass.name}\" for url: {url}")
            return HandlerClass
        
    # no handler was found for this url
    return None