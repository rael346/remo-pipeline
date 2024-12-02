from sqlmodel import Field, SQLModel


class TextFeatures(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    isbn: str = Field(max_digits=13, nullable=False)
