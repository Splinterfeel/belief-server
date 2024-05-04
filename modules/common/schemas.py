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


class UserResourcesDTO(BaseModel):
    user_id: int
    gold: int
    materials: int
    food: int
    population: int

    class Config:
        from_attributes = True
