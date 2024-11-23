from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BookDto(BaseModel):
    isbn: str = Field(..., min_length=13, max_length=13)
    title: str
    creators: str
    copyright_date: date
    summary: str
    series_name_position: Optional[str] = None
    genres: str
    form: str
    format: str
    pages: str
    type: str
    publisher: Optional[str] = None
    publication_date: Optional[date] = None
    awards: Optional[str] = None
    reading_level: Optional[str] = None
    banned_book: bool = Field(False, description="Default is False")
    topics: Optional[str] = None
    subjects: Optional[str] = None
    target_audience: Optional[str] = None
    alternate_titles: Optional[str] = None
