from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from modules.common.routes import check_cookie

router = APIRouter(prefix='/stronghold')


@router.get('/')
async def get_stronghold(
        authorized: Annotated[dict, Depends(check_cookie)],
        id: int):
    if not authorized:
        raise HTTPException(status_code=401, detail="Cookie not valid")
    return 'ok'
