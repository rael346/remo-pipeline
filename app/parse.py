from pymarc import Field, MARCReader
from typing import TypedDict
from lxml import etree


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


def get_local_tag(tag) -> str:
    return etree.QName(tag).localname


def parse_xml(content: bytes):
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
        # descriptive_details = product.findall("{*}DescriptiveDetail")
        # collateral_details = product.findall("{*}CollateralDetail")
        # related_materials = product.findall("{*}RelatedMaterial")
        # product_supply = product.findall("{*}ProductSupply")


with open("./Datasets/ONIX/LEEANDLOW_20210707.xml", "rb") as f:
    parse_xml(f.read())
