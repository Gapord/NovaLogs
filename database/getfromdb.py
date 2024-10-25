# ЭТО ВРЕМЕННО
import disnake

async def getchan(servid):
    chans = {
        1168078062278160404: 1168620321348255754
    }
    return chans.get(servid, None)

async def getcolor(servid):
    colors = {
        1168078062278160404: disnake.Color.orange()
    }

    return colors.get(servid, disnake.Color.default())
