from datetime import timezone, datetime

from sqlalchemy import Column, String
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./rejuvenAI.db"  # "postgresql://user:password@postgresserver/db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Users:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = mapped_column(Integer, primary_key=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # {"password_hash": "<password-hash>"}
    updated_on = Column(DateTime, nullable=True)
    created_on = Column(DateTime, default=datetime.now(tz=timezone.utc))
    is_deleted = Column(Boolean, default=False)


# Database Configurations
declarative_base().metadata.create_all(bind=engine)
