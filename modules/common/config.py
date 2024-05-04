from orm import Session
from sqlalchemy import select
from orm.common import Config

MAX_STRONGHOLDS_PER_CHUNK = 2
CELLS_IN_STRONGHOLD = 25


def init():
    global MAX_STRONGHOLDS_PER_CHUNK, CELLS_IN_STRONGHOLD
    with Session() as session:
        params = session.execute(select(Config)).scalars().all()
        config = dict()
    for p in params:
        config[p.param] = p.value
    MAX_STRONGHOLDS_PER_CHUNK = int(config['MAX_STRONGHOLDS_PER_CHUNK'])
    CELLS_IN_STRONGHOLD = int(config['CELLS_IN_STRONGHOLD'])
