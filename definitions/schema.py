from dataclasses import dataclass, asdict


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
