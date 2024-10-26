# ЭТО ВРЕМЕННО
from database.sqlite.getserv import GetServerData
import disnake

async def getchan(servid):
    server_data = await GetServerData(servid).fetch_server_data()
    return server_data["channel"] if server_data else None

async def getcolor(servid):
    server_data = await GetServerData(servid).fetch_server_data()
    if server_data:
        color_name = server_data["color"]
        # Словарь соответствия названий цветов и объектов disnake.Color
        colors = {
            "blue": disnake.Color.blue(),
            "red": disnake.Color.red(),
            "green": disnake.Color.green(),
            "yellow": disnake.Color.yellow(),
            "orange": disnake.Color.orange(),
            "purple": disnake.Color.purple(),
            "black": disnake.Color.from_rgb(0, 0, 0),  # Black
            "white": disnake.Color.from_rgb(255, 255, 255)  # White
        }
        return colors.get(color_name, disnake.Color.default())
    
    return disnake.Color.default()
