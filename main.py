from email.headerregistry import Address
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello Django Developer"}

# @app.get("/about")
# def about():
#     return {"name": "shahbaz", "role": "python Developer"}

# @app.get("/skills")
# def skills():
#     return {"skills": ["python", "Django", "FastAPI"]}

# @app.get("/hello/{name}")
# def hello(name:str):
#     return "Hello"+" "+ name

# @app.get("/user/{id}")
# def get_user(id:int):
#     return {"user_id": "id"}

# @app.get("/add_number/{num}")
# def add_number(num:int):
#     return 5 + num

# @app.get("/users/{user_id}/post/{post_id}")
# def get_post(user_id: int, post_id: int):
#     return{"user": user_id, "post":post_id}


# @app.get("/products")
# def list_products(limit: int = 10, skip: int = 0):
#     return {"limit": limit, "skip": skip}

# @app.get("/search")
# def search(q: str | None = None):
#     return{"query": q}

# # class User(BaseModel):
# #     name: str
# #     age: int

# # @app.post("/users")
# # def create_user(user: User):
# #     return user

# # @app.get("/users")
# # def get_user():
# #     user = User(name: str, age: int)
# #     return user

# class User(BaseModel):
#     name: str = Field(min_length=3, max_length=50)
#     age: int = Field(gt=0, lt=20)

# @app.post("/users")
# def create_user(user: User):
#     return user

# @app.post("/users/{user_id}")
# def update_user(user_id: int, user: User, admin: bool = False):
#     return {
#         "id": user_id,
#         "data": user,
#         "admin": admin
#     }

# @app.get("/square/{num}")
# def square(num: int):
#     return num*num


# @app.get("/items")
# def items(name: str, price:int):
#     return {
#         "name": name,
#         "price": price
#     }

# class UserRegister(BaseModel):
#     username: str = Field(min_length = 4)
#     password:str = Field(min_length = 8)
#     age:int = Field(gt = 18)

# @app.post("/register")
# def register(user_data: UserRegister):
#     return {
#         "user_data" : user_data
#     }

# def common_params():
#     return {"version": "1.0"}

# @app.get("/info")
# def info(data = Depends(common_params)):
#     return data


# def pagination(limit: int = 10):
#     return {"limit": limit}

# @app.get("/items")
# def items(p = Depends(pagination)):
#     return p


# def get_current_user(token: str | None = None):
#     if token != "secret":
#         return {"error": "Unauthrized"}
#     return {"username": "admin"}

# @app.get("/dashboard")
# def dashboard(user = Depends(get_current_user)):
#     return {"user": user}


# def get_db(db_username: str, db_password: str):
#     return f"db_connection with {db_username} {db_password}"

# def get_user(db = Depends(get_db)):
#     return f"user_from"

# @app.get("/")
# def home(user = Depends(get_user)):
#     return user 


# def logger():
#     return "request looged"

# @app.get("/test")
# def test(loggs = Depends(logger)):
#     return loggs


# def api_protect(api_key: str):
#     if api_key != "1234":
#         return "error"
#     else:
#         return "success"
    
# @app.get("/secure")
# def secure(msg = Depends(api_protect)):
#     return {"message": msg}

# def connect():
#     return "connect to db"

# @app.get("/users")
# def users(db = Depends(connect)):
#     return db

# def connect(db_username: str, db_password: str):
#     return f"connect to db with {db_username} {db_password}"

# @app.get("/users/{db_username}/{db_password}")
# def users(db_username, db_password, db = Depends(connect(db_username, db_password))):
#     return db

# from fastapi import FastAPI, Depends

# app = FastAPI()

# def connect(db_username: str, db_password: str):
#     return f"connect to db with {db_username} {db_password}"

# # @app.get("/users/{db_username}/{db_password}")
# # def users(db: str = Depends(connect)):
# #     return db
# @app.get("/users/{db_username}/{db_password}")
# def users(
#     db_username: str,
#     db_password: str,
#     db: str = Depends(connect)
# ):
#     return db


# #basic model
# class User(BaseModel):
#     username: str = Field(min_length = 4, max_length = 20)
#     age:int = Field(gt = 18, lt = 60)
#     email:str
#     bio: Optional[str] = None
#     is_staff: bool = False

# @app.post("/users")
# def create_user(user:User):
#     return user

# # Nested Model 
# class Address(BaseModel):
#     city: str
#     country: str
# class User(BaseModel):
#     username: str = Field(min_length = 4, max_length = 20)
#     age:int = Field(gt = 18, lt = 60)
#     email:str
#     bio: Optional[str] = None
#     is_staff: bool = False
#     address: Address

# @app.post("/users")
# def create_user(user:User):
#     return user


# class Item(BaseModel):
#     name: str 
#     price: float

# class Orders(BaseModel):
#     items: list[Item]

# @app.post("/orders")
# def orders(order: Orders):
#     return order


# class UserOut(BaseModel):
#     username:str
# class User(BaseModel):
#     username: str = Field(min_length=4, max_length=20)
#     age: int = Field(gt=18, lt=60)
#     email: str

# @app.post("/user", response_model= UserOut)
# def create_user(user: User):
#     return user


# class UserCreate(BaseModel):
#     username:str
#     password:str

# class UserResponse(BaseModel):
#     id:int = 2
#     username:str

# @app.post("/create_user", response_model= UserResponse)
# def create_user(user: UserCreate):
#     return user


# class User(BaseModel):
#     username: str

#     @field_validator("username")
#     def no_admin(cls, value):
#         if value == "admin":
#             raise ValueError("reserved username")
#         return value
    
# @app.post("/create_user")
# def create_user(user:User):
#     return user

# class Product(BaseModel):
#     name: str = Field(min_length=3)
#     price:int = Field(gt = 0)
#     discount: Optional[int] = None

# @app.post("/products")
# def products(p: Product):
#     return p


# class Profile(BaseModel):
#     age:int
#     city:str

# class User(BaseModel):
#     profile: Profile

# @app.post("/user_profile")
# def user_profile(u_p:User):
#     return {"user":u_p}


# class UserCreate(BaseModel):
#     username: str
#     password: str
#     email: str

# class UserResponse(BaseModel):
#     username:str
#     email:str

# @app.post("/create_user", response_model=UserResponse)
# def user_create(user: UserCreate):
#     return user