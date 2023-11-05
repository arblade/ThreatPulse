FROM python:slim


RUN python -m pip install poetry

# create app folder
RUN mkdir -p /app
WORKDIR /app

ENV POETRY_VIRTUALENVS_PATH=/app/venv