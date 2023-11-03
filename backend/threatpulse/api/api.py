from fastapi import FastAPI
import logging
from ..logger import setup_logger

app = FastAPI()

# setting up logging
logger = logging.getLogger("api")

# make uvicorn and fastapi use the same logger as the root logger
logging.getLogger("uvicorn").handlers = logging.getLogger().handlers
logging.getLogger("uvicorn.access").handlers = logging.getLogger().handlers

@app.get("/health")
def healthcheck():
    return "ok"