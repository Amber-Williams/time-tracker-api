from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field

class Habit(BaseModel):
    id: str
    user_id: str
    name: str

    class Config:
        orm_mode = True

class Daily(BaseModel):
    id: str
    date: str
    habits: List[Habit] = []

    class Config:
        orm_mode = True

class HabitCreate(BaseModel):
    user_id: str
    name: str = Field(..., max_length=128)

class HabitEdit(BaseModel):
    habit_id: str
    user_id: str
    name: str = Field(..., max_length=128)

class HabitDelete(BaseModel):
    habit_id: str
    user_id: str

class DailyCreate(BaseModel):
    user_id: str
    date: str
    habits: List[str] = []

class DailyEdit(BaseModel):
    daily_id: str
    user_id: str
    habits: List[str] = []
