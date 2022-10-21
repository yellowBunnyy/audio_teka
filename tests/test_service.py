import pytest
import pdb

from src.domain import schemas, preprocessing
from src.adapters import repository
from src.services_layer import service, unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self, source):
        self.titles_source = set(source)

    def add(self, title: str):
        self.titles_source.add(title)

    def get(self, title: str):
        title_source = [schemas.TitleSchema(title=book_title) for book_title in self.titles_source]
        try:
            return next(
                (
                    audiobook_title
                    for audiobook_title in title_source
                    if audiobook_title.title == title
                )
            )
        except StopIteration:
            return None

    def delete_single_title(self, title, _get_id):
        finded_title = [
            book_title for book_title in self.titles_source if book_title == title
        ][0]
        get_id = _get_id(title)
        return {get_id: finded_title}

    def delete_all(self):
        self.titles_source = set()

    def _get_id(self, title):
        return 1
    
    def get_all_rows(self):
        return list(self.titles_source)

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.repo = FakeRepository([])
        self.commited = False

    def __enter__(self):
        self.repo

    def commit(self):
        self.commited = True
    
    def rollback(self):
        pass

class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


def test_add_title_first_time():
    uow = FakeUnitOfWork()
    title_to_add = "Korona"
    service.add_title(title_to_add, uow)
    assert uow.repo.get(title_to_add) == schemas.TitleSchema(title=title_to_add)
    assert uow.commited


def test_add_title_to_db_when_we_have_others_titles():
    uow = FakeUnitOfWork()
    titles_in_db = ["Korona", "Gra o Tron", "Wiedzmin"]
    uow.repo.titles_source = set(titles_in_db)
    title_to_add = "Kanibal"
    service.add_title(title_to_add, uow)
    rows = uow.repo.get_all_rows()
    assert sorted(rows) == sorted(["Korona", "Gra o Tron", "Wiedzmin", title_to_add])
    assert uow.commited


def test_unhappy_path_add_same_string_second_time():
    uow = FakeUnitOfWork()
    title = "Marek"
    service.add_title(title, uow)
    with pytest.raises(
        service.TitleExistingInSource, match="Title: {title} exists in source!"
    ):
        service.add_title(title, uow)


def test_happy_path_get_title():
    uow = FakeUnitOfWork()
    uow.repo.titles_source = set(["John", "Denerys"])
    title_to_find = "Denerys"
    assert service.get_title(title_to_find, uow).title == title_to_find


def test_unhappy_path_get_not_existing_title():
    not_existing_title = "Wall"
    uow = FakeUnitOfWork()
    uow.repo.titles_source = set(["John", "Denerys"])
    with pytest.raises(
        service.NotTitleInSourceException,
        match=f"Can't find title: {not_existing_title}.",
    ):
        service.get_title(not_existing_title, uow).title


def test_happy_patch_delete_single_row():
    title_to_remove = "Juzek"
    uow = FakeUnitOfWork()
    uow.repo.titles_source = set(["Damian", title_to_remove])
    row = service.delete_single_row(title_to_remove, uow)
    assert row == {1: title_to_remove}
    assert uow.commited


def test_unhappy_path_remove_single_row():
    title_to_remove = "Ala"
    uow = FakeUnitOfWork()
    uow.repo.titles_source = set([])
    with pytest.raises(service.NotTitleInSourceException, match=f"Can't find title: {title_to_remove}."):
        service.delete_single_row(title_to_remove, uow)

def test_happy_patch_delete_all_rows():
    uow = FakeUnitOfWork()
    uow.repo.titles_source = ["Damian", "Waldek"]
    empty_db = service.delete_all_rows(uow)
    assert empty_db == []
    assert uow.commited
    

def test_save_all_title_from_file_to_db():
    uow = FakeUnitOfWork()
    data_to_add = preprocessing.main()
    service.save_all_titles_to_db(uow)
    assert len(uow.repo.get_all_rows()) == len(data_to_add)
    assert uow.commited
