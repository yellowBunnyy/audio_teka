from typing import Dict
import pdb


from src.domain import schemas, preprocessing, events, model
from src.services_layer import unit_of_work


class TitleExistingInSource(Exception):
    pass


class NotTitleInSourceException(Exception):
    pass


def add_title(event: events.AddBookTitle, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        existing_title = uow.repo.get(event.title)
        if existing_title:
            raise TitleExistingInSource("Title: {title} exists in source!")
        uow.repo.add(event.title)
        uow.commit()
        return schemas.TitleSchema(title=event.title)


def get_title(event: events.GetBookTitle, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        title_to_find = uow.repo.get(event.title)
        if not title_to_find:
            raise NotTitleInSourceException(f"Can't find title: {event.title}.")
        return schemas.TitleSchema(title=title_to_find.title)


def delete_single_row(
    event: events.DeleteSingleRow, uow: unit_of_work.AbstractUnitOfWork
) -> Dict:
    with uow:
        title_to_delete = uow.repo.get(event.title)
        if not title_to_delete:
            raise NotTitleInSourceException(f"Can't find title: {event.title}.")
        row = uow.repo.delete_single_title(event.title, uow.repo._get_id)
        uow.commit()
        return row

def delete_all_rows(event:events.DeleteAllRows, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        uow.repo.delete_all()
        uow.commit()
        return uow.repo.get_all_rows()

def save_all_titles_to_db(event: events.SaveAllTitlesInDB, uow: unit_of_work.AbstractUnitOfWork):
    titles = preprocessing.main()
    with uow:
        for title in titles:
            uow.repo.add(title)
        uow.commit()

