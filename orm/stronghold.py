import datetime
from sqlalchemy import BigInteger, String, Date, func, ForeignKey, Integer
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
