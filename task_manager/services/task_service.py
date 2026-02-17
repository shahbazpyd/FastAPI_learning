from models.task import Task
from schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db):
        self.db = db

    def create_task(self, data: TaskCreate):
        print("data1", data)
        print("data2", data.dict())
        task = Task(**data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.referesh(task)
        return task
    
    def get_tasks(self):
        return self.db.query(Task).all()
    
    def get_task(self, task_id:int):
        return self.db.query(Task).filter(Task.id == task_id).first()
      
    def update(self, task_id: int, data:TaskUpdate):
        task = self.get_task(task_id)
        if not task:
            return None
        
        for key, value in data.model_dump().items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_task(self, task_id: int):
        task = self.get_task(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return task

