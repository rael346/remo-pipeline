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
    # Normalize column names once
    sheet.rename(columns=lambda x: x.strip().replace(" ", "_").replace("/", "_"), inplace=True)
    # Detect problematic column names
    title_column = next((col for col in sheet.columns if col.startswith("Title")), None)
    reading_level_column = next(
        (col for col in sheet.columns if col in ["Lexile", "Reading_Level"]), None
    )

    for row in sheet.itertuples(index=False):
        entries.append(
            Incomplete(
                id=None,
                isbn=row.ISBN,
                title=getattr(row, title_column),
                creators=row.Author,
                copyright_date=row.Copyright_date if "Copyright_date" in sheet.columns else "",
                summary=row.Summary if "Summary" in sheet.columns else "",
                series=row.Series_Title if "Series_title" in sheet.columns else "",
                genre=row.Genre if "Genre" in sheet.columns else "",
                form=row.Form if "Form" in sheet.columns else "",
                format=row.Format if "Format" in sheet.columns else "",
                pages=row.Pages if "Pages" in sheet.columns else "",
                book_type=row.Book_Type if "Book_Type" in sheet.columns else "",
                publisher=row.Publisher,
                publication_date=row.Publication_Year if "Publication_Year" in sheet.columns else "",
                awards=row.Awards if "Awards" in sheet.columns else "",
                reading_level=getattr(row, reading_level_column),
                topics=row.Topics if "Topics" in sheet.columns else "",
                subjects=row.Subjects if "Subjects" in sheet.columns else "",
                target_audience=row.Target_Audience if "Target_Audience" in sheet.columns else "",
                banned_book=row.Banned_Book if "Banned_Book" in sheet.columns else "",
                alternate_titles=row.Alternate_Titles if "Alternate_Titles" in sheet.columns else "",
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
