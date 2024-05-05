import datetime
from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, UniqueConstraint, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from orm import Base


class BuildingQueue(Base):
    "Таблица запущенных задач по строительству"
    __tablename__ = 'building'
    __table_args__ = (
        CheckConstraint('cell between 0 and 24', name='buildingqueue_stronghold_cell_0_to_24'),
        UniqueConstraint('stronghold_id', 'cell', name='uq_buildingqueue_stronghold_cell'),
        {'schema': 'queued'}
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    stronghold_id: Mapped[int] = mapped_column(ForeignKey('stronghold.stronghold.id'), nullable=False)
    building_type_id: Mapped[int] = mapped_column(ForeignKey('stronghold.building_type.id'), nullable=True)
    cell: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=True, server_default='1')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    scheduled_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    queued: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
