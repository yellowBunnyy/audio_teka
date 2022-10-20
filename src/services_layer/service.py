from typing import Dict
from sqlalchemy.orm import Session
import pdb


from src.domain import schemas, preprocessing
from src.adapters import repository
from src.services_layer import unit_of_work


class TitleExistingInSource(Exception):
    pass


class NotTitleInSourceException(Exception):
    pass


def add_title(title: str, uow: unit_of_work.AbstractUnitOfWork):
    existing_title = uow.repo.get(title)
    if existing_title:
        raise TitleExistingInSource("Title: {title} exists in source!")
    uow.repo.add(title)
    uow.commit()
    return schemas.TitleSchema(title=title)


def get_title(title: str, repository: repository.AbstractRepository):
    title_to_find = repository.get(title)
    if not title_to_find:
        raise NotTitleInSourceException(f"Can't find title: {title}.")
    return schemas.TitleSchema(title=title_to_find.title)


def delete_single_row(
    title: str, session: Session, repository: repository.AbstractRepository
) -> Dict:
    title_to_delete = repository.get(title)
    if not title_to_delete:
        raise NotTitleInSourceException(f"Can't find title: {title}.")
    get_id = repository._get_id
    row = repository.delete_single_title(title, get_id)
    session.commit()
    return row

def delete_all_rows(session: Session, repository: repository.AbstractRepository):
    repository.delete_all()
    session.commit()
    return repository.get_all_rows()

def save_all_titles_to_db(session:Session, repository: repository.AbstractRepository):
    titles = preprocessing.main()
    for title in titles:
        repository.add(title)
    session.commit()
    
