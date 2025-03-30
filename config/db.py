from datetime import timezone, datetime

# Connect args for SQLite
from sqlalchemy import Column
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column, declared_attr
from sqlalchemy.orm import sessionmaker

# https://docs.chainlit.io/data-layers/sqlalchemy

# Connect args for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./rejuvenAI.db"  # "postgresql://user:password@postgresserver/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel(object):
    # Abstract Model
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {"mysql_engine": "InnoDB"}

    id = mapped_column(Integer, primary_key=True, unique=True)
    is_deleted = Column(Boolean, default=False)
    updated_on = Column(DateTime, nullable=True)
    created_on = Column(DateTime, default=datetime.now(tz=timezone.utc))


Base = declarative_base(cls=BaseModel)


# Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
