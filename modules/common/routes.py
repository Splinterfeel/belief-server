from fastapi import APIRouter
from modules.common import schemas, users

router = APIRouter(prefix='/common')


@router.post('/auth')
async def auth(user: schemas.User) -> schemas.AuthResult:
    return users.auth_user(user)


@router.post('/user')
async def add_user(user: schemas.User) -> bool:
    return users.add_user(user)
