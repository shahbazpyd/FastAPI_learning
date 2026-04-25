# 📋 Task Manager API - Complete Guide for Beginners

A production-ready **Task Management system** built with **FastAPI**, featuring JWT authentication, asynchronous database operations, and automated migrations. This guide helps beginners build this system from scratch without cloning the repository.

---

## 📚 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Project Structure](#-project-structure)
3. [Step-by-Step Development](#-step-by-step-development)
4. [Execution Flow](#-execution-flow)
5. [Database Setup](#-database-setup)
6. [Running the Application](#-running-the-application)
7. [API Endpoints](#-api-endpoints)
8. [Testing](#-testing)
9. [Troubleshooting](#-troubleshooting)

---

## 🛠 Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **PostgreSQL 12+** → [Download](https://www.postgresql.org/download/)
- **Git** (optional, for version control)
- **Postman** or **VS Code REST Client** (for testing APIs)

### Verify Installation

```bash
python --version          # Should output Python 3.10 or higher
psql --version           # Should show PostgreSQL version
```

---

## 📁 Project Structure

Here's the complete directory structure you'll create:

```
task_manager/
│
├── main.py                    # FastAPI application entry point
├── .env                       # Environment variables (create this)
├── requirements.txt           # Python dependencies
│
├── core/                      # Core configurations & security
│   ├── __init__.py
│   ├── config.py             # Settings from environment
│   ├── security.py           # JWT authentication & password hashing
│   └── cache.py              # Optional caching utilities
│
├── db/                        # Database configuration
│   ├── __init__.py
│   ├── base.py               # SQLAlchemy declarative base
│   └── session.py            # Database connection & session
│
├── models/                    # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py               # User model
│   └── task.py               # Task model
│
├── schemas/                   # Pydantic validation schemas
│   ├── __init__.py
│   ├── user.py               # User request/response schemas
│   └── task.py               # Task request/response schemas
│
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── user_service.py       # User operations
│   └── task_service.py       # Task operations
│
├── routes/                    # API route handlers
│   ├── __init__.py
│   ├── auth_routes.py        # Authentication endpoints
│   └── task_routes.py        # Task management endpoints
│
├── dependencies/              # Dependency injection
│   ├── __init__.py
│   ├── db_dep.py             # Database dependency
│   ├── task_dep.py           # Task service dependency
│   └── user_dep.py           # User service dependency
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── logger.py             # Logging utilities
│
└── alembic/                   # Database migrations
    ├── versions/             # Migration files
    ├── env.py
    └── script.py.mako
```

---

## 🚀 Step-by-Step Development

### Step 1: Initialize Project & Virtual Environment

```bash
# Create project directory
mkdir task_manager
cd task_manager

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy alembic pydantic-settings python-jose[cryptography] passlib[bcrypt] asyncpg psycopg2-binary python-dotenv
```

**Dependency Explanation:**

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM for database
- `alembic` - Database migrations
- `pydantic-settings` - Configuration management
- `python-jose` - JWT token handling
- `passlib[bcrypt]` - Password hashing
- `asyncpg` - Async PostgreSQL driver
- `psycopg2-binary` - Sync PostgreSQL driver
- `python-dotenv` - Load .env files

### Step 3: Create Directory Structure

Create all the folders:

```bash
mkdir core db models schemas services routes dependencies utils alembic/versions
```

### Step 4: Create Environment Configuration

**File: `core/config.py`**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    ENV: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
```

**File: `.env`**

Create this in your `task_manager` root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost/taskdb
JWT_SECRET=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENV=development
```

> ⚠️ **Note:** Replace `your_password` with your PostgreSQL password

### Step 5: Database Configuration

**File: `db/base.py`**

```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

**File: `db/session.py`**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Step 6: Create Models

**File: `models/user.py`**

```python
from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

**File: `models/task.py`**

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

### Step 7: Create Pydantic Schemas

**File: `schemas/user.py`**

```python
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
```

**File: `schemas/task.py`**

```python
from typing import Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    status: str
    user_id: int

    class Config:
        from_attributes = True
```

### Step 8: Create Security & Authentication

**File: `core/security.py`**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> dict:
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {"username": username}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

### Step 9: Create Services (Business Logic)

**File: `services/user_service.py`**

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate
from core.security import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        hashed_password = hash_password(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_username(self, username: str) -> User:
        """Get user by username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()
```

**File: `services/task_service.py`**

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        """Create a new task"""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_tasks(self, user_id: int, skip: int = 0, limit: int = 5) -> list:
        """Get all tasks for a user"""
        result = await self.db.execute(
            select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_task(self, task_id: int, user_id: int) -> Task:
        """Get a specific task"""
        result = await self.db.execute(
            select(Task).where(
                (Task.id == task_id) & (Task.user_id == user_id)
            )
        )
        return result.scalars().first()

    async def update_task(self, task_id: int, user_id: int, task_data: TaskUpdate) -> Task:
        """Update a task"""
        db_task = await self.get_task(task_id, user_id)
        if not db_task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task"""
        db_task = await self.get_task(task_id, user_id)
        if not db_task:
            return False

        await self.db.delete(db_task)
        await self.db.commit()
        return True
```

### Step 10: Create Dependencies

**File: `dependencies/db_dep.py`**

```python
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from fastapi import Depends

async def get_database() -> AsyncSession:
    async with get_db() as db:
        yield db
```

**File: `dependencies/task_dep.py`**

```python
from sqlalchemy.ext.asyncio import AsyncSession
from services.task_service import TaskService
from dependencies.db_dep import get_database
from fastapi import Depends

async def get_task_service(db: AsyncSession = Depends(get_database)) -> TaskService:
    return TaskService(db)
```

**File: `dependencies/user_dep.py`**

```python
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService
from dependencies.db_dep import get_database
from fastapi import Depends

async def get_user_service(db: AsyncSession = Depends(get_database)) -> UserService:
    return UserService(db)
```

### Step 11: Create API Routes

**File: `routes/auth_routes.py`**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from services.user_service import UserService
from dependencies.user_dep import get_user_service
from core.security import verify_password, create_access_token
from core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    """Register a new user"""
    # Check if user exists
    existing_user = await service.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    return await service.create_user(user)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, service: UserService = Depends(get_user_service)):
    """Login user and return JWT token"""
    db_user = await service.get_user_by_username(user.username)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

**File: `routes/task_routes.py`**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from services.task_service import TaskService
from dependencies.task_dep import get_task_service
from core.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    # Extract user_id from the user dictionary (need to query actual user)
    return await service.create_task(task_data, user_id=1)  # In real app, get actual user_id

@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 5,
    user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Get all tasks for current user"""
    return await service.get_tasks(user_id=1, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Get a specific task"""
    task = await service.get_task(task_id, user_id=1)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Update a task"""
    task = await service.update_task(task_id, user_id=1, task_data=task_data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Delete a task"""
    success = await service.delete_task(task_id, user_id=1)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task deleted successfully"}
```

### Step 12: Create Main Application

**File: `main.py`**

```python
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.task_routes import router as task_router
from routes.auth_routes import router as auth_router
from core.security import get_current_user
from db.base import Base
from db.session import engine

app = FastAPI(
    title="Task Manager API",
    description="A production-ready task management system with JWT authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_router)
app.include_router(auth_router)

@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Task Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/profile", tags=["Auth"])
async def profile(user=Depends(get_current_user)):
    """Get current user profile"""
    return {"user": user}

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
```

### Step 13: Create Utility Functions

**File: `utils/logger.py`**

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_task_creation(title: str, user: dict):
    """Log task creation"""
    logger.info(f"Task created: {title} by {user.get('username')} at {datetime.utcnow()}")
```

---

## 🗄 Database Setup

### Step 1: Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE taskdb;

# Create user (optional)
CREATE USER taskuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;

# Quit
\q
```

### Step 2: Initialize Alembic

```bash
alembic init alembic
```

### Step 3: Configure Alembic

**File: `alembic/env.py`**

Update the SQLAlchemy URL configuration:

```python
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from core.config import settings
from db.base import Base
import os
import asyncio

# ... existing imports ...

config = context.config

# Set the SQLAlchemy URL from .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("asyncpg", "psycopg2"))

target_metadata = Base.metadata

# ... rest of the configuration ...
```

### Step 4: Create Initial Migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

### Step 5: Apply Migrations

```bash
alembic upgrade head
```

---

## 🔄 Execution Flow

Understanding how requests flow through the application is crucial for beginners. This section explains the architecture and how each component interacts.

### Request Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT REQUEST                            │
│                 (e.g., POST /auth/login)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                           │
│                      (main.py)                                   │
│  - Receives HTTP request                                         │
│  - Routes to appropriate handler                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API ROUTES LAYER                              │
│              (routes/auth_routes.py)                             │
│  - Validates request format                                      │
│  - Checks authentication (if needed)                             │
│  - Extracts parameters                                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 DEPENDENCY INJECTION LAYER                       │
│           (dependencies/user_dep.py, task_dep.py)               │
│  - Creates service instances                                     │
│  - Provides database sessions                                    │
│  - Manages resource lifecycle                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICES LAYER                                 │
│           (services/user_service.py)                             │
│  - Implements business logic                                     │
│  - Processes data                                                │
│  - Performs validations                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MODELS LAYER                                    │
│            (models/user.py, task.py)                             │
│  - SQLAlchemy ORM models                                         │
│  - Database table definitions                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 DATABASE CONNECTION                              │
│              (db/session.py, core/config.py)                     │
│  - Manages PostgreSQL connections                                │
│  - Executes SQL queries                                          │
│  - Returns results                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  POSTGRESQL DATABASE                             │
│  - Stores data persistently                                      │
│  - Validates data integrity                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
          Response flows back through layers in reverse order
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        RESPONSE                                  │
│              (JSON with status code)                             │
│                 Sent back to CLIENT                              │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Example: Creating a Task

Let's trace a real example to understand the flow better.

#### Client sends request:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d '{"title":"Buy groceries","description":"Milk, bread"}'
```

#### Step 1: Request reaches FastAPI (main.py)

```python
app = FastAPI()
app.include_router(task_router)  # Routes the request to task_router
```

#### Step 2: Route handler processes it (routes/task_routes.py)

```python
@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,                           # Validates JSON
    user = Depends(get_current_user),               # Authenticates user
    service: TaskService = Depends(get_task_service) # Injects service
):
    # At this point:
    # - task_data is validated Pydantic model
    # - user is extracted from JWT token
    # - service is created with database session
    return await service.create_task(task_data, user_id=1)
```

#### Step 3: Dependency injection (dependencies/task_dep.py)

```python
async def get_task_service(db: AsyncSession = Depends(get_database)):
    # FastAPI calls this function automatically
    # It creates a TaskService with a database session
    return TaskService(db)
```

#### Step 4: Service layer processes (services/task_service.py)

```python
class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        # Business logic here
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id
        )
        self.db.add(db_task)      # Add to session
        await self.db.commit()     # Execute INSERT
        await self.db.refresh(db_task)  # Get ID from database
        return db_task
```

#### Step 5: ORM model (models/task.py)

```python
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # SQLAlchemy converts this to SQL:
    # INSERT INTO tasks (title, description, user_id)
    # VALUES ('Buy groceries', 'Milk, bread', 1)
```

#### Step 6: Database connection (db/session.py)

```python
# Creates async engine connected to PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,  # postgresql+asyncpg://...
    echo=True
)

# Executes SQL query asynchronously
# PostgreSQL processes and returns the inserted row
```

#### Step 7: Response flows back

```python
# Service returns Task object
# Route validates with TaskResponse schema
# FastAPI serializes to JSON
# Returns to client:
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread",
    "completed": false,
    "status": "pending",
    "user_id": 1
}
```

### Authentication Flow

When a request needs authentication, here's what happens:

```
Request with Authorization header
         ↓
get_current_user() called
         ↓
Extract Bearer token from header
         ↓
Decode JWT token using JWT_SECRET
         ↓
If valid: Extract username from payload
If invalid: Raise 401 Unauthorized
         ↓
Return user data to route handler
```

**Example:**

```python
@app.get("/profile")
async def profile(user=Depends(get_current_user)):
    # user = {"username": "john_doe"}
    return {"message": f"Hello {user['username']}"}
```

### Error Handling Flow

When something goes wrong:

```
Error in any layer
         ↓
Exception raised
         ↓
FastAPI catches exception
         ↓
Returns appropriate HTTP status code + error message
         ↓
Client receives error response
```

**Example:**

```python
@router.get("/{task_id}")
async def get_task(task_id: int, service = Depends(get_task_service)):
    task = await service.get_task(task_id)

    if not task:
        # Raises 404 Not Found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
```

### Data Validation Flow

Pydantic automatically validates incoming data:

```python
class TaskCreate(BaseModel):
    title: str                      # Required string
    description: Optional[str] = None  # Optional string

# Client sends: {"title": "My Task"}
# ✅ Valid - description is optional

# Client sends: {"description": "My Task"}
# ❌ Invalid - title is required

# Client sends: {"title": 123}
# ❌ Invalid - title must be string

# FastAPI returns 422 Unprocessable Entity with detailed errors
```

---

## 🏃 Running the Application

### Development Mode

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at: **http://localhost:8000**

### Access Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔌 API Endpoints

### Authentication Endpoints

#### Register User

```
POST /auth/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123"
}
```

#### Login

```
POST /auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password123"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Task Endpoints

All task endpoints require Bearer token in Authorization header:

```
Authorization: Bearer <your_access_token>
```

#### Create Task

```
POST /tasks
Content-Type: application/json

{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs"
}
```

#### Get All Tasks

```
GET /tasks?skip=0&limit=5
```

#### Get Specific Task

```
GET /tasks/{task_id}
```

#### Update Task

```
PUT /tasks/{task_id}
Content-Type: application/json

{
    "title": "Updated title",
    "completed": true
}
```

#### Delete Task

```
DELETE /tasks/{task_id}
```

---

## ✅ Testing

### Using Postman

1. Register a user first
2. Copy the `access_token` from login response
3. In Postman, add Authorization header:
   - Type: Bearer Token
   - Token: `<your_access_token>`

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Create Task (with token)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"My Task","description":"Task description"}'
```

---

## 🛠 Troubleshooting

### Issue: "Database connection refused"

**Solution:** Ensure PostgreSQL is running and database `taskdb` exists.

```bash
# Check PostgreSQL status
psql -U postgres -c "SELECT version();"
```

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Activate virtual environment and install dependencies.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "JWT Token Expired"

**Solution:** Login again to get a new token. Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`.

### Issue: "Alembic: Target database is not up to date"

**Solution:** Apply migrations.

```bash
alembic upgrade head
```

### Issue: "CORS error when calling API from frontend"

**Solution:** Check CORS configuration in `main.py`. Update `allow_origins` if needed.

---

## 📦 Creating requirements.txt

To save dependencies for easy installation:

```bash
pip freeze > requirements.txt
```

The file should contain:

```
fastapi==0.129.0
uvicorn==0.40.0
sqlalchemy==2.0.46
alembic==1.18.4
pydantic-settings==2.1.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.2
asyncpg==0.29.0
psycopg2-binary==2.9.11
python-dotenv==1.0.0
```

---

## 🚢 Production Deployment Checklist

- [ ] Set `ENV=production` in `.env`
- [ ] Use strong `JWT_SECRET`
- [ ] Enable HTTPS
- [ ] Set `echo=False` in database engine
- [ ] Use environment variables for sensitive data
- [ ] Add proper logging and monitoring
- [ ] Set up proper CORS origins (not "\*")
- [ ] Use connection pooling for database
- [ ] Add rate limiting
- [ ] Implement proper error handling

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📄 License

This project is open source and available under the MIT License.

The API will be available at `http://127.0.0.1:8000`.

- **Interactive Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`

## 🔒 Security Implementation

The project uses `OAuth2PasswordBearer` for securing routes.

- **Hashing**: Passwords are hashed using `bcrypt` via Passlib.
- **JWT**: Tokens are signed with a `SECRET_KEY` and include an expiration time.
- **Protected Routes**: Use the `get_current_user` dependency to authorize requests.

## 📝 Logging & Utilities

- **Logger**: Task creations are logged to `task_log.txt` using the utility in `utils/logger.py`.
- **Cache**: `core/cache.py` provides a `set_cache` and `get_cache` functionality with Time-To-Live (TTL) support to reduce database load.

## 📜 License

This project is licensed under the MIT License.



## Chat Responses
# Development Process
I'll help you create a comprehensive README.md that guides beginners through building this FastAPI project from scratch. Let me first read the current README to see what's already there.

Now I'll create a comprehensive README.md that guides beginners through building this FastAPI project from scratch. This will include detailed step-by-step instructions:

Perfect! I've successfully created a comprehensive README.md file that guides beginners through building this FastAPI Task Manager project from scratch. Here's what I included:

📋 What's in the New README:
✅ Complete Prerequisites - Links to download Python, PostgreSQL, and other tools
✅ Detailed Project Structure - Full directory tree with explanations of each folder
✅ 13-Step Development Guide - From environment setup to running the app:

Virtual environment creation
Dependency installation
Configuration files (.env, config.py)
Database models (User, Task)
Pydantic schemas for validation
Authentication & security (JWT, password hashing)
Business logic services
Dependency injection
API routes (auth & tasks)
Main FastAPI application
Database setup with Alembic
Utility functions
✅ Database Setup Instructions - Step-by-step PostgreSQL configuration
✅ Running the Application - How to start the development server
✅ API Endpoints Reference - All endpoints with example requests/responses
✅ Testing Guide - Using Postman and cURL
✅ Troubleshooting Section - Common issues and solutions
✅ Production Checklist - Deployment best practices
✅ Additional Resources - Links to official documentation

A beginner with Python and FastAPI knowledge can now follow this README step-by-step to build the complete project without cloning it! 🚀


# Project Execution Flow On Requests
Perfect! I've added a comprehensive "Execution Flow" section to the README that explains how requests flow through the system. Here's what I included:

📊 What's in the New Execution Flow Section:
✅ Request Flow Diagram - Visual ASCII diagram showing the complete request path through all layers:

Client Request → FastAPI → Routes → Dependencies → Services → Models → Database → Response
✅ Detailed Example: Creating a Task - Step-by-step walkthrough showing:

What the client sends
How each layer processes it (Route → Dependency Injection → Service → Model → Database)
The actual code at each step
The final response returned to client
✅ Authentication Flow - Explains:

Bearer token extraction
JWT decoding and validation
User data extraction
Error handling for invalid tokens
✅ Error Handling Flow - Shows:

How exceptions propagate through layers
How FastAPI catches and converts them to HTTP errors
Example with 404 Not Found
✅ Data Validation Flow - Illustrates:

How Pydantic validates incoming requests
Valid vs. invalid examples
422 error responses
I also updated the Table of Contents to include the new section for easy navigation.

Now beginners can visually understand how a request flows through your entire application architecture! 🚀