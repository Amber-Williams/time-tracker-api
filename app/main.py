from typing import List, Optional

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from mangum import Mangum

from crud import crud_habit, crud_daily
from database import SessionLocal, engine
from models import Base
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="time tracker api", root_path_in_servers=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/test/{test}")
def root(test: str):
    return {"message": test}


@app.get("/habit/{user_id}", response_model=List[schemas.Habit])
def read_user_habits(user_id: str, db: Session = Depends(get_db)):
    db_habits = crud_habit.get_user_habits(db=db, user_id=user_id)
    return db_habits


@app.post("/habit", response_model=schemas.Habit, status_code=201)
def create_user_habit(habit_create: schemas.HabitCreate, db: Session = Depends(get_db)):
    db_habit = crud_habit.add_user_habit(db=db, habit_create=habit_create)
    return db_habit


@app.put("/habit", response_model=schemas.Habit)
def update_user_habit(habit_edit: schemas.HabitEdit, db: Session = Depends(get_db)):
    db_habit = crud_habit.update_user_habit(db=db, habit_edit=habit_edit)
    return db_habit


@app.delete("/habit", status_code=204)
def delete_user_habit(habit_delete: schemas.HabitDelete, db: Session = Depends(get_db)):
    db_habit = crud_habit.delete_user_habit(db=db, habit_delete=habit_delete)
    return db_habit


@app.get("/daily/{user_id}", response_model=List[schemas.Daily])
def read_user_dailies(user_id: str, start: Optional[str] = None, end: Optional[str] = None, db: Session = Depends(get_db)):
    if start and end:
        db_daily = crud_daily.get_user_daily_range(
            db=db,
            user_id=user_id,
            start=start,
            end=end)
    else:
        db_daily = crud_daily.get_user_dailies(db=db, user_id=user_id)
    return db_daily


@app.post("/daily", response_model=schemas.Daily, status_code=201)
def create_user_daily(daily_create: schemas.DailyCreate, db: Session = Depends(get_db)):
    habits = crud_habit.get_habits_from_strings(
        db=db, str_habits=daily_create.habits)
    db_daily = crud_daily.add_user_daily(
        db=db, daily_create=daily_create, habits=habits)
    return db_daily


@app.put("/daily", response_model=schemas.Daily)
def update_user_daily(daily_edit: schemas.DailyEdit, db: Session = Depends(get_db)):
    habits = crud_habit.get_habits_from_strings(
        db=db, str_habits=daily_edit.habits)
    db_daily = crud_daily.update_user_daily(
        db=db, daily_id=daily_edit.daily_id, habits=habits)
    return db_daily


handler = Mangum(app)
