from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm import Base, stronghold
from typing import List


class Chunk(Base):
    __tablename__ = 'chunk'
    __table_args__ = {'schema': 'region'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    x_start: Mapped[int] = mapped_column(BigInteger, nullable=False)
    y_start: Mapped[int] = mapped_column(BigInteger, nullable=False)
    x_end: Mapped[int] = mapped_column(BigInteger, nullable=False)
    y_end: Mapped[int] = mapped_column(BigInteger, nullable=False)
    full: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    strongholds: Mapped[List["stronghold.Stronghold"]] = relationship('orm.stronghold.Stronghold', back_populates='chunk')

    def __repr__(self) -> str:
        return f"Chunk {self.x_start}:{self.y_start} -  {self.x_end}:{self.y_end}"
