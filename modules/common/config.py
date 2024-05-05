from orm import Session
from sqlalchemy import select
from orm.common import Config

MAX_STRONGHOLDS_PER_CHUNK = 2
CELLS_IN_STRONGHOLD = 25
MAX_FARMLANDS_IN_CHUNK = 2
MAX_GOLDMINES_IN_CHUNK = 1
MAX_MINES_IN_CHUNK = 2
MAX_SETTLEMENTS_IN_CHUNK = 2
RESOURCE_TICK_SECONDS = 60
MAX_FOOD = 1000
MAX_MATERIALS = 1000
MAX_POPULATION = 1000
MAX_GOLD = 1000


def init():
    global MAX_STRONGHOLDS_PER_CHUNK, CELLS_IN_STRONGHOLD, \
        MAX_FARMLANDS_IN_CHUNK, MAX_GOLDMINES_IN_CHUNK, \
        MAX_MINES_IN_CHUNK, MAX_SETTLEMENTS_IN_CHUNK, \
        RESOURCE_TICK_SECONDS, MAX_FOOD, MAX_MATERIALS, MAX_POPULATION, MAX_GOLD
    with Session() as session:
        params = session.execute(select(Config)).scalars().all()
        config = dict()
    for p in params:
        config[p.param] = p.value
    MAX_STRONGHOLDS_PER_CHUNK = int(config['MAX_STRONGHOLDS_PER_CHUNK'])
    CELLS_IN_STRONGHOLD = int(config['CELLS_IN_STRONGHOLD'])
    MAX_FARMLANDS_IN_CHUNK = int(config['MAX_FARMLANDS_IN_CHUNK'])
    MAX_GOLDMINES_IN_CHUNK = int(config['MAX_GOLDMINES_IN_CHUNK'])
    MAX_MINES_IN_CHUNK = int(config['MAX_MINES_IN_CHUNK'])
    MAX_SETTLEMENTS_IN_CHUNK = int(config['MAX_SETTLEMENTS_IN_CHUNK'])
    RESOURCE_TICK_SECONDS = int(config['RESOURCE_TICK_SECONDS'])
    MAX_FOOD = int(config['MAX_FOOD'])
    MAX_MATERIALS = int(config['MAX_MATERIALS'])
    MAX_POPULATION = int(config['MAX_POPULATION'])
    MAX_GOLD = int(config['MAX_GOLD'])
