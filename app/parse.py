import io
from io import BytesIO

from pymarc import Field, MARCReader
from typing import TypedDict
from lxml import etree
from pandas import pandas, DataFrame
from app.database.incomplete import Incomplete


class IncompleteFile(TypedDict):
    mime: str
    size: str
    entries: list[Incomplete]


def map_fields(fields: list[Field]) -> list[str]:
    return list(map(lambda field: field.value(), fields))


def parse_marc(content: bytes) -> list[Incomplete]:
    reader = MARCReader(content, file_encoding="latin-1")
    entries: list[Incomplete] = []
    for record in reader:
        if record is None:
            # TODO: what to do with these exceptions
            # print(
            #     "Current chunk:",
            #     reader.current_chunk,
            #     "was ignored because exceptions\n",
            #     reader.current_exception,
            #     "\n",
            # )
            continue

        entries.append(
            Incomplete(
                title=record.title,
                creators=record.author,
                copyright_date=record.pubyear,
                summary="\n".join(map_fields(record.notes)),
                series="\n".join(map_fields(record.series)),
                genre="",  # TODO: add genre parser for marc files
                form="",  # TODO: add form parser for marc files
                format="",  # TODO: add format parser for marc files
                isbn=record.isbn,
                pages="\n".join(map_fields(record.physicaldescription)),
                book_type="",  # TODO: add book type parser for marc files
            )
        )

    return entries

def parse_excel(content: bytes) -> list[Incomplete]:
    entries: list[Incomplete] = []
    # Create a file-like object from the decoded bytes
    file_like: BytesIO = io.BytesIO(content)
    sheet = pandas.read_excel(file_like)
    # Replace bogus values with empty strings
    sheet.fillna("", inplace=True)

    for _, row in sheet.iterrows():
        entries.append(
            Incomplete(
                title=row["Title/Subtitle"],
                creators=row["Author"],
                publication_date=row["Publication Year"],
                series=row["Series Title"],
                genre="",  # TODO: Add genre parser for Excel files
                form="",  # TODO: Add form parser for Excel files
                format="",  # TODO: Add format parser for Excel files
                isbn=row["ISBN"],
                publisher=row["Publisher"],
                book_type="",  # TODO: Add book type parser for Excel files
            )
        )

    return entries

def get_local_tag(tag) -> str:
    return etree.QName(tag).localname

def parse_xml(content: bytes):
    # TODO: Finish ONIX parsing
    root = etree.fromstring(content)
    for product in root.findall("{*}Product"):
        isbn_10_row = product.find(
            "{*}ProductIdentifier/[{*}ProductIDType='02']/{*}IDValue"
        )
        isbn_10 = isbn_10_row.text if isbn_10_row is not None else None
        print("ISBN 10: ", isbn_10)

        isbn_13_row = product.find(
            "{*}ProductIdentifier/[{*}ProductIDType='15']/{*}IDValue"
        )
        isbn_13 = isbn_13_row.text if isbn_13_row is not None else None
        print("ISBN 13: ", isbn_13)
