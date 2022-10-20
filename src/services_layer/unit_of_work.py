from abc import ABC, abstractmethod


from src.adapters import repository

class AbstractUnitOfWork(ABC):
    def __exit__(self, *args):
        self.rollback()
    
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session = self.session_factory()
        self.repo = repository.SQLReopsitory(self.session)


    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
        print(*args)

    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()