from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from modules.common.routes import check_cookie
from modules.stronghold import main, schemas

router = APIRouter(prefix='/stronghold')


@router.get('/')
async def get_stronghold(
        authorized: Annotated[dict, Depends(check_cookie)],
        id: int):
    if not authorized:
        raise HTTPException(status_code=401, detail="Cookie not valid")
    return main.get_stronghold(id)


async def get_user_strongholds(user_id: int) -> list[schemas.StrongholdDTO]:
    return main.get_user_strongholds(user_id)
