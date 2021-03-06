from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def get_user_habits(db: Session, user_id: str):
    return db.query(models.Habit).filter(
        models.Habit.user_id == user_id,
        models.Habit.is_deleted == False
    ).all()


def get_habit(db: Session, habit_id: str):
    return db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.is_deleted == False
    ).first()


def get_habits_from_strings(db: Session, str_habits: List[str]):
    habits = []
    for habit_id in str_habits:
        habit = get_habit(db=db, habit_id=habit_id)
        habits.append(habit)
    return habits


def add_user_habit(db: Session, habit_create: schemas.HabitCreate):
    db_habit = models.Habit(
        user_id=habit_create.user_id,
        name=habit_create.name
    )

    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def update_user_habit(db: Session, habit_edit: schemas.HabitEdit):
    db_habit = get_habit(db=db, habit_id=habit_edit.habit_id)
    db_habit.name = habit_edit.name

    db.commit()
    db.refresh(db_habit)
    return db_habit


def delete_user_habit(db: Session, habit_delete: schemas.HabitDelete):
    db_habit = get_habit(db=db, habit_id=habit_delete.habit_id)
    db_habit.is_deleted = True

    db.commit()
    db.refresh(db_habit)
    return None
