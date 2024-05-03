from enum import Enum


class BuildingType(Enum):
    # TODO формировать динамически из таблицы типов строений
    CASTLE = 'castle'
    BARRACKS = 'barracks'
    RESIDENCE = 'residence'  # дает прирост золота
    SHOOTING_RANGE = 'shooting_range'
    CHURCH = 'church'
    FARM = 'farm'  # дает прирост еды
    WAREHOUSE = 'warehouse'  # дает прирост сырья
    HOSPITAL = 'hospital'  # дает прирост населения
