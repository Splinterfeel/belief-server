from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm import Base, region
from typing import List


class StructureType(Base):
    __tablename__ = 'structure_type'
    __table_args__ = {'schema': 'structure'}
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    icon_name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    structures: Mapped[List["Structure"]] = relationship(back_populates='structure_type')


class Structure(Base):
    __tablename__ = 'structure'
    __table_args__ = {'schema': 'structure'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chunk_id: Mapped[int] = mapped_column(ForeignKey('region.chunk.id'), nullable=False)
    structure_type_id: Mapped[int] = mapped_column(ForeignKey('structure.structure_type.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('common.user.id'), nullable=True)
    structure_type: Mapped["StructureType"] = relationship(back_populates='structures')
    x_coordinate: Mapped[int] = mapped_column(BigInteger, nullable=False)
    y_coordinate: Mapped[int] = mapped_column(BigInteger, nullable=False)
    chunk: Mapped["region.Chunk"] = relationship('orm.region.Chunk', back_populates='structures')
