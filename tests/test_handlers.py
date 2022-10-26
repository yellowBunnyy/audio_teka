from src.adapters import repository
from src.domain import schemas, events
from src.services_layer import unit_of_work, messagebus


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

    def _commit(self):
        self.commited = True
    
    def rollback(self):
        pass



class TestAddTitle:
    def test_for_new_title(self):
        uow = FakeUnitOfWork()
        title_to_add = "Armagedon"
        event = events.AddBookTitle(title=title_to_add)
        messagebus.handle(event, uow)
        assert uow.repo.titles_source == {title_to_add}

class TestGetTitle:
    def test_get_title_from_db(self):
        uow = FakeUnitOfWork()
        uow.repo.titles_source = {"Armagedon", "Kot", "Pies"}
        title_to_find = "Kot"
        event = events.GetBookTitle(title=title_to_find)
        [result] = messagebus.handle(event, uow)
        assert result == schemas.TitleSchema(title=title_to_find)

class TestDeleteSingleRow:
    def test_delete_single_row_from_db(self):
        uow = FakeUnitOfWork()
        uow.repo.titles_source = {"Armagedon", "Kot", "Pies"}
        title_to_remove = "Pies"
        event = events.DeleteSingleRow(title=title_to_remove)
        [result] = messagebus.handle(event, uow)
        assert result == {1:title_to_remove}

class TestDeleteAllRows:
    def test_delete_all_rows_in_db(self):
        uow = FakeUnitOfWork()
        uow.repo.title_source = {"Armagedon", "Kot", "Pies"}
        event = events.DeleteAllRows()
        [result] = messagebus.handle(event, uow)
        assert result == list(set())


