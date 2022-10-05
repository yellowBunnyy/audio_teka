from abc import ABC, abstractmethod
import pdb

from src.domain import model, schemas

class ArstractRepository(ABC):
    @abstractmethod
    def add(self, title:schemas.TitleSchema):
        raise NotImplementedError

    @abstractmethod
    def get(self, title:schemas.TitleSchema):
        raise NotImplementedError

    @abstractmethod
    def delete_all():
        raise NotImplementedError

class SQLReopsitory(ArstractRepository):
    def __init__(self, session):
        self.session = session
    
    def add(self, title:schemas.TitleSchema):
        # pdb.set_trace()
        db_title = model.Title(title=title)
        self.session.add(db_title)
        self.session.commit()
        self.session.refresh(db_title)
        return f"added {title.title}"
    
    def get(self, title:str):
        return self.session.query(model.Title).filter(model.Title.title == title).first()
    
    def delete_all():
        return "delete"