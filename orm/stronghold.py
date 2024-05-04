import datetime
from typing import List
from sqlalchemy import BigInteger, CheckConstraint, String, Date, UniqueConstraint, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm import Base, common, region


class Stronghold(Base):
    __tablename__ = 'stronghold'
    __table_args__ = {'schema': 'stronghold'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    chunk_id: Mapped[int] = mapped_column(ForeignKey('region.chunk.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('common.user.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    created: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=func.now())
    user: Mapped["common.User"] = relationship('orm.common.User', back_populates='strongholds')
    x_coordinate: Mapped[int] = mapped_column(BigInteger, nullable=False)
    y_coordinate: Mapped[int] = mapped_column(BigInteger, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False, server_default='1')
    chunk: Mapped["region.Chunk"] = relationship('orm.region.Chunk', back_populates='strongholds')
    buildings: Mapped[List["Building"]] = relationship(back_populates='stronghold')


class BuildingType(Base):
    __tablename__ = 'building_type'
    __table_args__ = {'schema': 'stronghold'}
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    icon_name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False, server_default='5')
    buildings: Mapped["Building"] = relationship(back_populates='building_type')
    building_prices: Mapped[List["BuildingPrice"]] = relationship(back_populates='building_type')


class Building(Base):
    __tablename__ = 'building'
    __table_args__ = (
        CheckConstraint('cell between 0 and 24', name='building_stronghold_cell_0_to_24'),
        UniqueConstraint('stronghold_id', 'cell', name='uq_building_stronghold_cell'),
        {'schema': 'stronghold'}
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    stronghold_id: Mapped[int] = mapped_column(ForeignKey('stronghold.stronghold.id'), nullable=False)
    building_type_id: Mapped[int] = mapped_column(ForeignKey('stronghold.building_type.id'), nullable=True)
    cell: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=True, server_default='1')
    building_type: Mapped["BuildingType"] = relationship(back_populates='buildings')
    stronghold: Mapped["Stronghold"] = relationship(back_populates='buildings')


class BuildingPrice(Base):
    __tablename__ = 'building_price'
    __table_args__ = (
        CheckConstraint('level > 0', name='building_price_level_gt_0'),
        UniqueConstraint('building_type_id', 'level', name='uq_building_type_id_level'),
        {'schema': 'stronghold'}
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    building_type_id: Mapped[int] = mapped_column(ForeignKey('stronghold.building_type.id'))
    level: Mapped[int] = mapped_column(Integer, nullable=False, server_default='1')
    materials: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    food: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    population: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    time: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default='1')
    building_type: Mapped["BuildingType"] = relationship(back_populates='building_prices')
