from datetime import date

from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    isbn: int = Field(max_digits=13, unique=True, nullable=False)
    title: str = Field(nullable=False)
    creators: str = Field(nullable=False)
    copyright_date: date = Field(nullable=False)
    summary: str = Field(nullable=False)
    series_name_position: str = Field(nullable=True)
    genres: str = Field(nullable=False)
    form: str = Field(nullable=False)
    format: str = Field(nullable=False)
    pages: str = Field(nullable=False)
    type: str = Field(nullable=False)
    publisher: str = Field(nullable=True)
    publication_date: str = Field(nullable=True)
    awards: str = Field(nullable=True)
    reading_level: str = Field(nullable=True)
    banned_book: bool = Field(nullable=True, default=False)
    topics: str = Field(nullable=True)
    subjects: str = Field(nullable=True)
    target_audience: str = Field(nullable=True)
    alternate_titles: str = Field(nullable=True)
