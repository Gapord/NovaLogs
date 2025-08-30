from sqlalchemy import Column, DateTime, Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Guild(Base):
    __tablename__ = "guilds"

    guild_id = Column(BigInteger, primary_key=True)
    color = Column(Integer)
    channel_id = Column(BigInteger)
    date = Column(DateTime)
