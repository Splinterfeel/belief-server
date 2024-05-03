from enum import Enum


class BuildingType(Enum):
    # TODO формировать динамически из таблицы типов строений
    CASTLE = 'castle'
    BARRACKS = 'barracks'
    RESIDENCE = 'residence'
    SHOOTING_RANGE = 'shooting_range'
    CHURCH = 'church'
