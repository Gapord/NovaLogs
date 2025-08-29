import json

import disnake
from disnake.ext import commands

import config as c
from database.getfromdb import getchan

bot = commands.Bot(
    command_prefix=c.pref,
    help_command=None,
    intents=disnake.Intents.all(),
    reload=True,
    activity=disnake.Game(c.game),
)


@bot.event
async def on_ready():
    print(f"{bot.user.name} готов к работе")


with open("cogs_url.json", "r") as json_file:
    cogs_data = json.load(json_file)

for url in cogs_data["cogs"]:
    bot.load_extension(url)


bot.run(c.token)
