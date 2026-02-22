from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models.user import User
from core.security import hash_password, veryfy_password, create_token
from sqlalchemy import select

class UserService:

    def __init__(self, db) -> None:
        self.db = db

    def register(self, data):
        user = User(username = data.username,
                    hashed_password = hash_password(data.password)
                )
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(400, "Username already exists")
    
    async def login(self, data):
        # user = self.db.query(User).filter(User.username == data.username).first()
        result = await self.db.execute(
            select(User).where(User.username == data.username)
        )
        user = result.scalar_one_or_none()

        if not user or not veryfy_password(data.password, user.hashed_password):
            return None
        
        token = create_token({"sub": user.username})
        return token
    

        