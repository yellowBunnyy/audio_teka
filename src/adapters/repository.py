from abc import ABC, abstractmethod
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
        return self.session.add(title.title)
    
    def get(self, title:str):
        return self.session.query(model.Title).filter(model.Title.title == title).first()
    
    def delete_all():
        return "delete"