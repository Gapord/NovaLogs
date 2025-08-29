from datetime import datetime

from database.mysql.base import DatabaseConnection


class InitDB:
    def __init__(self, serverid: str):
        self.db_connection = DatabaseConnection()
        self.servid = serverid

    async def initdb(self, color: str, channel: int):
        db = await self.db_connection.connect()
        async with db.cursor() as cursor:
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS servers (
                    serverid BIGINT PRIMARY KEY,
                    color VARCHAR(255),
                    channel BIGINT,
                    date DATETIME
                )
            """
            )

            await cursor.execute(
                """
                UPDATE servers
                SET color = %s, channel = %s, date = %s
                WHERE serverid = %s
            """,
                (color, channel, datetime.now(), self.servid),
            )

            await cursor.execute(
                """
                INSERT INTO servers (serverid, color, channel, date)
                SELECT %s, %s, %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM servers WHERE serverid = %s)
            """,
                (self.servid, color, channel, datetime.now(), self.servid),
            )

        await db.commit()
        db.close()
