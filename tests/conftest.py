from sqlite3 import connect
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pytest

from src import config


def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            connection = engine.connect()
            print("was connected")
            return connection
        except OperationalError:
            time.sleep(0.5)
    pytest.fail('Postgres never came up')

# postgres_db()