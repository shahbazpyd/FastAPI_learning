from fastapi import FastAPI
from routes.task_routes import router as task_router
from db.base import Base
from db.session import engine

Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Task Manager API")

app.include_router(task_router)