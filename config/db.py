from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from db.base import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./rejuvenAI.db"  # "postgresql://user:password@postgresserver/db"

# Connect args for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
Base = declarative_base(cls=BaseModel)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
