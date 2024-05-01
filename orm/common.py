import datetime
from sqlalchemy import BigInteger, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm import Base, stronghold


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'common'}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, unique=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=func.now())
    password: Mapped[str] = mapped_column(String(400))
    cookie: Mapped[str] = mapped_column(String(400), nullable=True)
    strongholds: Mapped["stronghold.Stronghold"] = relationship('orm.stronghold.Stronghold', back_populates='user')
    money: Mapped[int] = mapped_column(BigInteger, server_default='100', nullable=False)
