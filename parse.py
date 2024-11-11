from pymarc import Field, MARCReader
from typing import TypedDict


class MarcEntry(TypedDict):
    title: str | None
    isbn: str | None
    author: str | None
    publisher: str | None
    pub_year: str | None
    issn: str | None
    issnl: str | None
    issn_title: str | None
    sudoc: str | None
    uniform_title: str | None
    location: list[str]
    series: list[str]
    notes: list[str]
    subjects: list[str]
    physical_description: list[str]


class MarcFile(TypedDict):
    mime: str
    size: str
    entries: list[MarcEntry]


def map_fields(fields: list[Field]) -> list[str]:
    return list(map(lambda field: field.value(), fields))


def parse_marc(content: bytes) -> list[MarcEntry]:
    reader = MARCReader(content, file_encoding="latin-1")
    entries: list[MarcEntry] = []
    for record in reader:
        if record is None:
            # print(
            #     "Current chunk:",
            #     reader.current_chunk,
            #     "was ignored because exceptions\n",
            #     reader.current_exception,
            #     "\n",
            # )
            continue

        entries.append(
            {
                "title": record.title,
                "isbn": record.isbn,
                "author": record.author,
                "publisher": record.publisher,
                "pub_year": record.pubyear,
                "issn": record.issn,
                "issnl": record.issnl,
                "issn_title": record.issn_title,
                "sudoc": record.sudoc,
                "uniform_title": record.uniformtitle,
                "location": map_fields(record.location),
                "series": map_fields(record.series),
                "notes": map_fields(record.notes),
                "subjects": map_fields(record.subjects),
                "physical_description": map_fields(record.physicaldescription),
            }
        )

    return entries
