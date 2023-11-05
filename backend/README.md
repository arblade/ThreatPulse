# Threatpulse backend

To install dependencies for the project, run the following commands:

```bash
cd ./backend/
poetry install

# enable the context
poetry shell
threatpulse -h
```

## Test scenario

To try the API:

```bash
# fetch latest articles
threatpulse test

# serve the api
threatpulse serve
```