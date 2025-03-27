# https://docs.chainlit.io/data-layers/sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declared_attr

from db.base import Base


class User(Base):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {"mysql_engine": "InnoDB"}

    identifier = Column(String, nullable=False, unique=True)
    metadata = Column(String, nullable=False)  # {"password_hash": "<password-hash>"}
    createdAt = Column(String, nullable=True)  # Duplicate of created_on
