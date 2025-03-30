from pydantic import BaseModel


class LoginRequestForm(BaseModel):
    username: str
    password: str
