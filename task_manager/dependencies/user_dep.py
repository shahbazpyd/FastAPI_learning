from fastapi import Depends
from dependencies.db_dep import get_db
from services.user_service import UserService

def get_user_service(db = Depends(get_db)):
    return UserService(db)