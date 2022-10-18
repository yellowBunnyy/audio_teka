from abc import ABC, abstractmethod
from requests import session
from sqlalchemy import text, delete
from typing import Dict
import pdb


from src.domain import model, schemas


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, title: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, title):
        raise NotImplementedError

    @abstractmethod
    def delete_single_title(self, title: schemas.TitleSchema):
        raise NotImplementedError

    @abstractmethod
    def delete_all():
        raise NotImplementedError
    
    @abstractmethod
    def get_all_rows():
        raise NotImplementedError


class SQLReopsitory(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, title: str):
        db_title = model.Title(title=title)
        self.session.add(db_title)
        return f"added {title}"

    def get(self, title: str):
        return (
            self.session.query(model.Title).filter(model.Title.title == title).first()
        )

    def delete_single_title(self, title: str, _get_id) -> Dict:
        title_id = _get_id(title)
        stmt = text("DELETE FROM titles WHERE id=:title_id")
        stmt = stmt.bindparams(title_id=title_id)
        self.session.execute(stmt)
        return {title_id: title}

    def _get_id(self, book_title: str = None) -> int:
        stmt = text("SELECT id FROM titles WHERE title=:title")
        stmt = stmt.bindparams(title=book_title)
        [[title_id]] = self.session.execute(stmt).all()
        return title_id

    def delete_all(self):
        self.session.query(model.Title).delete()
    
    def get_all_rows(self):
        return self.session.query(model.Title).all()
