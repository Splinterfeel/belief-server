import datetime
from typing import List
from sqlalchemy import BigInteger, String, Date, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm import Base, stronghold


class Resource(Base):
    __tablename__ = 'resource'
    __table_args__ = {'schema': 'common'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('common.user.id'), unique=True, nullable=False)
    gold: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='100')
    materials: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='1000')
    food: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='1000')
    population: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='1000')
    user: Mapped["User"] = relationship(back_populates='resource')


class ResourceGain(Base):
    __tablename__ = 'resource_gain'
    __table_args__ = {'schema': 'common'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('common.user.id'), unique=True, nullable=False)
    gold: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='10')
    materials: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='50')
    food: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='50')
    population: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='50')
    user: Mapped["User"] = relationship(back_populates='resource_gain')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'common'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=func.now())
    password: Mapped[str] = mapped_column(String(400))
    cookie: Mapped[str] = mapped_column(String(400), nullable=True)
    strongholds: Mapped[List["stronghold.Stronghold"]] = relationship('orm.stronghold.Stronghold', back_populates='user')
    resource: Mapped["Resource"] = relationship(back_populates='user')
    resource_gain: Mapped["ResourceGain"] = relationship(back_populates='user')


class Config(Base):
    __tablename__ = 'config'
    __table_args__ = {'schema': 'common'}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    param: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(500), nullable=False)
