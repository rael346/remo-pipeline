from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine, text


SQLITE_FILE_NAME = "./database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys = on;"))
        connection.execute(text("PRAGMA journal_mode = wal;"))
        connection.execute(text("PRAGMA synchronous = normal;"))
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
