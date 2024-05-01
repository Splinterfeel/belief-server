from sqlalchemy import select, func
from orm import Session
from orm.region import Chunk


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
init_chunks()
# generate_new_chunks()
