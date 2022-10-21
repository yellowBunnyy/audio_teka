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
    with uow:
        existing_title = uow.repo.get(title)
        if existing_title:
            raise TitleExistingInSource("Title: {title} exists in source!")
        uow.repo.add(title)
        uow.commit()
        return schemas.TitleSchema(title=title)


def get_title(title: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        title_to_find = uow.repo.get(title)
        if not title_to_find:
            raise NotTitleInSourceException(f"Can't find title: {title}.")
        return schemas.TitleSchema(title=title_to_find.title)


def delete_single_row(
    title: str, uow: unit_of_work.AbstractUnitOfWork
) -> Dict:
    with uow:
        title_to_delete = uow.repo.get(title)
        if not title_to_delete:
            raise NotTitleInSourceException(f"Can't find title: {title}.")
        row = uow.repo.delete_single_title(title, uow.repo._get_id)
        uow.commit()
        return row

def delete_all_rows(uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        uow.repo.delete_all()
        uow.commit()
        return uow.repo.get_all_rows()

def save_all_titles_to_db(uow: unit_of_work.AbstractUnitOfWork):
    titles = preprocessing.main()
    with uow:
        for title in titles:
            uow.repo.add(title)
        uow.commit()

