from abc import ABC, abstractmethod
from sqlalchemy import text, delete
from typing import Dict
import pdb

from src.domain import model, schemas


class AbstractRepository(ABC):
    
    def __init__(self):
        self.seen = []
        
    def add(self, title: str):
        self._add(title)
        self.seen.append(title)

    def get(self, title:str)-> schemas.TitleSchema:
        title = self._get(title)
        if title:
            self.seen.append(title)
        return title

    def _add(self):
        raise NotImplementedError
    
    def _get(self):
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
        super().__init__()
        

    def _add(self, title: str):
        db_title = model.Title(title=title)
        self.session.add(db_title)
        return f"added {title}"

    def _get(self, title: str)-> schemas.TitleSchema:
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
