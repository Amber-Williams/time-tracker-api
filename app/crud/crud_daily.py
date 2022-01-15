from typing import List

from sqlalchemy import Date
from sqlalchemy.orm import Session
from dateutil import parser

from app import models, schemas

def get_user_daily_range(db: Session, user_id: str, start: Date, end: Date):
    return db.query(models.Daily).filter(
        models.Daily.user_id == user_id, 
            Daily.date >= start, Daily.date <= end
        )

def get_user_dailies(db: Session, user_id: str):
    return db.query(models.Daily).filter(
        models.Daily.user_id == user_id
        ).all()

def add_user_daily(db: Session, daily_create: schemas.DailyCreate, habits: List[schemas.Habit]):
    daily = models.Daily(
        user_id=daily_create.user_id,
        date=parser.parse(daily_create.date),
        habits=habits
    )
    db.add(daily)
    db.commit()
    db.refresh(daily)
    return daily
