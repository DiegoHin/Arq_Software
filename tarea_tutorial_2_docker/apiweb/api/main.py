from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, Date

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/v1/")
async def root():
    return "version 1"

#consulta objetivo

#http://172.17.0.2:12333/v1/news/?from_=2021-10-28&to_=2021-10-29
#@app.get("/v1/news/", response_model=List[schemas.news])
#def get_news(from_: str, to_= str, db: Session = Depends(get_db)):
#    gnbd = crud.get_news_by_date(db, from_ = from_, to_ = to_)
#    return gnbd

#http://172.17.0.2:12333/v1/news/?category=deporte
#@app.get("/v1/news/", response_model=List[schemas.news])
#def get_news(category: str, db: Session = Depends(get_db)):
#    gnbc = crud.get_news_by_category(db, category=category)
#    return gnbc

#http://127.0.0.1:8000/v1/news/?from_=2021-10-25&to_=2021-10-30&category=deporte   
#tendencia, politica
@app.get("/v1/news/", response_model=List[schemas.news])
def get_news(from_: str, to_:str, category: str, db: Session = Depends(get_db)):
    getnews = crud.get_news_final(db, from_=from_, to_=to_, category=category)
    return getnews