from pydantic import BaseModel
import datetime


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
    buildings: list = []
