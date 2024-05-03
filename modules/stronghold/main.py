import random
from orm import Session
from orm.stronghold import Stronghold
from orm.region import Chunk
from orm.common import User
from modules.region.chunks import generate_new_chunks
from modules.common.config import MAX_STRONGHOLDS_PER_CHUNK
from modules.stronghold import schemas, buildings


def get_stronghold(stronghold_id: int) -> schemas.StrongholdFullDTO:
    "Получить подробную инфу по крепости. Сюда позднее добавить всю инфу о постройках внутри нее"
    with Session() as session:
        stronghold_orm = session.query(Stronghold).where(Stronghold.id == stronghold_id).one()
    stronghold = schemas.StrongholdFullDTO.model_validate(stronghold_orm)
    # test data
    stronghold.buildings = [
        None, None, None, None, buildings.BuildingType.RESIDENCE,
        None, buildings.BuildingType.CASTLE, None, buildings.BuildingType.BARRACKS, None,
        None, None, None, buildings.BuildingType.SHOOTING_RANGE, None,
        None, buildings.BuildingType.CHURCH, None, None, None,
        None, None, None, None, None,
    ]
    return stronghold


def get_user_strongholds(user_id: str) -> list[schemas.StrongholdDTO]:
    "Получить список крепостей пользователя"
    with Session() as session:
        strongholds = session.query(Stronghold).where(Stronghold.user_id == user_id).all()
    return [schemas.StrongholdDTO.model_validate(x) for x in strongholds]


def create_initial_user_stronghold(user: User) -> None:
    "Создать новую крепость при регистрации игрока"
    with Session() as session:
        free_chunk = session.query(Chunk).where(Chunk.full.is_not(True)).limit(1).one_or_none()
        if not free_chunk:
            generate_new_chunks()
            free_chunk = session.query(Chunk).where(Chunk.full.is_not(True)).limit(1).one_or_none()
        has_position = False
        while not has_position:
            position_x = (random.randint(free_chunk.x_start, free_chunk.x_end))
            position_y = (random.randint(free_chunk.y_start, free_chunk.y_end))
            position_busy = session.query(
                Stronghold).where(
                    Stronghold.x_coordinate.in_((position_x, position_x + 1, position_x - 1))).where(
                        Stronghold.y_coordinate.in_((position_y, position_y + 1, position_y - 1))).one_or_none()
            if not position_busy:
                has_position = True
        # generate stronghold
        stronghold = Stronghold(
            chunk_id=free_chunk.id, user_id=user.id,
            name='Крепость ' + user.login,
            x_coordinate=position_x,
            y_coordinate=position_y)
        session.add(stronghold)
        session.flush()
        session.commit()
        # close chunk for new strongholds if it is full now
        count_in_chunk = session.query(Stronghold).where(Stronghold.chunk_id == free_chunk.id).count()
        if count_in_chunk >= MAX_STRONGHOLDS_PER_CHUNK:
            free_chunk.full = True
            session.flush()
            session.commit()
