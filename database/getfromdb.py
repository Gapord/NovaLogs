import disnake

import config as c
from database.mysql.getserv import GetServerData as GetServerDataMySQL
from database.sqlite.getserv import GetServerData as GetServerDataSQLite


async def getchan(servid):
    if c.DBSTATUS == 1:
        server_data = await GetServerDataSQLite(servid).fetch_server_data()
    elif c.DBSTATUS == 2:
        server_data = await GetServerDataMySQL(servid).fetch_server_data()
    else:
        return None

    return server_data["channel"] if server_data else None


async def getcolor(servid):
    if c.DBSTATUS == 1:
        server_data = await GetServerDataSQLite(servid).fetch_server_data()
    elif c.DBSTATUS == 2:
        server_data = await GetServerDataMySQL(servid).fetch_server_data()
    else:
        return disnake.Color.default()

    if server_data:
        color_name = server_data["color"]
        colors = {
            "blue": disnake.Color.blue(),
            "red": disnake.Color.red(),
            "green": disnake.Color.green(),
            "yellow": disnake.Color.yellow(),
            "orange": disnake.Color.orange(),
            "purple": disnake.Color.purple(),
            "black": disnake.Color.from_rgb(0, 0, 0),
            "white": disnake.Color.from_rgb(255, 255, 255),
        }
        return colors.get(color_name, disnake.Color.default())

    return disnake.Color.default()
