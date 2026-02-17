from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "aqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, echo = True)

SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit = False)