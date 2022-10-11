from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import pdb

from src.domain import schemas
from src.adapters import repository
from tests.conftest import engine, SessionLocal
from src.services_layer import service
from src.adapters import orm

orm.metadata_obj.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping", response_model=schemas.TitleSchema)
def pong():
    return schemas.TitleSchema(title="pong")


@app.post("/send_title", response_model=schemas.TitleSchema)
def create_title(title: schemas.TitleSchema, session: Session = Depends(get_db)):
    repo = repository.SQLReopsitory(session)
    try:
        return service.add_title(title.title, session, repo)
    except:
        raise HTTPException(status_code=400, detail=f"title: {title.title} is in db!!")


@app.get("/get_title", response_model=schemas.TitleSchema)
def get_title(title: schemas.TitleSchema, session: Session = Depends(get_db)):
    repo = repository.SQLReopsitory(session)
    title = repo.get(title.title)
    if not title:
        return f"title: {title.title} not in db!!"
    return schemas.TitleSchema(title=title)
