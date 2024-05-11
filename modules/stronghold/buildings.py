import datetime
from enum import Enum
from modules.stronghold import schemas
from sqlalchemy import text
from modules.stronghold.schemas import BuildingQueueDTO, BuildingQueueResult, BuildingTypeDTO
from orm import Session
from orm.common import Resource
from orm.stronghold import BuildingPrice, Stronghold, Building, BuildingType as BuildingTypeORM
from orm.queued import BuildingQueue
from mq.schemas import BuildingTaskDTO


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


def build(building: BuildingTaskDTO) -> None:
    "Построить здание по заданию из очереди"
    with Session() as session:
        query = session.query(Building).where(
                Building.stronghold_id == building.stronghold_id,
                Building.cell == building.cell)
        if building.upgrade:
            # апгрейд здания
            query = query.where(Building.building_type_id == building.building_type_id)
        existing_building = query.one()
        existing_building.building_type_id = building.building_type_id
        existing_building.level = building.level
        session.add(existing_building)
        session.execute(text(
            'UPDATE queued.building SET done = true WHERE id = :id'),
            {'id': building.id})
        session.commit()


def queue_building(building: BuildingQueueDTO) -> BuildingQueueResult:
    "Создать задание на постройку здания"
    with Session() as session:
        # check if stronghold belongs to player
        stronghold_belongs_to_player = session.query(Stronghold).where(
            Stronghold.id == building.stronghold_id).where(Stronghold.user_id == building.user_id).one_or_none()
        if not stronghold_belongs_to_player:
            return BuildingQueueResult(successful=False, description='Крепость не принадлежит пользователю')
        # check if cell available to build or upgrade this building type
        cell_in_stronghold = session.query(Building).where(
            Building.stronghold_id == building.stronghold_id).where(
                Building.cell == building.cell).one()
        if cell_in_stronghold.building_type_id:
            if not building.is_upgrade:
                return BuildingQueueResult(successful=False, description='Ячейка занята, нельзя построить новое здание')
            if cell_in_stronghold.building_type_id != building.building_type_id:
                return BuildingQueueResult(successful=False, description='Ячейка занята зданеим другого типа')
            if cell_in_stronghold.level <= building.level + 1:
                return BuildingQueueResult(
                    successful=False, description='Попытка построить здание выше на несколько уровней (>1)')
        cell_in_building_queue = session.query(BuildingQueue).where(
            BuildingQueue.stronghold_id == building.stronghold_id).where(
                BuildingQueue.cell == building.cell).one_or_none()
        if cell_in_building_queue:
            return BuildingQueueResult(successful=False, description='Ячейка уже задействована в очереди строительства')
        # get building price
        price = session.query(BuildingPrice).where(
            BuildingPrice.building_type_id == building.building_type_id).where(
                BuildingPrice.level == building.level).one()
        # check uf player has enough resources
        user_resources = session.query(Resource).where(Resource.user_id == building.user_id).one()
        if (
             (user_resources.food < price.food) or (user_resources.materials < price.materials) or
             (user_resources.gold < price.gold) or (user_resources.population < price.population)):
            return BuildingQueueResult(successful=False, description='Недостаточно ресурсов')
        # decrease player resources
        user_resources.food -= price.food
        user_resources.gold -= price.gold
        user_resources.materials -= price.materials
        user_resources.population -= price.population
        session.add(user_resources)
        time_to_build = price.time * 60  # minutes in DB -> seconds
        building.scheduled_at = building.created_at + datetime.timedelta(seconds=time_to_build)
        # add to BuildingQueue table
        building_queue = BuildingQueue(
            stronghold_id=building.stronghold_id,
            building_type_id=building.building_type_id,
            cell=building.cell,
            level=building.level,
            created_at=building.created_at,
            scheduled_at=building.scheduled_at, done=False)
        session.add(building_queue)
        session.commit()
    return BuildingQueueResult(successful=True)


def get_building_price(query: schemas.BuildingPriceQuery) -> schemas.BuildingPriceDTO:
    "Получить данные о стоимости постройки или улучшения здания"
    with Session() as session:
        return session.query(BuildingPrice).where(
            BuildingPrice.building_type_id == query.building_type_id,
            BuildingPrice.level == query.level).one()


def get_building_types() -> list[BuildingTypeDTO]:
    global BUILDING_TYPES
    if 'BUILDING_TYPES' not in globals():
        with Session() as session:
            BUILDING_TYPES = [BuildingTypeDTO.model_validate(t) for t in session.query(BuildingTypeORM).all()]
    return BUILDING_TYPES
