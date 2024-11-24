from sqlmodel import Field, Session, SQLModel


class Incomplete(SQLModel, table=True):
    # Required
    # This id field can be None, see https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str | None = Field(default=None, nullable=True)
    creators: str | None = Field(default=None, nullable=True)
    copyright_date: str | None = Field(default=None, nullable=True)
    summary: str | None = Field(default=None, nullable=True)
    series: str | None = Field(default=None, nullable=True)
    genre: str | None = Field(default=None, nullable=True)
    form: str | None = Field(default=None, nullable=True)
    format: str | None = Field(default=None, nullable=True)
    pages: str | None = Field(default=None, nullable=True)
    isbn: str | None = Field(default=None, nullable=True)
    book_type: str | None = Field(default=None, nullable=True)

    # Optional
    publisher: str | None = Field(default=None, nullable=True)
    publication_date: str | None = Field(default=None, nullable=True)
    awards: str | None = Field(default=None, nullable=True)
    reading_level: str | None = Field(default=None, nullable=True)

    # Nice to have
    topics: str | None = Field(default=None, nullable=True)
    subjects: str | None = Field(default=None, nullable=True)
    target_audience: str | None = Field(default=None, nullable=True)
    banned_book: str | None = Field(default=None, nullable=True)
    alternate_titles: str | None = Field(default=None, nullable=True)


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
