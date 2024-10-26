import aiosqlite

class GetServerData:
    def __init__(self, servid):
        self.servid = servid
        self.db_path = f"database/sqlite/bases/servers.db"

    async def fetch_server_data(self):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT serverid, color, channel, date FROM servers WHERE serverid = ?
            """, (self.servid,))
            row = await cursor.fetchone()
            await cursor.close()

        if row:
            return {
                "serverid": row[0],
                "color": row[1],
                "channel": row[2],
                "date": row[3]
            }
        return None
