
from enum import auto
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt, JWTError
from jose import JWTError, ExpiredSignatureError



pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def veryfy_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


SECRET_KEY = "secret"
ALGORITHM = "HS256"
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours = 1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        print("payload:", payload)
        return payload["sub"]
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expires")
    
    except JWTError:
        raise HTTPException(status_code=401, detail = "Invalid token")