from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from modules.common.routes import check_cookie
from modules.stronghold import main, schemas, buildings

router = APIRouter(prefix='/strongholds', tags=['Strongholds'])


@router.get('/', description='Получить подробную инфу по крепости')
async def get_stronghold(
        authorized: Annotated[dict, Depends(check_cookie)],
        id: int) -> schemas.StrongholdFullDTO:
    if not authorized:
        raise HTTPException(status_code=401, detail="Cookie not valid")
    return main.get_stronghold(id)


@router.post('/building', tags=['Buildings'], description='Добавить задание на постройку здания в очредь')
async def quque_building(building: schemas.BuildingQueueDTO) -> schemas.BuildingQueueResult:
    return buildings.queue_building(building)


@router.get('/building_types', tags=['Buildings'], description='Получить список типов зданий')
async def get_building_types() -> list[schemas.BuildingTypeDTO]:
    return buildings.get_building_types()


@router.get('/user', tags=['Strongholds', 'Users'], description='Получить список крепостей ползователя')
async def get_user_strongholds(user_id: int) -> list[schemas.StrongholdDTO]:
    return main.get_user_strongholds(user_id)
