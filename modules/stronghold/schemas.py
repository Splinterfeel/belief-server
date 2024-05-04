from pydantic import BaseModel
import datetime


class BuildingTypeDTO(BaseModel):
    id: int
    name: str
    icon_name: str
    description: str | None = None
    max_level: int

    class Config:
        from_attributes = True


class BuildingDTO(BaseModel):
    id: int
    stronghold_id: int
    building_type_id: int | None
    cell: int
    level: int | None
    building_type: BuildingTypeDTO | None

    class Config:
        from_attributes = True


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
