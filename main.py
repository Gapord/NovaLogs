import json

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient
import config as c

bot = CustomClient()

@bot.event
async def on_ready():
    await bot.db.create_tables()

    print(f"{bot.user.name} готов к работе")

@bot.event
async def on_slash_command_error(
    interaction: disnake.ApplicationCommandInteraction, 
    error: commands.CommandError
    ):
    match type(error):
        case commands.BadColourArgument:
                interaction.send("Неверный ввод цвета!", ephemeral=True)
        case commands.MissingPermissions:
            interaction.send("У вас нет прав для выполнения данной команды!", ephemeral=True)

with open("cogs_url.json", "r") as json_file:
    cogs_data = json.load(json_file)

for url in cogs_data["cogs"]:
    bot.load_extension(url)

bot.run(c.token)

