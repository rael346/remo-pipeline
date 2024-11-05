# ReMo Pipeline

- A data pipeline to clean up book data for [ReMo](https://remo.app/)

## Prerequisite 

This project use the following technologies:

- [uv](https://docs.astral.sh/uv/) - a drop-in replacement for `pip` (very similar to `npm`)
- [fastapi](https://fastapi.tiangolo.com/) - backend framework 
- [pymarc](https://gitlab.com/pymarc/pymarc) - parsing marc records

## Development 
1. Create a virtual environment for the project (basically an `npm install`)
```sh
uv sync

```
2. Run the app
```sh
# run the app through uv
uv run fastapi dev main.py

# run the app through .venv
source ./.venv/bin/activate
fastapi dev main.py
```
