from base64 import b64decode
from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from humanize import naturalsize
from jinja2 import Template
from starlette.status import HTTP_201_CREATED

from datastar import stream_template
from models.dtos.BookDto import BookDto
from models.entities.BookEntity import BookEntity
from models.mappers.BookMapper import BookMapper
from parse import MarcFile, parse_marc

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


external_data = {
    "isbn": "9783161484100",
    "title": "Example Book Title",
    "creators": "Author Name",
    "copyright_date": date(2021, 1, 1),
    "summary": "This is an example summary for the book.",
    "series_name_position": "Series Name, Book 1",
    "genres": "Fiction",
    "form": "Paperback",
    "format": "Standard",
    "pages": "350",
    "type": "Novel",
    "publisher": "Example Publisher",
    "publication_date": date(2021, 5, 20),
    "awards": "Best Book Award",
    "reading_level": "Advanced",
    "banned_book": False,
    "topics": "Adventure, Exploration",
    "subjects": "Literature",
    "target_audience": "Adults",
    "alternate_titles": "The Example Book",
}


@app.get("/book/{isbn}", response_model=BookDto)
async def get_book_by_isbn(isbn: str) -> BookDto:
    book = BookDto(**external_data)
    book.isbn = isbn
    return book


@app.post("/book", response_description="201")
async def create_book(book: BookDto):
    # Create a new book record for testing
    new_book = BookEntity.create(
        isbn="9783161484100",
        title="Super Derp!!",
        creators="Author Name",
        copyright_date="2021-01-01",
        summary="Awesome badassery adventures",
        genres="Fiction",
        form="Paperback",
        format="Standard",
        pages="350",
        type="Novel",
        publisher="Example Publisher",
        publication_date="2021-05-20",
        awards="Best Book Award",
        reading_level="Advanced",
        banned_book=False,
        topics="Adventure, Exploration",
        subjects="Literature",
        target_audience="Adults",
        alternate_titles="The Example Book",
    )
    print(f"Book created: {new_book.title} with ID {new_book.book_id}")
    book_entity = BookMapper.dto_to_entity(book)
    book_entity.save()
    return HTTP_201_CREATED


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
