from abc import ABC, abstractmethod
from sqlalchemy import select

class ArstractRepository(ABC):
    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def delete_all():
        raise NotImplementedError

class SQLReopsitory(ArstractRepository):
    def __init__(self, session):
        self.session = session
    
    def add(self, title):
        return self.session.add(title)
    
    # def get(self, title):
    #     return self.session.query().