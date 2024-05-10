from fastapi import APIRouter, Response, Request
from modules.common import schemas, users

router = APIRouter(prefix='/common', tags=['Users'])


async def check_cookie(req: Request):
    token = req.headers["Authorization"]
    print(token)
    return users.check_cookie(token)


@router.post('/auth', description='Авторизация пользователя', tags=['Users'])
async def auth(user: schemas.User, response: Response) -> schemas.AuthResult:
    result: schemas.AuthResult = users.auth_user(user)
    if result.successful:
        response.set_cookie(key="user_cookie", value=result.user.cookie)
    return result


@router.get('/resources/', description='Получить количество ресурсов у игрока', tags=['Users'])
async def get_user_resources(user_id: int) -> schemas.UserResourcesDTO:
    return users.get_user_resources(user_id)


@router.post('/user', description='Регистрация пользователя', tags=['Users'])
async def add_user(user: schemas.User) -> bool:
    return users.add_user(user)
