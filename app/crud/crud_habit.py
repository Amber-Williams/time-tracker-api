from sqlalchemy.orm import Session

from app import models, schemas

def get_user_habits(db: Session, user_id: str):
    return db.query(models.Habit).filter(
        models.Habit.user_id == user_id, 
        models.Habit.is_deleted == False
        ).all()

def add_user_habit(db: Session, habit_create: schemas.HabitCreate):
    db_habit = models.Habit(
        user_id=habit_create.user_id,
        name=habit_create.name
    )

    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit
