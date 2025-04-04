from datetime import timezone, datetime

from sqlalchemy import Column, String
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker


class Users:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = mapped_column(Integer, primary_key=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # stores hashed password
    updated_on = Column(DateTime, nullable=True)
    created_on = Column(DateTime, default=datetime.now(tz=timezone.utc))
    is_deleted = Column(Boolean, default=False)


LOCALHOST_DATABASE_URL = "postgresql://chainlit_user:yourpassword@localhost:5432/chainlit_db"
# DATABASE_URL = os.getenv("DATABASE_URL", default=LOCALHOST_DATABASE_URL)
DATABASE_URL = "sqlite:///./chainlit_db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
Base.metadata.create_all(bind=engine)
