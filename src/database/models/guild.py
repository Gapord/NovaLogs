from sqlalchemy import Column, Integer, DateTime

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Guild(Base):
    __tablename__ = 'guilds'
    
    guild_id = Column(Integer, primary_key=True)
    color = Column(Integer)
    channel_id = Column(Integer)
    date = Column(DateTime)