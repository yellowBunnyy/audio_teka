from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import text
import pytest
import pdb


from src.adapters import repository
from src import config
from src.domain import model


@pytest.fixture
def tear_down():
    session = postgres_db_session()
    yield session
    clean_table(session)


def clean_table(session):
    session.query(model.Title).delete()
    session.commit()


def postgres_create_engine():
    db_uri = config.get_postgres_uri()
    return create_engine(db_uri)


def postgres_db_session():
    session = Session(postgres_create_engine())
    return session


def add_rows_to_db():
    titles = [
        model.Title(title="Marian"),
        model.Title(title="W pustyni i w puszczy"),
        model.Title(title="Armagedon"),
        model.Title(title="Kanibal"),
    ]
    engine = postgres_create_engine()
    with Session(engine) as session:
        for title in titles:
            session.add(title)
            session.commit()


def test_remove_all_rows_from_source(tear_down):
    add_rows_to_db()
    session = tear_down
    repo = repository.SQLReopsitory(session)
    repo.delete_all()
    assert session.query(model.Title).all() == []


def test_delete_selected_row_in_table(tear_down):
    add_rows_to_db()
    title_to_remove = "Armagedon"
    session = tear_down
    repo = repository.SQLReopsitory(session)
    get_id = repo._get_id
    repo.delete_single_title(title_to_remove, get_id)
    rows = session.query(model.Title).all()
    assert rows == [
        model.Title(title="Marian"),
        model.Title(title="W pustyni i w puszczy"),
        model.Title(title="Kanibal"),
    ]


def test_add_single_title_to_source(tear_down):
    session = tear_down
    title_to_add = "Pan Tadeusz"
    repo = repository.SQLReopsitory(session)
    repo.add(title_to_add)
    rows = session.query(model.Title).all()
    assert rows == [model.Title(title=title_to_add)]


def test_get_single_row_from_table(tear_down):
    add_rows_to_db()
    title = "Kanibal"
    session = tear_down
    repo = repository.SQLReopsitory(session)
    row = repo.get(title)
    assert row == model.Title(title=title)
