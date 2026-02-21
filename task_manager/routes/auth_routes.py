from multiprocessing.resource_tracker import ResourceTracker
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, UserLogin, UserResponse
from dependencies.user_dep import get_user_service

router = APIRouter(prefix="/auth", tags = ["Auth"])
@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, service = Depends(get_user_service)):
    return service.register(data)

@router.post("/login")
def login(data:UserLogin, service = Depends(get_user_service)):
    token = service.login(data)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}