from enum import Enum


# TODO читать динамически из БД
class StructureTypeID(Enum):
    MINE = 1
    FARMLANDS = 2
    SETTLEMENT = 3
    GOLDEN_MINE = 4
