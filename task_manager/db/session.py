from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./tasks.db"
DATABASE_URL = "postgresql://postgres:postgres123@localhost/taskdb"


engine = create_engine(DATABASE_URL, echo = True)

SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit = False)