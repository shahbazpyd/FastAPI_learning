from asyncio import Task
from os import name
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Tasks(BaseModel):
    name: str = Field(min_length=3)
    discriptions:str = Field(min_length=3)
    date:str 


@app.post("/tasks")
def create_tasks(task:Tasks):
    new_task:Tasks = Tasks(task.name, task.discriptions, task.date)


@app.get("/tasks")
def show_tasks():
    return Tasks


@app.get("/tasks/{id}")
def show_tasks_id(id:int):
    for task in Tasks:

