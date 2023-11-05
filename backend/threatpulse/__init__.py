import argparse
import json
import traceback
import threading

from .logger import setup_logger
from .db.db import DB

logger = setup_logger()

def parse_args():
    parser = argparse.ArgumentParser(prog="ctiexplorer")
    subparsers = parser.add_subparsers(title="commands", dest="command")
    
    # serve the api
    api_parser = subparsers.add_parser("serve", help="Serve the API")
    api_parser.add_argument("--host", help="Host on which serving the API", default="0.0.0.0")
    api_parser.add_argument("-p", "--port", help="Port on which serving the API", default=1234)
    
    # parse an url
    article_parser = subparsers.add_parser("parse", help="Parse an URL")
    article_parser.add_argument("url", help="Url to parse")
    
    # fetch latest articles
    fetch_parser = subparsers.add_parser("fetch", help="Fetch latest articles")
    
    return parser.parse_args()
    

def main():
    args = parse_args()
    
    # parsing an article
    if args.command == "parse":
        from .newsfeed.feed import find_handler
        from .newsfeed.handlers.base import BaseFeedHandler

        # get the correct handler for the url
        HandlerClass: BaseFeedHandler = find_handler(args.url)
        if HandlerClass is None:
            logger.error(f"No suitable handler found for site: {args.url}")
            return
        handler = HandlerClass(args.url)
        
        # fetch and parse the content
        content = handler.fetch()
        article = handler.parse(content)
        
        # init the db
        db = DB()
        
    # serving the API
    elif args.command == "serve":
        import uvicorn
        uvicorn.run(app="threatpulse.api.api:app", host=args.host, port=args.port, log_level=logger.level, reload=True)
        
    # else testing new features
    elif args.command == "fetch":
        from .newsfeed.handlers import HANDLERS
        
        
        def fetch(HandlerClass):
            # init the DB
            db = DB()
            
            # get urls on the feed page
            handler = HandlerClass(None)
            urls = handler.get_latest_news()
            for url in urls:
                # if url is already in db, skip it
                if db.is_url_in_db(url):
                    logger.info(f"Url {url} is already in the DB, skipping it")
                    continue
                
                handler = HandlerClass(url)
                content = handler.fetch()
                try:
                    article = handler.parse(content)
                    db.add_article(article)
                except Exception as e:
                    logger.error(f"Error while parsing url: {url}\n{e}")
                    traceback.print_exc()
                    continue
        
        threads = [None for _ in range(len(HANDLERS))]
        for i, HandlerClass in enumerate(HANDLERS):
            logger.info(f"Fetching new content for {HandlerClass.name}")
            threads[i] = threading.Thread(target=fetch, args=[HandlerClass])
            threads[i].start()
            
        for i in range(len(HANDLERS)):
            threads[i].join()
            