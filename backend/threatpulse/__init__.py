import argparse

from .logger import setup_logger

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
        res = handler.parse(content)
        # print(res)
        
    # serving the API
    elif args.command == "serve":
        import uvicorn
        uvicorn.run(app="threatpulse.api.api:app", host=args.host, port=args.port, log_level=logger.level)