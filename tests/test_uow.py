import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import pdb

from src import config
from src.domain import model
from src.services_layer import unit_of_work
from src.adapters import repository


@pytest.fixture
def tear_down():
    session_factory = postgres_db_session()
    yield session_factory
    clean_table(session_factory)


def clean_table(session_factory):
    session = session_factory()
    session.query(model.Title).delete()
    session.commit()


def postgres_create_engine():
    db_uri = config.get_postgres_uri()
    return create_engine(db_uri)


def postgres_db_session():
    session_factory = sessionmaker(postgres_create_engine())
    return session_factory


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
            session.close()


def test_uow_can_retrive_title_from_source(tear_down):
    add_rows_to_db()
    session_factory = tear_down
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    title_to_find = "Kanibal"
    with uow:
        finded_title = uow.repo.get(title_to_find)
        assert finded_title == model.Title(title=title_to_find)


def test_uow_add_row_to_source(tear_down):
    session_factory = tear_down
    add_rows_to_db()
    title_to_add = "Kosmos"
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.repo.add(title_to_add)
        uow.commit()
    session = session_factory()
    repo = repository.SQLReopsitory(session)
    rows = repo.get_all_rows()
    assert rows == [
        model.Title(title="Marian"),
        model.Title(title="W pustyni i w puszczy"),
        model.Title(title="Armagedon"),
        model.Title(title="Kanibal"),
        model.Title(title=title_to_add),
    ]
