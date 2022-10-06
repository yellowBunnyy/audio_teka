from src.adapters import repository
from src.domain import schemas


class FakeRepository(repository.ArstractRepository):
    data = set()

    def __init__(self, session):
        self.session = session

    def add(self, title: schemas.TitleSchema):
        self.data.add(title.title)
        self.session.commit()

    def get(self, title: str):
        return next(
            (
                audiobook_title
                for audiobook_title in self.data
                if audiobook_title == title
            )
        )

    def delete_all(self):
        return "delete"


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


def test_add_title():
    session = FakeSession()
    repo = FakeRepository(session)
    data = schemas.TitleSchema(title="Roman")
    repo.add(data)
    assert repo.get("Roman") == "Roman"
    assert session.commited


def test_get_title():
    session = FakeSession()
    repo = FakeRepository(session)
    repo.data = {"book1", "book2", "book3"}
    assert repo.get("book2") == "book2"
