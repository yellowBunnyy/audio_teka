from abc import ABC, abstractmethod
from sqlalchemy import delete, text, select
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

    def delete_single_title(self, title: str):
        title_id = self._get_id(title)
        pass

    def delete_all(self):
        self.session.query(model.Title).delete()

    def _get_id(self, book_title: str = None):
        book_title = "Armagedon"
        stmt = text("SELECT id FROM titles WHERE title=:title")
        stmt = stmt.bindparams(title=book_title)
        [[title_id]] = self.session.execute(stmt).all()
        return title_id
