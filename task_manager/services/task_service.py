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

    async def _check_owner(self, task, username):
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user or task.user_id != user.id:
            raise HTTPException(403, "Not authorized")

    async def create_task(self, data: TaskCreate, username):
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        task = Task(title = data.title,
                    description = data.description,
                    user_id = user.id
                    )
        
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        cache_store.clear()
        return task
    
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


    async def get_task(self, task_id:int):
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
      
    async def update(self, task_id: int, data:TaskUpdate, username):
        task = await self.get_task(task_id)
        if not task:
            return None
        
        await self._check_owner(task, username)

        for key, value in data.model_dump().items():
            setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        cache_store.clear()
        return task
    
    async def partial_update(self, task_id: int, data: TaskUpdate, username):
        task = await self.get_task(task_id)
        if not task:
            return None
        await self._check_owner(task, username)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        cache_store.clear()
        return task
    
    async def delete_task(self, task_id: int, username):
        task = await self.get_task(task_id)
        if not task:
            return False
        await self._check_owner(task, username)

        await self.db.delete(task)
        await self.db.commit()
        cache_store.clear()
        return task
