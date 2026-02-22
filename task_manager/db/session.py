from venv import create
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./tasks.db"
# DATABASE_URL = "postgresql://postgres:postgres123@localhost/taskdb"

engine = create_async_engine(settings.DATABASE_URL, echo = True)

SessionLocal = async_sessionmaker(bind = engine, expire_on_commit=False)

# engine = create_engine(DATABASE_URL, echo = True)

# SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit = False)