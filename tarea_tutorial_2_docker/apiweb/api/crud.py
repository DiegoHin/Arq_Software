from sqlalchemy.orm import Session
from sqlalchemy import and_, Date
from . import models, schemas

#filtro por fecha
#def get_news_by_date(db: Session, from_: Date, to_: Date):
#    return db.query(models.news).filter(and_(models.news.date >= from_, models.news.date <= to_)).all()

#por categoria
#def get_news_by_category(db: Session, category = str):
#    return db.query(models.news).filter(models.news.category == category).all()

#por ambas
def get_news_final(db: Session, from_: Date, to_: Date, category = str):
    gnf = db.query(models.news).filter(models.news.date >= from_, models.news.date <= to_).all() and db.query(models.news).filter(models.news.category == category).all()
    return gnf