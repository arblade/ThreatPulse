import argparse

from .newsfeed.feed import find_handler
from .newsfeed.handlers.base import BaseFeedHandler
from .logger import setup_logger

logger = setup_logger()

def parse_args():
    parser = argparse.ArgumentParser(prog="ctiexplorer")
    parser.add_argument("url", help="Url to parse")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # get the correct handler for the url
    HandlerClass: BaseFeedHandler = find_handler(args.url)
    if HandlerClass is None:
        logger.error(f"No suitable handler found for site: {args.url}")
        return
    handler = HandlerClass(args.url)
    
    # fetch and parse the content
    content = handler.fetch()
    res = handler.parse(content)
    # print(res)