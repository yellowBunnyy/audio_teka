from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


# Base = declarative_base()


# class Title(Base):
#     __tablename__ = "titles"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)


class Title:
    def __init__(self, title):
        self.title = title

    def __eq__(self, other):
        if not isinstance(other, Title):
            return False
        return self.title == other.title
