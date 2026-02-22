from fastapi import HTTPException
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from models.user import User
from core.cache import get_cache, set_cache
from core.cache import cache_store 
from sqlalchemy import select

class TaskService:
    def __init__(self, db):
        self.db = db

    def _check_owner(self, task, username):
        if task.user_id != self.db.query(User).filter(User.username == username).first().id:
            raise HTTPException(403, "Not authorized")

    def create_task(self, data: TaskCreate, username):
        print("data1", data)
        print("data2", data.dict())
        user = self.db.query(User).filter(User.username == username).first()
        task = Task(title = data.title,
                    description = data.description,
                    user_id = user.id
                    )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        cache_store.clear()
        return task
    
    # def get_tasks(self, limit:int ,skip:int ):

    #     cache_key = f"tasks_{limit}_{skip}"

    #     cached = get_cache(cache_key)
    #     if cached:
    #         print("from cached")
    #         return cached
        
    #     tasks = (
    #         self.db.query(Task)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    #     print("from db")
    #     set_cache(cache_key, tasks, ttl= 10)
    #     return tasks
    
    async def get_tasks(self, limit: int, skip: int):

        cache_key = f"tasks_{limit}_{skip}"

        cached = get_cache(cache_key)
        if cached:
            print("from cached")
            return cached

        stmt = select(Task).offset(skip).limit(limit)

        result = await self.db.execute(stmt)

        tasks = result.scalars().all()

        print("from db")

        set_cache(cache_key, tasks, ttl=10)

        return tasks


    def get_task(self, task_id:int):
        return self.db.query(Task).filter(Task.id == task_id).first()
      
    def update(self, task_id: int, data:TaskUpdate, username):
        task = self.get_task(task_id)
        if not task:
            return None
        
        self._check_owner(task, username)

        for key, value in data.model_dump().items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        cache_store.clear()
        return task
    
    def partial_update(self, task_id: int, data: TaskUpdate, username):
        task = self.get_task(task_id)
        if not task:
            return None
        self._check_owner(task, username)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        cache_store.clear()
        return task
    
    def delete_task(self, task_id: int, username):
        task = self.get_task(task_id)
        if not task:
            return False
        self._check_owner(task, username)

        self.db.delete(task)
        self.db.commit()
        cache_store.clear()
        return task

