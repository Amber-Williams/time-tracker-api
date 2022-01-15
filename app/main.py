from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .crud import crud_habit, crud_daily
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/habits/{user_id}", response_model=List[schemas.Habit])
def read_user_habits(user_id: str, db: Session = Depends(get_db)):
    db_habits = crud_habit.get_user_habits(db=db, user_id=user_id)
    return db_habits

@app.post("/habits", response_model=schemas.Habit)
def create_user_habit(habit_create: schemas.HabitCreate, db: Session = Depends(get_db)):
    db_habits = crud_habit.add_user_habit(db=db, habit_create=habit_create)
    return db_habits

@app.get("/daily/{user_id}", response_model=List[schemas.Daily])
def read_user_dailies(user_id: str, db: Session = Depends(get_db)):
    db_daily = crud_daily.get_user_dailies(db=db, user_id=user_id)
    return db_daily

@app.post("/daily", response_model=schemas.Daily)
def create_user_daily(daily_create: schemas.DailyCreate, db: Session = Depends(get_db)):
    habits = []
    for habit_id in daily_create.habits:
        habit = crud_habit.get_habit(db=db, habit_id=habit_id)
        habits.append(habit)

    db_daily = crud_daily.add_user_daily(db=db, daily_create=daily_create, habits=habits)
    return db_daily
