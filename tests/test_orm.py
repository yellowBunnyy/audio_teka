import time
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import insert
import pytest

from src.adapters import orm
from src import config
from src.domain import model




@pytest.fixture
def tear_down():
    session = session_postgres()
    yield session
    clean_table()


def clean_table():
    session = session_postgres()
    session.query(model.Title).delete()
    session.commit()


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Baza Postgres się nie uruchomiła")


def create_engine_postgres():
    db_uri = config.get_postgres_uri()
    engine = create_engine(db_uri)
    wait_for_postgres_to_come_up(engine)
    orm.metadata_obj.create_all(engine)
    return engine


def session_postgres():
    session = Session(create_engine_postgres())
    return session


def add_title(title):
    session = session_postgres()
    session.add(model.Title(title))
    session.commit()


def test_add_title_to_source(tear_down):
    session = tear_down
    title_to_add = "Hostel"
    add_title(title_to_add)
    assert session.query(model.Title).all() == [model.Title(title_to_add)]


def test_add_few_titles(tear_down):
    session = tear_down
    titles_to_add = ["Hostel", "John", "Wick"]
    for title in titles_to_add:
        add_title(title)
    assert session.query(model.Title).all() == [
        model.Title(title) for title in titles_to_add
    ]
