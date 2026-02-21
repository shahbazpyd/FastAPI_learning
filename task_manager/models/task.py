from argparse import BooleanOptionalAction
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from db.base import Base
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"))

