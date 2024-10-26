from database.mysql.base import DatabaseConnection


class GetServerData:
    def __init__(self, serverid: str):
        self.servid = serverid
        self.db_connection = DatabaseConnection()

    async def fetch_server_data(self):
        db = await self.db_connection.connect()
        async with db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT serverid, color, channel, date FROM servers WHERE serverid = %s
            """,
                (self.servid,),
            )
            row = await cursor.fetchone()

        if row:
            return {
                "serverid": row[0],
                "color": row[1],
                "channel": row[2],
                "date": row[3],
            }
        return None
