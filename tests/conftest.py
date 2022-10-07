import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pytest

from src import config
from src.domain import model


def my_engine():
    uri = config.get_postgres_uri()
    print(uri)
    engine = create_engine(uri)
    return engine



def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            connection = engine.connect()
            print("was connected")
            create_table_title_in_db(engine)
            return connection
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")

def create_table_title_in_db(engine):
    model.Base.metadata.create_all(bind=engine)
    print(f"table title was created")


if __name__ == "__main__":
    engine = my_engine()
    wait_for_postgres_to_come_up(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


