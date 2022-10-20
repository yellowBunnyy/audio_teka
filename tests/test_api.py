from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import requests
import pytest
import pdb

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
        model.Title(title="Aligator")
    ]
    engine = postgres_create_engine()
    with Session(engine) as session:
        for title in titles:
            session.add(title)
            session.commit()



def test_happy_path_ping():
    url = f"{config.get_api_url()}/ping"
    r = requests.get(url)
    assert r.status_code == 200
    # assert r.json()["title"] == "pong"


def test_add_title_to_source(tear_down):
    data = {"title": "Marian"}
    url = f"{config.get_api_url()}/add_title"
    r = requests.post(url, json=data)
    assert r.status_code == 200
    assert r.json()["title"] == "Marian"


def test_unhappy_path_trying_add_same_title_twice(tear_down):
    data = {"title": "Marian"}
    url = f"{config.get_api_url()}/add_title"
    r = requests.post(url, json=data)
    assert r.status_code == 200
    r = requests.post(url, json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == f"title: Marian is in db!!"


def test_get_book_title_from_source(tear_down):
    add_rows_to_db()
    searched_book_title = "Aligator"
    data = {"title":searched_book_title}
    url = f"{config.get_api_url()}/get_title"
    r = requests.get(url, json=data)
    assert r.status_code == 200
    assert r.json()["title"] == "Aligator"

# def test_foo():
#     searched_book_title = "Abi ma pla"
#     data = {"title":searched_book_title}
#     url = f"{config.get_api_url()}/get_title"
#     r = requests.get(url, json=data)
#     assert r.status_code == 200
#     assert r.json()["title"] == searched_book_title
