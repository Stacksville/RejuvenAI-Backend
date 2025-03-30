from enum import Enum

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, declared_attr

from config.db import Base


class FileStatus(str, Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"

    UPLOAD_FAILED = "upload_failed"
    PROCESSING_FAILED = "processing_failed"


class Users(Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # {"password_hash": "<password-hash>"}

    # Relationship to Child (one-to-many)
    files = relationship("Files", back_populates="user")


class Files(Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(String, nullable=True)
    type = Column(String, nullable=True)
    status = Column(String, default=FileStatus.UPLOADING)

    user_id = mapped_column(ForeignKey("users.id"))  # ForeignKey referencing Parent
    user = relationship("Users", back_populates="files")  # Relationship to Parent
