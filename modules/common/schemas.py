from pydantic import BaseModel


class AddUser(BaseModel):
    login: str
    password: str


class LoginResult(BaseModel):
    successful: bool
    login: str | None = None
