from fastapi import Depends, FastAPI
from routes.task_routes import router as task_router
from db.base import Base
from db.session import engine
from core.security import get_current_user
from routes.auth_routes import router as auth_router
import asyncio
from db.session import engine
from db.base import Base

# Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Task Manager API")

# @app.on_event("startup")
# async def startup():
#     print("@app.on_event")
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(task_router)
app.include_router(auth_router)


@app.get("/profile", tags = ["Auth"])
def profile(user = Depends(get_current_user)):
    return {"user": user}



