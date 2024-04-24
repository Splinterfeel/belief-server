import datetime
from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str


class AuthUser(BaseModel):
    id: int
    login: str
    created: datetime.date
    cookie: str

    class Config:
        from_attributes = True


class AuthResult(BaseModel):
    "Reponse for auth request"
    successful: bool
    user: AuthUser | None = None
