FROM node:lts-slim

# TODO: remove once the backend simulation is gone
RUN apt-get update && apt-get install -y python3 python3-venv
RUN mkdir -p /tmp/python_deps
COPY frontend/back_simulation/requirements.txt /tmp/requirements.txt
RUN cd /tmp && python3 -m venv venv && venv/bin/python3 -m pip install -r /tmp/requirements.txt

RUN mkdir -p /app
WORKDIR /app