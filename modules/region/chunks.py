import random
from sqlalchemy import select, func, text
from orm import Session
from orm.region import Chunk
import orm.structure
from modules.structure.main import StructureTypeID
from itertools import cycle
from PIL import Image, ImageDraw
from modules.common import config
CHUNK_SIZE = 10


def create_structures_in_chunk(chunk: Chunk):
    "Сгенерировать структуры (поселения, шахты и т д) в чанке"
    structures = []
    used_coordinates = set()  # на момент начала генерации структур чанк должен быть пустой
    types_to_generate = [
        {'type': StructureTypeID.MINE.value, 'max_count': config.MAX_MINES_IN_CHUNK},
        {'type': StructureTypeID.FARMLANDS.value, 'max_count': config.MAX_FARMLANDS_IN_CHUNK},
        {'type': StructureTypeID.SETTLEMENT.value, 'max_count': config.MAX_SETTLEMENTS_IN_CHUNK},
        {'type': StructureTypeID.GOLDEN_MINE.value, 'max_count': config.MAX_GOLDMINES_IN_CHUNK},
    ]
    for structure_type in types_to_generate:
        for _ in range(structure_type['max_count']):
            generated = False
            while not generated:
                x_coordinate = random.randint(chunk.x_start, chunk.x_end)
                y_coordinate = random.randint(chunk.y_start, chunk.y_end)
                if (x_coordinate, y_coordinate,) in used_coordinates:
                    continue
                used_coordinates.add((x_coordinate, y_coordinate,))
                generated = True
            structure = orm.structure.Structure(
                chunk_id=chunk.id,
                structure_type_id=structure_type['type'],
                x_coordinate=x_coordinate, y_coordinate=y_coordinate
            )
            structures.append(structure)
    with Session() as session:
        session.add_all(structures)
        session.commit()


def init_chunks() -> None:
    "Проверить, если начального чанка нет - то создать его"
    with Session() as session:
        any_chunk_exists = session.query(Chunk).limit(1).one_or_none()
        if not any_chunk_exists:
            initial_chunk = Chunk(
                x_start=0, y_start=0, x_end=CHUNK_SIZE - 1, y_end=CHUNK_SIZE - 1)
            session.add(initial_chunk)
            session.flush()
            session.commit()
            session.refresh(initial_chunk)
    create_structures_in_chunk(initial_chunk)
    generate_new_chunks()
    print('created initial chunkset (3x3)')


def generate_new_chunks() -> None:
    "Расширить чанки во все стороны от существующих"
    with Session() as session:
        min_X = session.execute(select(func.min(Chunk.x_start))).scalar()
        min_Y = session.execute(select(func.min(Chunk.y_start))).scalar()
        max_X = session.execute(select(func.max(Chunk.x_end))).scalar()
        max_Y = session.execute(select(func.max(Chunk.y_end))).scalar()
        new_chunks = []
        # добавляем чанки сверху и снизу
        x_start = min_X - CHUNK_SIZE
        y_start = min_Y - CHUNK_SIZE
        while x_start < max_X + CHUNK_SIZE:
            chunk_1 = Chunk(
                x_start=x_start, y_start=y_start,
                x_end=x_start + CHUNK_SIZE - 1, y_end=y_start + CHUNK_SIZE - 1)
            chunk_2 = Chunk(
                x_start=x_start, y_start=max_Y + 1,
                x_end=x_start + CHUNK_SIZE - 1, y_end=max_Y + CHUNK_SIZE)
            new_chunks.extend([chunk_1, chunk_2])
            x_start += CHUNK_SIZE
        # добавляем чанки слева и справа
        x_start2 = min_X - CHUNK_SIZE
        y_start2 = min_Y
        while y_start2 < max_Y:
            chunk_1 = Chunk(
                x_start=x_start2, y_start=y_start2,
                x_end=x_start2 + CHUNK_SIZE - 1, y_end=y_start2 + CHUNK_SIZE - 1)
            chunk_2 = Chunk(
                x_start=max_X + 1, y_start=y_start2,
                x_end=max_X + CHUNK_SIZE, y_end=y_start2 + CHUNK_SIZE - 1)
            new_chunks.extend([chunk_1, chunk_2])
            y_start2 += CHUNK_SIZE

        session.add_all(new_chunks)
        session.flush()
        session.commit()
        for chunk in new_chunks:
            session.refresh(chunk)
            create_structures_in_chunk(chunk)


def create_chunks_image():
    colormap = (
        "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige",
        "bisque", "black", "blanchedalmond", "blue", "blueviolet", "brown",
        "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue",
        "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray",
        "darkgrey", "darkgreen", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange",
        "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey",
        "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey", "dodgerblue", "firebrick",
        "floralwhite", "forestgreen", "fuchsia", "gainsboro", "ghostwhite", "gold", "goldenrod", "gray", "grey",
        "green", "greenyellow", "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender",
        "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow",
        "lightgreen", "lightgray", "lightgrey", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue",
        "lightslategray", "lightslategrey", "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta",
        "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue",
        "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin",
        "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod",
        "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue",
        "purple", "rebeccapurple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen",
        "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray", "slategrey", "snow", "springgreen",
        "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke",
        "yellow", "yellowgreen")
    get_color = cycle(colormap)
    with Session() as session:
        x_offset = abs(session.execute(select(func.min(Chunk.x_start))).scalar())
        y_offset = abs(session.execute(select(func.min(Chunk.y_start))).scalar())
        max_X = session.execute(select(func.max(Chunk.x_end))).scalar()
        max_Y = session.execute(select(func.max(Chunk.y_end))).scalar()
        chunks = session.query(Chunk).all()
    width = max_X + x_offset
    height = max_Y + y_offset
    img = Image.new(mode="RGB", size=(width, height), color=(209, 123, 193))
    draw = ImageDraw.Draw(img)
    for chunk in chunks:
        draw.rectangle((
            (chunk.x_start+x_offset, chunk.y_start+y_offset),
            (chunk.x_end+x_offset, chunk.y_end+y_offset)), fill=next(get_color))
        draw.text((chunk.x_start+x_offset, chunk.y_start+y_offset), str(chunk.id))
    img.show()


def clear_all_gamedata():
    "Подготовка на случай запуска на пустой БД"
    with Session() as session:
        session.execute(text('delete from structure.structure;'))
        session.execute(text('delete from stronghold.building;'))
        session.execute(text('delete from stronghold.stronghold;'))
        session.execute(text('delete from common.resource_gain;'))
        session.execute(text('delete from common.resource;'))
        session.execute(text('delete from common.user;'))
        session.execute(text('delete from region.chunk;'))
        session.commit()
    init_chunks()


# clear_all_gamedata()
