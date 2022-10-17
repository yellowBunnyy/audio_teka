import pytest
from unittest.mock import patch
import pdb

from src.adapters import repository
from src.services_layer import service


class FakeRepository(repository.AbstractRepository):
    def __init__(self, source):
        self.titles_source = set(source)

    def add(self, title: str):
        self.titles_source.add(title)

    def get(self, title: str):
        try:
            return next(
                (
                    audiobook_title
                    for audiobook_title in self.titles_source
                    if audiobook_title == title
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
        return "delete"

    def _get_id(self, title):
        return 1


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


def test_add_title_first_time():
    session = FakeSession()
    repo = FakeRepository([])
    title = "Marek"
    service.add_title(title, session, repo)
    assert repo.titles_source == {"Marek"}
    assert session.commited


def test_unhappy_path_add_same_string_second_time():
    session = FakeSession()
    title = "Marek"
    repo = FakeRepository([title])
    with pytest.raises(
        service.TitleExistingInSource, match="Title: {title} exists in source!"
    ):
        service.add_title(title, session, repo)


def test_happy_path_get_title():
    repo = FakeRepository(["John", "Denerys"])
    title_to_find = "Denerys"
    assert service.get_title(title_to_find, repo).title == title_to_find


def test_unhappy_path_get_not_existing_title():
    not_existing_title = "Wall"
    repo = FakeRepository(["John", "Denerys"])
    with pytest.raises(
        service.NotTitleInSourceException,
        match=f"Can't find title: {not_existing_title}.",
    ):
        service.get_title(not_existing_title, repo).title


def test_happy_patch_delete_single_row():
    title_to_remove = "Juzek"
    session = FakeSession()
    repo = FakeRepository(["Damian", title_to_remove])
    row = service.delete_single_row(title_to_remove, session, repo)
    assert row == {1: title_to_remove}
