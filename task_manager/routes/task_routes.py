from fastapi import APIRouter, Depends, HTTPException
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from services.task_service import TaskService
from dependencies.task_dep import get_task_services
from core.security import get_current_user
from fastapi import BackgroundTasks

from utils.logger import log_task_creation


router = APIRouter(prefix = "/tasks", tags = ["Tasks"])

@router.post("", response_model= TaskResponse)
def create_task(
    data: TaskCreate,
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user),
    service: TaskService = Depends(get_task_services)
):
    task = service.create_task(data, user)

    background_tasks.add_task(
        log_task_creation,
        task.title,
        user
    )

    return task



@router.get("")
def get_tasks(limit: int = 5, skip: int = 0, service: TaskService = Depends(get_task_services)):
    return service.get_tasks(limit=limit, skip = skip)


@router.get("/{task_id}")
def get_task(task_id:int, service:TaskService = Depends(get_task_services)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.put("/{task_id}")
def update_task(task_id: int, data: TaskUpdate, user = Depends(get_current_user), service: TaskService = Depends(get_task_services)):
    task = service.update(task_id, data, user)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, user = Depends(get_current_user), service: TaskService = Depends(get_task_services)):
    success = service.delete_task(task_id, user)
    if not success:
        raise HTTPException(404, "Task not found")
    return {"message": "Delete successfully"}


@router.patch("/{task_id}")
def partial_update(task_id:int, data: TaskUpdate, user = Depends(get_current_user), service: TaskService = Depends(get_task_services)):
    task = service.partial_update(task_id, data, user)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

    


   