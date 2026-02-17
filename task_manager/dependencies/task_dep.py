from services.task_service import TaskService
from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies.db_dep import get_db

def get_task_services(db: Session = Depends(get_db)):
    return TaskService(db)