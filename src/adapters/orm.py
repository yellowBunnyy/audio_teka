from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy import MetaData

from src.domain import model

metadata_obj = MetaData()
mapper_registry = registry()

title = Table(
    "titles",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255)),
)

mapper_registry.map_imperatively(model.Title, title)
