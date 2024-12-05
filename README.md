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

4. Note: We didn't set up any migration so in case you change the models, remove the database files in the root folder and run it again.

## Tech choices
- We went with Python since it has an open source [MARC parser library](https://gitlab.com/pymarc/pymarc) that is still actively maintain
- We chose `uv` for package management since it is more consistent in replicating repos than `pip`
- The rest of the technologies above are mostly preference (wanting to learn new tech, etc)

## Learning
- Parsing multiple files in Python is relatively slow since parsing is a CPU-bounded task, and you can't use multiple threads in Python because of the Global Interpreter Lock (GIL). Future implementation should consider other languages with threading capability like Java or Go if parsing multiple files is a required feature.
- Since the MARC and Excel records are from 'clients' (schools), the entries are entirely unprocessed and contains a lot of missing fields and corrupted entries. So, for data integrity sake, we decided to put records from those files to an `Incomplete` table, where all of the fields in an entry is either `str` or `None`
    - ONIX records are put into a `Book` table where the data type of each field is enforced (date has to be `date`, isbn has to be `CHAR(13)`, etc). This is mainly because ONIX records are from publishers, so we can consider them as a source of truth.
    - Because of time constraint, in the implementation we didn't put the ONIX records in the `Book` table, but the `Incomplete` table instead. This is mainly because ONIX spec is fairly extensive and can take a while to find the field that you need.

## Future works
- A complete pipeline can be something like this:
    - For each of the entries parsed from MARC/Excel records, find if it exist in the `Book` table (contains concrete book metadata) through isbn number.
    - If the entry already exist, then it doesn't need to be added anywhere.
    - If it is not there then use an external API for book metadata (ISBNDB for example) to get the missing fields and also verify that the book exists. 
    - If the entry has all the fields then it can be added to the `Book` table.
    - If the entry is still missing data (since ISBNDB might not provide all the fields that is needed) then the entry is added to the `Incomplete` table for manual processing.
    - Manual processing is basically having people manual entering the missing fields. This can be another UI where the fields gotten from the external API is pre-populated and the user just need to fill in the missing ones. 

- Having another table for file status, since we probably want to keep track of the files that has already been processed in the system.
