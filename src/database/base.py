from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import config as c
from src.database.mysql.base import MySQLDatabase
from src.database.sqlite.base import SQLiteDatabase
from src.database.models.guild import Guild

class Database:
    def __init__(self):
        if c.dbstatus == "mysql":
             self._db = MySQLDatabase()
        else:
             self._db = SQLiteDatabase()

        self.engine = self._db.engine
        self._async_sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_tables(self):
     async with self.engine.begin() as conn:
         await conn.run_sync(Guild.metadata.create_all)

    def session(self) -> AsyncSession:
        return self._async_sessionmaker()

    async def fetch_guild_data(self, guild_id) -> Optional[Guild]:
        async with self.session() as session:
            result = await session.execute(
                select(Guild).where(Guild.guild_id == guild_id)
            )

            return result.scalar_one_or_none()
    
    async def configure_guild(self, guild_id: int, color: int, channel_id: int):
        async with self.session() as session:
            result = await session.execute(
                select(Guild).where(Guild.guild_id == guild_id)
            )
            server = result.scalar_one_or_none()
            
            if server:
                await session.execute(
                    update(Guild)
                    .where(Guild.guild_id == guild_id)
                    .values(color=color, channel_id=channel_id, date=datetime.now())
                )
            else:
                new_server = Guild(
                    guild_id=guild_id,
                    color=color,
                    channel_id=channel_id,
                    date=datetime.now()
                )
                session.add(new_server)

            await session.commit()
