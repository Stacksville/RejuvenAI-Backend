# https://docs.chainlit.io/data-layers/sqlalchemy


from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, declared_attr

from db.base import BaseModel
from db.model_const import FileStatus


class Users(BaseModel):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {"mysql_engine": "InnoDB"}

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # {"password_hash": "<password-hash>"}


class Files(BaseModel):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __tablename__ = "files"

    user = relationship("Users")

    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=True)
    type = Column(String, nullable=True)
    status = Column(String, default=FileStatus.UPLOADING)
