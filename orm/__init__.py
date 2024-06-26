import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


__all__ = ['Session', 'Base', 'queue']


class Base(DeclarativeBase):
    ...


sa_url = os.getenv('BELIEF_ORM_URL')
engine = create_engine(sa_url, echo=False)
Session = sessionmaker(engine)
