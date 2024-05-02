import random
from orm import Session
from orm.stronghold import Stronghold
from orm.region import Chunk
from orm.common import User
from modules.region.chunks import generate_new_chunks
from modules.common.config import MAX_STRONGHOLDS_PER_CHUNK


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
