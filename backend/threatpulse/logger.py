import logging

from .utils import rich_print

class ColorFormatter(logging.Formatter):
    fmt = "[[{}]%(levelname)s[/]] [dim]%(name)-8s[/] || %(message)s"
    
    COLORS = {
        logging.DEBUG: "magenta",
        logging.INFO: "green",
        logging.WARNING: "yellow",
        logging.ERROR: "red",
        logging.CRITICAL: "bold red",
    }
    
    def format(self, record):
        log_fmt = self.fmt.format(self.COLORS[record.levelno])
        formatter = logging.Formatter(log_fmt)
        head, *rest = formatter.format(record).split("||")
        
        return rich_print(head, highlight=False) + "||".join(rest)
    
def setup_logger(level=logging.DEBUG) -> logging.Logger:
    # get root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # create stream handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(ColorFormatter())
    
    # add the handler to the logger
    logger.addHandler(sh)
    
    # create filters
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    return logger