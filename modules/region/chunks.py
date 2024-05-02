from sqlalchemy import select, func
from orm import Session
from orm.region import Chunk
from itertools import cycle
from PIL import Image, ImageDraw

CHUNK_SIZE = 10


def init_chunks():
    "Проверить, если начального чанка нет - то создать его"
    with Session() as session:
        any_chunk_exists = session.query(Chunk).limit(1).one_or_none()
        if not any_chunk_exists:
            initial_chunk = Chunk(
                x_start=0, y_start=0, x_end=CHUNK_SIZE - 1, y_end=CHUNK_SIZE - 1)
            session.add(initial_chunk)
            session.flush()
            session.commit()
            print('created initial chunk')


def generate_new_chunks():
    "Расширить чанки во все стороны от существующих"
    with Session() as session:
        min_X = session.execute(select(func.min(Chunk.x_start))).scalar()
        print(f"{min_X=}")
        min_Y = session.execute(select(func.min(Chunk.y_start))).scalar()
        print(f"{min_Y=}")
        max_X = session.execute(select(func.max(Chunk.x_end))).scalar()
        print(f"{max_X=}")
        max_Y = session.execute(select(func.max(Chunk.y_end))).scalar()
        print(f"{max_Y=}")
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

        for chunk in new_chunks:
            print(chunk)
        print(len(new_chunks))
        session.add_all(new_chunks)
        session.flush()
        session.commit()


# подготовка на случай запуска на пустой БД
# init_chunks()
# generate_new_chunks()
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


# init_chunks()
# generate_new_chunks()
# create_chunks_image()
