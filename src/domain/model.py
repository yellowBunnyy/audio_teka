from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,primary_key=True, index=True)