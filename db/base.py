from datetime import timezone, datetime

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True)
    is_deleted = Column(Boolean, default=False)
    updated_on = Column(DateTime, nullable=True)
    created_on = Column(DateTime, default=datetime.now(tz=timezone.utc))
