from fastapi import APIRouter, Depends, HTTPException
from schemas.task import TaskCreate, TaskUpdate
from services.task_service import TaskService
from dependencies.task_dep import get_task_services

router = APIRouter(prefix = "/tasks", tags = ["Tasks"])

@router.post("")
def create_task(data: TaskCreate, service: TaskService = Depends(get_task_services)):
    return service.create_task(data)

@router.get("")
def get_tasks(service: TaskService = Depends(get_task_services)):
    return service.get_tasks()


@router.get("/{task_id}")
def get_task(task_id:int, service:TaskService = Depends(get_task_services)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.put("/{task_id}")
def update_task(task_id: int, data: TaskUpdate, service: TaskService = Depends(get_task_services)):
    task = service.update(task_id, data)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_services)):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(404, "Task not found")
    return {"message": "Delete successfully"}


   