from models.dtos.BookDto import BookDto
from models.entities.BookEntity import BookEntity

class BookMapper:
    @staticmethod
    def dto_to_entity(dto: BookDto) -> BookEntity:
        return BookEntity(
            isbn=dto.isbn,
            title=dto.title,
            creators=dto.creators,
            copyright_date=dto.copyright_date,
            summary=dto.summary,
            series_name_position=dto.series_name_position,
            genres=dto.genres,
            form=dto.form,
            format=dto.format,
            pages=dto.pages,
            type=dto.type,
            publisher=dto.publisher,
            publication_date=dto.publication_date,
            awards=dto.awards,
            reading_level=dto.reading_level,
            banned_book=dto.banned_book,
            topics=dto.topics,
            subjects=dto.subjects,
            target_audience=dto.target_audience,
            alternate_titles=dto.alternate_titles,
        )

    @staticmethod
    def entity_to_dto(entity: BookEntity) -> BookDto:
        return BookDto(
            isbn=entity.isbn,
            title=entity.title,
            creators=entity.creators,
            copyright_date=entity.copyright_date,
            summary=entity.summary,
            series_name_position=entity.series_name_position,
            genres=entity.genres,
            form=entity.form,
            format=entity.format,
            pages=entity.pages,
            type=entity.type,
            publisher=entity.publisher,
            publication_date=entity.publication_date,
            awards=entity.awards,
            reading_level=entity.reading_level,
            banned_book=entity.banned_book,
            topics=entity.topics,
            subjects=entity.subjects,
            target_audience=entity.target_audience,
            alternate_titles=entity.alternate_titles,
        )