from dataclasses import dataclass, asdict
from pydantic import BaseModel


@dataclass
class Base:
    """
    This class is the parent dataclass for all schema classes.
    It is used to provide the dict() method to all of the child dataclasses
    """

    def dict(self):
        return asdict(self)


@dataclass
class User(Base):
    username: str


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Request Schema >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class LoginRequestSchema(BaseModel):
    username: str
    password: str

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Response Schema >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
