import argparse
import json
import traceback

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
    
    # test something
    test_parser = subparsers.add_parser("test", help="Test a new feature")
    
    return parser.parse_args()

def get_keywords_from_markdown(text: str, limit: int = 10, score_threshold: int = 14):
    # cleanup text
    import re
    # remove images
    text = re.sub(r"!\[(.+?)\]\(.+?\)", r"", text)
    # remove links
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    # remove styling
    text = text.replace("**", "")
    text = text.replace("### ", "")
    text = text.replace("## ", "")
    text = text.replace("# ", "")
    
    # download models
    import nltk
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
    
    # extract keywords
    from rake_nltk import Rake
    r = Rake()
    r.extract_keywords_from_text(text)
    
    # process best words
    keywords_scored = sorted(r.get_word_degrees().items(), key=lambda x: x[1], reverse=True)
    keywords_scored = [k for k in keywords_scored if k[1] >= score_threshold and len(k[0]) >= 3 and not k[0].isdigit()]
    keywords = [k for k in keywords_scored[:limit]]
    
    return keywords
    

def main():
    args = parse_args()
    
    # parsing an article
    if args.command == "parse":
        from .newsfeed.feed import find_handler
        from .newsfeed.handlers.base import BaseFeedHandler
        from .db.db import DB

        # get the correct handler for the url
        HandlerClass: BaseFeedHandler = find_handler(args.url)
        if HandlerClass is None:
            logger.error(f"No suitable handler found for site: {args.url}")
            return
        handler = HandlerClass(args.url)
        
        # fetch and parse the content
        content = handler.fetch()
        md_text = handler.parse(content)
        logger.info(f"Keywords: {get_keywords_from_markdown(md_text, 10)}")
        
        # init the db
        db = DB()
        
    # serving the API
    elif args.command == "serve":
        import uvicorn
        uvicorn.run(app="threatpulse.api.api:app", host=args.host, port=args.port, log_level=logger.level)
        
    # else testing new features
    elif args.command == "test":
        from .newsfeed.handlers import HANDLERS
        
        for HandlerClass in HANDLERS:
            logger.info(f"Fetching new content for {HandlerClass.name}")
            handler = HandlerClass(None)
            urls = handler.get_latest_news()
            for url in urls:
                handler = HandlerClass(url)
                content = handler.fetch()
                try:
                    md_text = handler.parse(content)
                    kw = get_keywords_from_markdown(md_text, 10)
                    
                    # with open("keywords.json", "a") as f:
                    #     f.write(json.dumps(kw)+"\n")
                except Exception as e:
                    logger.error(e)
                    traceback.print_exc()
                    continue