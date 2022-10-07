from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pytest
import pdb

from src.adapters import repository
from src.domain import schemas
from src import config
from src.domain import model





class FakeRepository(repository.AbstractRepository):
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
    
    def delete(self,title):
        pass


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


def postgres_create_engine():
    db_uri = config.get_postgres_uri()
    return create_engine(db_uri)
    

def postgres_db_session():
    session = Session(postgres_create_engine())
    return session


def add_rows_to_db():
    titles = [model.Title(title="Marian"), model.Title(title="W pustyni i w puszczy"),
    model.Title(title="Armagedon"), model.Title(title="Kanibal")]
    engine = postgres_create_engine()
    with Session(engine) as session:
        for title in titles:
            session.add(title)
            session.commit()

def test_remove_all_rows_from_source():
    add_rows_to_db()
    engine = postgres_create_engine()
    session = Session(engine)
    session.query(model.Title).all()
    repo = repository.SQLReopsitory(session)
    repo.delete_all()
    assert session.query(model.Title).all() == []




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

def test_delete_all_rows_in_table():
    pass
