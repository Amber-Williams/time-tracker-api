from typing import List, Optional
from enum import Enum
from datetime import date

from pydantic import BaseModel, Field


class Habit(BaseModel):
    id: str
    user_id: str
    name: str

    class Config:
        orm_mode = True

class Daily(BaseModel):
    id: str
    date: date
    habits: List[Habit] = []

    class Config:
        orm_mode = True

class HabitCreate(BaseModel):
    user_id: str
    name: str = Field(..., max_length=128)

class HabitEdit(BaseModel):
    user_id: str
    habit_id: str
    name: str = Field(..., max_length=128)

class HabitDelete(BaseModel):
    user_id: str
    habit_id: str

class DailyCreate(BaseModel):
    user_id: str
    date: str
    habits: List[str] = []

class DailyEdit(BaseModel):
    user_id: str
    daily_id: str
    habits: List[str] = []
