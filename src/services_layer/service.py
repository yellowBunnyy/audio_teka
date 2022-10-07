from sqlalchemy.orm import Session
from src.domain import schemas
from src.adapters import repository


class TitleExistingInSource(Exception):
    pass


class NotTitleInSourceException(Exception):
    pass


def add_title(title: str, session: Session, repository: repository.AbstractRepository):
    existing_title = repository.get(title)
    if existing_title:
        raise TitleExistingInSource("Title: {title} exists in source!")
    repository.add(title)
    session.commit()
    return schemas.TitleSchema(title=title)


def get_title(title: str, repository: repository.AbstractRepository):
    title_to_find = repository.get(title)
    if not title_to_find:
        raise NotTitleInSourceException(f"Can't find title: {title}.")
    return schemas.TitleSchema(title=title_to_find)
