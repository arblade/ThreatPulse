from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import logging
from ..logger import setup_logger
from ..db.db import DB

app = FastAPI()

# setting up logging
logger = logging.getLogger("api")

# make uvicorn and fastapi use the same logger as the root logger
logging.getLogger("uvicorn").handlers = logging.getLogger().handlers
logging.getLogger("uvicorn.access").handlers = logging.getLogger().handlers

@app.get("/health")
def healthcheck():
    return "healthy"

@app.get("/article")
def list_articles():
    db = DB()
    return db.get_articles()

@app.get("/article/{url}")
def get_article(url: str):
    db = DB()
    return db.get_article(url)

@app.get("/article/{url}/text", response_class=PlainTextResponse)
def get_article_text(url: str):
    db = DB()
    return db.get_article_text(url)