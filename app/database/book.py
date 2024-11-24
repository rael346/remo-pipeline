from datetime import date
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    # TODO: finish adding fields to this table
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    creators: str = Field(nullable=False)
    copyright_date: date = Field(nullable=False)
    summary: str = Field(nullable=False)
    isbn: int = Field(max_digits=13, unique=True, nullable=False)
