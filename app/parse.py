import io
from io import BytesIO

from pymarc import Field, MARCReader
from typing import TypedDict
from lxml import etree
from pandas import pandas
from app.database.incomplete import Incomplete
from .configs.configs import Configs


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
    sheet.rename(
        columns=lambda x: x.strip().replace(" ", "_").replace("/", "_"), inplace=True
    )
    # Detect problematic column names
    title_column = next((col for col in sheet.columns if col.startswith("Title")), None)
    reading_level_column = next(
        (col for col in sheet.columns if col in ["Lexile", "Reading_Level"]), ""
    )

    for row in sheet.itertuples(index=False):
        entries.append(
            Incomplete(
                id=None,
                isbn=row.ISBN if "ISBN" in row else "",
                title=getattr(row, title_column),
                creators=row.Author,
                copyright_date=row.Copyright_date
                if "Copyright_date" in sheet.columns
                else "",
                summary=row.Summary if "Summary" in sheet.columns else "",
                series=row.Series_Title if "Series_title" in sheet.columns else "",
                genre=row.Genre if "Genre" in sheet.columns else "",
                form=row.Form if "Form" in sheet.columns else "",
                format=row.Format if "Format" in sheet.columns else "",
                pages=row.Pages if "Pages" in sheet.columns else "",
                book_type=row.Book_Type if "Book_Type" in sheet.columns else "",
                publisher=row.Publisher if "Publisher" in sheet.columns else "",
                publication_date=row.Publication_Year
                if "Publication_Year" in sheet.columns
                else "",
                awards=row.Awards if "Awards" in sheet.columns else "",
                reading_level=getattr(row, reading_level_column, "")
                if reading_level_column
                else "",
                sub_genres=row.Sub_genres if "Sub_genres" in sheet.columns else "",
                topics=row.Topics if "Topics" in sheet.columns else "",
                subjects=row.Subjects if "Subjects" in sheet.columns else "",
                target_audience=row.Target_Audience
                if "Target_Audience" in sheet.columns
                else "",
                banned_book=row.Banned_Book if "Banned_Book" in sheet.columns else "",
                alternate_titles=row.Alternate_Titles
                if "Alternate_Titles" in sheet.columns
                else "",
                text_features=row.Text_features
                if "Text_features" in sheet.columns
                else "",
            )
        )

    return entries


def get_local_tag(tag) -> str:
    return etree.QName(tag).localname


def parse_xml(content: bytes) -> list[Incomplete]:
    file_like: BytesIO = io.BytesIO(content)
    xml = etree.parse(file_like)
    root = xml.getroot()
    configs: dict[str, dict] = Configs.get_configs()
    entries = []

    for key in configs:
        config = configs[key]
        rows = xml.xpath(config["grain_path"])
        # A row is one grain object, e.g. one book tag
        for row in rows:
            entry = {}
            for column in config["columns"]:
                column_name = column["name"]
                path = column["path"]
                node = row.xpath(path)
                if len(node) > 0:
                    if "text()" in path:
                        value = node[0]
                    else:
                        value = node[0].text
                    entry[column_name] = value
            creators = ""
            if "creator1" in entry:
                creators += entry["creator1"]
            if "creator2" in entry:
                creators += entry["creator2"]
            if "creator3" in entry:
                creators += entry["creator3"]
            entry["creators"] = creators

            summary = ""
            if "shortdescription" in entry:
                summary = entry["shortdescription"]
            elif "longdescription" in entry:
                summary = entry["longdescription"]
            entry["summary"] = summary
            entries.append(Incomplete(**entry))
    return entries
