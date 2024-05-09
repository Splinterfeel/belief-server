import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class TaskTable(str, Enum):
    BUILDING = 'building'


class TaskType(int, Enum):
    BUILD_A_BUILDING = 1


class QueuedTask(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    id: int
    table: TaskTable  # табилца в схеме queue, в которой хранится задача
    task_type: TaskType  # тип задачи для определения функции-исполнителя
    created_at: datetime.datetime
    scheduled_at: datetime.datetime
    done: bool  # исполнена ли задача
    queued: bool  # была ли задача отправлена в очередь
    delay: int = 0  # задержка между вычиткой из БД и получением из mq


class BuildingTaskDTO(QueuedTask):
    model_config = ConfigDict(use_enum_values=True)
    stronghold_id: int
    building_type_id: int
    cell: int
    level: int
    upgrade: bool  # является ли задание апгрейдом здания
