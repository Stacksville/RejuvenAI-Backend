import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./my_sqlite.db"  # "postgresql://user:password@postgresserver/db"
from db.base import Base

# Connect args for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
Base = declarative_base(cls=Base)
