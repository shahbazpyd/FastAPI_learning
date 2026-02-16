from models.task import Task
from schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self):
        self.tasks = []
        self.counter = 1

    def create_task(self, data: TaskCreate):
        print("data1", data)
        print("data2", data.dict())
        task = Task(id = self.counter, **data.dict())
        self.tasks.append(task)
        self.counter += 1
        return task
    
    def get_all(self):
        return self.tasks
    
    def get_one(self, task_id:int):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None  
      
    def update(self, task_id: int, data:TaskUpdate):
        task = self.get_one(task_id)
        if not task:
            return None
        
        update_data = data.dict(exclude_unset= True)
        for key, value in update_data.items():
            setattr(task, key, value)

        return task
    
    def delete(self, task_id: int):
        task = self.get_one(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        return True

