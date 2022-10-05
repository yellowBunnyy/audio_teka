from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.domain import schemas
from src.domain import model
from src.adapters.repository import SQLReopsitory
from tests.conftest import engine, SessionLocal

model.Base.metadata.create_all(bind=engine)

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
    repo = SQLReopsitory(session)
    existing_title = repo.get(title.title)
    if existing_title:
        raise HTTPException(status_code=400, detail=f"title: {title.title} is in db!!")
    return repo.add(title)

@app.get("/get_title", response_model=schemas.TitleSchema)
def get_title(title: schemas.TitleSchema, session: Session = Depends(get_db)):
    repo = SQLReopsitory(session)
    title = repo.get(title.title)
    if not title:
        return f"title: {title.title} not in db"
    return title
