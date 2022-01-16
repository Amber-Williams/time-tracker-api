from typing import List

from sqlalchemy import Date
from sqlalchemy.orm import Session
from dateutil import parser

from app import models, schemas

def get_daily(db: Session, daily_id: str):
    return db.query(models.Daily).filter(
        models.Daily.id == daily_id
        ).first()

def get_user_daily_range(db: Session, user_id: str, start: Date, end: Date):
    return db.query(models.Daily).filter(
        models.Daily.user_id == user_id, 
            models.Daily.date >= start, models.Daily.date <= end
        ).all()

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

def update_user_daily(db: Session, daily_id: str, habits: List[schemas.Habit]):
    daily = get_daily(db=db, daily_id=daily_id)
    daily.habits = habits

    db.commit()
    db.refresh(daily)
    return daily
