from pydantic import BaseModel
import datetime


class StrongholdDTO(BaseModel):
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
