from pydantic import BaseModel

class TitleSchema(BaseModel):
    title: str
    class Config:
        orm_mode = True