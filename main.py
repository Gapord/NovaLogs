import json

import disnake
from disnake.ext import commands

import config as c
from src.classes.custom_client import CustomClient

bot = CustomClient()


@bot.event
async def on_ready():
    await bot.db.create_tables()

    print(f"{bot.user.name} готов к работе")


@bot.event
async def on_slash_command_error(
    interaction: disnake.ApplicationCommandInteraction, error: commands.CommandError
):
    match type(error):
        case commands.BadColourArgument:
            await interaction.send("Неверный ввод цвета!", ephemeral=True)
        case commands.MissingPermissions:
            await interaction.send(
                "У вас нет прав для выполнения данной команды!", ephemeral=True
            )
        case _:
            pass


with open("cogs_url.json", "r") as json_file:
    cogs_data = json.load(json_file)

for url in cogs_data["cogs"]:
    bot.load_extension(url)

bot.run(c.token)
