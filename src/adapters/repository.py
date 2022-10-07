from abc import ABC, abstractmethod
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
    def delete(self, title: schemas.TitleSchema):
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

    def delete(self, title: str):
        pass

    def delete_all(self):
        self.session.query(model.Title).delete()
