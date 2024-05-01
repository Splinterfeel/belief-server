from typing import Annotated
from fastapi import APIRouter, Response, Cookie
from modules.common import schemas, users

router = APIRouter(prefix='/common')


async def check_cookie(user_cookie: Annotated[str | None, Cookie()] = None):
    return users.check_cookie(user_cookie)


@router.post('/auth')
async def auth(user: schemas.User, response: Response) -> schemas.AuthResult:
    result: schemas.AuthResult = users.auth_user(user)
    if result.successful:
        response.set_cookie(key="user_cookie", value=result.user.cookie)
    return result


@router.post('/user')
async def add_user(user: schemas.User) -> bool:
    return users.add_user(user)
