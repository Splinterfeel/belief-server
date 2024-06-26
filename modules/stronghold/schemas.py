from pydantic import BaseModel, Field
import datetime


class BuildingPriceQuery(BaseModel):
    "Ззапрос цены на постройку / улучшение здания"
    building_type_id: int
    level: int


class BuildingPriceDTO(BaseModel):
    "Ответ цены на постройку / улучшение здания"
    building_type_id: int
    level: int
    materials: int
    food: int
    population: int
    gold: int
    time: int  # в минутах


class BuildingTypeDTO(BaseModel):
    id: int
    name: str
    icon_name: str
    description: str | None = None
    max_level: int

    class Config:
        from_attributes = True


class BuildingQueueDTO(BaseModel):
    user_id: int
    stronghold_id: int
    building_type_id: int
    cell: int
    level: int | None
    is_upgrade: bool
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    scheduled_at: datetime.datetime | None = None
    building_type: BuildingTypeDTO | None = None


class BuildingDTO(BaseModel):
    id: int
    stronghold_id: int
    building_type_id: int | None
    cell: int
    level: int | None
    building_type: BuildingTypeDTO | None = None
    queued_task: BuildingQueueDTO | None = None

    class Config:
        from_attributes = True


class BuildingQueueResult(BaseModel):
    'Ответ на запрос добавления постройки в очередь'
    successful: bool
    description: str = None


class StrongholdDTO(BaseModel):
    "Базовая модель для возврата инфы по крепости"
    id: int
    chunk_id: int
    user_id: int
    name: str
    created: datetime.date
    x_coordinate: int
    y_coordinate: int
    level: int

    class Config:
        from_attributes = True


class StrongholdFullDTO(StrongholdDTO):
    "Подробная модель для возврата инфы по крепости"
    buildings: list[BuildingDTO]

    class Config:
        from_attributes = True
