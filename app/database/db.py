from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine


SQLITE_FILE_NAME = "./database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

Engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(Engine)


def get_session():
    with Session(Engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
