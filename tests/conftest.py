import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pytest

from src import config
from src.adapters import orm


def my_engine():
    uri = config.get_postgres_uri()
    print(uri)
    engine = create_engine(uri)
    print("-"*10)
    print("engin was created")
    print("-"*9)
    return engine

def wait_for_postgres_to_come_up(engine):
    print("Wating for establish connection...")
    c = 0
    while True:
        try:
            print(f"tries: {c}")
            connection = engine.connect()
            print("was connected")
            create_table_title_in_db(engine)
            return connection
        except OperationalError:
            time.sleep(1)
        c+=1

def create_table_title_in_db(engine):
    orm.metadata_obj.create_all(bind=engine)
    print(f"table 'title' was created")


engine = my_engine()
wait_for_postgres_to_come_up(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
