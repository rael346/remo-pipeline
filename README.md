# ReMo Pipeline

- A data pipeline to clean up book data for [ReMo](https://remo.app/)

## Prerequisite 

This project use the following technologies:

- [uv](https://docs.astral.sh/uv/) - a drop-in replacement for `pip` (very similar to `npm`)

- [tailwindcss](https://tailwindcss.com/) + [daisyui](https://daisyui.com/) - CSS utility libaries 
- [Datastar](https://data-star.dev/) - Hypermedia framework for UI interactivity

- [fastapi](https://fastapi.tiangolo.com/) - backend framework 
- [pymarc](https://gitlab.com/pymarc/pymarc) - parsing marc records
- [SQLModel](https://sqlmodel.tiangolo.com/) - ORM that integrates well with Pydantic and Fastapi
- [SQLite](https://www.sqlite.org/) - Database, mainly for ease of use

## Development 
1. Create a virtual environment for the project (basically an `npm install`)
```sh
uv sync
```

2. Run the app
```sh
# run the app through uv
uv run fastapi dev app/main.py

# run the app through .venv
source ./.venv/bin/activate
fastapi dev app/main.py
```

3. When you are ready to commit your changes run

```sh
# For linting
uvx ruff check

# For formatting
uvx ruff format
```
