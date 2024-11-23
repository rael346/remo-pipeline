from base64 import b64decode
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from humanize import naturalsize
from jinja2 import Template

from .database.db import SessionDep, create_db_and_tables
from .database.incomplete import Incomplete
from .datastar import stream_template
from .parse import MarcFile, parse_marc


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="./app/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.get("/book")
async def create_book(session: SessionDep):
    incomplete_book = Incomplete(
        title="Example Book Title",
        creators="Author Name",
        copyright_date=date(2021, 1, 1).strftime("%d/%m/%Y, %H:%M:%S"),
        summary="This is an example summary for the book.",
        genre="Fiction",
        form="Paperback",
        format="Standard",
        pages="350",
        book_type="Novel",
        isbn="9783161484100",
    )
    session.add(incomplete_book)
    session.commit()
    session.refresh(incomplete_book)
    return incomplete_book


@app.post("/upload")
async def upload_files(request: Request):
    body = await request.json()
    files = body["files"]
    filesMimes = body["filesMimes"]
    filesNames = body["filesNames"]
    file_result: dict[str, MarcFile] = {}

    for file, mime, name in zip(files, filesMimes, filesNames):
        decoded_bytes = b64decode(file)
        # with open(f"files/{name}", "wb") as f:
        #     f.write(decoded_bytes)
        file_result[name] = {
            "mime": mime,
            "size": naturalsize(len(decoded_bytes)),
            "entries": parse_marc(decoded_bytes),
        }

    results = list(
        map(
            lambda name: (
                name,
                file_result[name]["mime"],
                file_result[name]["size"],
                len(file_result[name]["entries"]),
            ),
            filesNames,
        )
    )

    temp: Template = templates.get_template("upload_result.html")
    frag = temp.render(results=results)
    return stream_template(frag)
