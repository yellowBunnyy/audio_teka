import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pytest

from src import config

def my_engine():
    engine = create_engine(config.get_postgres_uri())
    return engine

def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            connection = engine.connect()
            print("was connected")
            return connection
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


engine = my_engine()
wait_for_postgres_to_come_up(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def postgres_db():
#     wait_for_postgres_to_come_up(engine)
