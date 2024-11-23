from peewee import Model, AutoField, CharField, TextField, DateField, BooleanField

import db


class BookEntity(Model):
    book_id = AutoField(primary_key=True)  # Auto-incrementing primary key
    isbn = CharField(max_length=13, unique=True, null=False)  # CHAR(13) NOT NULL
    title = CharField(max_length=100, null=False)  # VARCHAR(100) NOT NULL
    creators = TextField(null=False)  # VARCHAR NOT NULL
    copyright_date = DateField(null=False)  # DATE NOT NULL
    summary = TextField(null=False)  # VARCHAR NOT NULL
    series_name_position = TextField(null=True)  # VARCHAR (optional)
    genres = TextField(null=False)  # VARCHAR NOT NULL
    form = TextField(null=False)  # VARCHAR NOT NULL
    format = TextField(null=False)  # VARCHAR NOT NULL
    pages = TextField(null=False)  # VARCHAR NOT NULL
    type = TextField(null=False)  # VARCHAR NOT NULL
    publisher = TextField(null=True)  # VARCHAR (optional)
    publication_date = DateField(null=True)  # DATE (optional)
    awards = TextField(null=True)  # VARCHAR (optional)
    reading_level = TextField(null=True)  # VARCHAR (optional)
    banned_book = BooleanField(default=False)  # BOOLEAN DEFAULT FALSE
    topics = TextField(null=True)  # VARCHAR (optional)
    subjects = TextField(null=True)  # VARCHAR (optional)
    target_audience = TextField(null=True)  # VARCHAR (optional)
    alternate_titles = TextField(null=True)  # VARCHAR (optional)

    class Meta:
        database = db
        table_name = "BOOK"
