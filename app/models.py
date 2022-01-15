import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Habit(Base):
    def __repr__(self):
        return f"<Habit(id={self.id}, user_id={self.user_id}, name={self.name}>"

    __tablename__ = "habit"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    name = Column(String)
    is_deleted = Column(Boolean, default=False)
    daily = Column(String, ForeignKey('daily.id'), nullable=True)


class Daily(Base):
    def __repr__(self):
        return f"<Daily(id={self.id}, user_id={self.user_id}, name={self.name}>"

    __tablename__ = "daily"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    date = Column(DateTime)
    habits = relationship("Habit")
