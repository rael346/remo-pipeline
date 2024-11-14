from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import Database
from models.dtos.BookDto import BookDto

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = Database()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

external_data = {
    'book_id': 1,
    'isbn': '9783161484100',
    'title': 'Example Book Title',
    'creators': 'Author Name',
    'copyright_date': date(2021, 1, 1),
    'summary': 'This is an example summary for the book.',
    'series_name_position': 'Series Name, Book 1',
    'genres': 'Fiction',
    'form': 'Paperback',
    'format': 'Standard',
    'pages': '350',
    'type': 'Novel',
    'publisher': 'Example Publisher',
    'publication_date': date(2021, 5, 20),
    'awards': 'Best Book Award',
    'reading_level': 'Advanced',
    'banned_book': False,
    'topics': 'Adventure, Exploration',
    'subjects': 'Literature',
    'target_audience': 'Adults',
    'alternate_titles': 'The Example Book'
}
@app.get("/book/{isbn}", response_model=BookDto)
async def get_book_by_isbn(isbn: str) -> BookDto:
    book = BookDto(**external_data)
    book.isbn = isbn
    return book
