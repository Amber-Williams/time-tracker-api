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
    db_habit = crud_habit.add_user_habit(db=db, habit_create=habit_create)
    return db_habit

@app.put("/habits", response_model=schemas.Habit)
def update_user_habit(habit_edit: schemas.HabitEdit, db: Session = Depends(get_db)):
    db_habit = crud_habit.update_user_habit(db=db, habit_edit=habit_edit)
    return db_habit

@app.get("/daily/{user_id}", response_model=List[schemas.Daily])
def read_user_dailies(user_id: str, db: Session = Depends(get_db)):
    db_daily = crud_daily.get_user_dailies(db=db, user_id=user_id)
    return db_daily

@app.post("/daily", response_model=schemas.Daily)
def create_user_daily(daily_create: schemas.DailyCreate, db: Session = Depends(get_db)):
    habits = crud_habit.get_habits_from_strings(db=db, str_habits=daily_create.habits)
    db_daily = crud_daily.add_user_daily(db=db, daily_create=daily_create, habits=habits)
    return db_daily

@app.put("/daily", response_model=schemas.Daily)
def update_user_daily(daily_edit: schemas.DailyEdit, db: Session = Depends(get_db)):
    habits = crud_habit.get_habits_from_strings(db=db, str_habits=daily_edit.habits)
    db_daily = crud_daily.update_user_daily(db=db, daily_id=daily_edit.daily_id, habits=habits)
    return db_daily
