from sqlmodel import Field, Session, SQLModel


class Incomplete(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None)
    creators: str | None = Field(default=None)
    copyright_date: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    series: str | None = Field(default=None)
    genre: str | None = Field(default=None)
    form: str | None = Field(default=None)
    format: str | None = Field(default=None)
    pages: str | None = Field(default=None)
    book_type: str | None = Field(default=None)
    isbn: str | None = Field(default=None)


def insert_incomplete(session: Session, entry: Incomplete):
    session.add(entry)
    session.commit()
    session.refresh(entry)


def insert_incompletes(session: Session, entries: list[Incomplete]):
    for entry in entries:
        session.add(entry)
    session.commit()
    for entry in entries:
        session.refresh(entry)
