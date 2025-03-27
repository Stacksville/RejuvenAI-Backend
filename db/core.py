from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base import Base


class Files(Base):
    __tablename__ = "files"

    user = relationship("User")
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)


class Agents(Base):
    __tablename__ = "agents"

    user = relationship("User")
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    instructions = Column(String, nullable=True)
