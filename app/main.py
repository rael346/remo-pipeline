import io
from base64 import b64decode
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from humanize import naturalsize
from jinja2 import Template

from app.database import incomplete
from app.database.db import SessionDep, create_db_and_tables
from app.datastar import stream_template
from app.parse import IncompleteFile, parse_marc, parse_xml, parse_excel


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="./app/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"is_more_files": False}
    )


@app.post("/upload")
async def upload_files(request: Request, session: SessionDep):
    body = await request.json()
    files = body["files"]
    filesMimes = body["filesMimes"]
    filesNames = body["filesNames"]
    file_result: dict[str, IncompleteFile] = {}

    for file, mime, name in zip(files, filesMimes, filesNames):
        print(name)
        decoded_bytes: bytes = b64decode(file)
        if mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            entries = parse_excel(decoded_bytes)

            file_result[name] = {
                "mime": mime,
                "size": naturalsize(len(decoded_bytes)),
                "entries": entries,
            }
            incomplete.insert_incompletes(session, entries)
        elif mime == "marc_file":
            entries = parse_marc(decoded_bytes)

            file_result[name] = {
                "mime": mime,
                "size": naturalsize(len(decoded_bytes)),
                "entries": entries,
            }
            incomplete.insert_incompletes(session, entries)
        elif mime == "onyx":
            entries = parse_xml(decoded_bytes)

            file_result[name] = {
                "mime": mime,
                "size": naturalsize(len(decoded_bytes)),
                "entries": entries,
            }
            incomplete.insert_incompletes(session, entries)

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
