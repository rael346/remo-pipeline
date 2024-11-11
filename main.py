from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import Database
from jinja2 import Template
from humanize import naturalsize
from base64 import b64decode

from datastar import stream_template
from parse import MarcFile, parse_marc


app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = Database()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


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
