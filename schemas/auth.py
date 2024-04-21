from pydantic import BaseModel


class LoginResult(BaseModel):
    successful: bool
    login: str | None = None
