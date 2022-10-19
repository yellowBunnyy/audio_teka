from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pdb

from src.domain import schemas
from src.adapters import repository
from tests.conftest import engine, SessionLocal
from src.services_layer import service
from src.adapters import orm

orm.metadata_obj.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="src/page/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping", response_class=HTMLResponse)
def pong(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("index.html", {"request":request, "data":data})


@app.post("/add_title", response_model=schemas.TitleSchema)
def create_title(title: schemas.TitleSchema, session: Session = Depends(get_db)):
    repo = repository.SQLReopsitory(session)
    try:
        return service.add_title(title.title, session, repo)
    except:
        raise HTTPException(status_code=400, detail=f"title: {title.title} is in db!!")


@app.get("/get_title", response_model=schemas.TitleSchema)
def get_title(title: schemas.TitleSchema, session: Session = Depends(get_db)):
    repo = repository.SQLReopsitory(session)
    try:
        title = service.get_title(title.title, repo)
        return title
    except service.NotTitleInSourceException:
        raise HTTPException(status_code=400, detail=f"title: {title.title} not in db!!")

