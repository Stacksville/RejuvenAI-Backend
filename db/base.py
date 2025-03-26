import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True)
    is_deleted = Column(Boolean, default=False)
    updated_on = Column(DateTime, nullable=True)
    created_on = Column(DateTime, default=datetime.datetime.now(tz=datetime.UTC))
