from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from src.domain import schemas, events
from tests.conftest import engine, SessionLocal
from src.services_layer import unit_of_work, messagebus, handlers
from src.adapters import orm


orm.metadata_obj.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db().close()


@app.get("/ping", response_class=HTMLResponse)
def pong():
    data = {
        "ping": "pong"
    }
    html_response=f"""
    <h1>
        Welcome to FastAPI/albo co tam chcemy.
        {data['ping']}.
    </h1>
    """
    return HTMLResponse(html_response)

@app.post("/add_title/", response_model=schemas.TitleSchema)
def create_title(title: schemas.TitleSchema, session_factory: Session = Depends(get_db)):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    try:
        event = events.AddBookTitle(title=title.title)
        result = messagebus.handle(event, uow)
        return result.pop(0)
    except handlers.TitleExistingInSource:
        raise HTTPException(status_code=400, detail=f"title: {title.title} is in db!!")

@app.get("/get_title/", response_model=schemas.ResponseToClient)
def get_title(title: str, session_factory: Session = Depends(get_db)):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    try:
        event = events.GetBookTitle(title=title)
        result = messagebus.handle(event, uow)
        response = {"status_code": 200,
        "message": f"Title {result.pop(0)} in sutsription."}
        return schemas.ResponseToClient(**response)
    except handlers.NotTitleInSourceException:
        raise HTTPException(status_code=200, detail=f"title: {title} not in subscription!!")

@app.get("/fill_db")
def load_all_items_to_db(session_factory: Session = Depends(get_db)):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    event = events.SaveAllTitlesInDB()
    # result = messagebus.handle(event, uow)
    handlers.save_all_titles_to_db(event=event, uow=uow)
    response = {"status_code": 200,
                "message": "db was upload"}
    return response
