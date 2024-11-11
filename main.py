from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import Database
from jinja2 import Template
from humanize import naturalsize

from datastar import stream_template

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
    results = []
    for file, mime, name in zip(files, filesMimes, filesNames):
        humanize_len = naturalsize(len(file.encode("utf-8")))
        results.append((name, mime, humanize_len))

    temp: Template = templates.get_template("upload_result.html")
    frag = temp.render(results=results)
    return stream_template(frag)
