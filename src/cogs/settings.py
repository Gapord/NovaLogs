import disnake
from disnake.ext import commands

import config as c
from src.classes.custom_client import CustomClient


class BotSettings(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.slash_command(description="Настройка сервера")
    @commands.has_permissions(administrator=True)
    async def setting(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel,
        color: str = commands.Param(
            autocomplete=True,
            description="Выберите цвет для сервера или укажите свой в формате HEX (#000000)",
        ),
    ):
        colour = c.colors.get(color)

        if colour is None:
            try:
                colour = int(color.lstrip("#"), 16)
            except ValueError:
                await interaction.send("Неверно введен цвет!", ephemeral=True)
                return
            color_value = colour
        else:
            color_value = colour.value

        await self.bot.db.configure_guild(
            guild_id=interaction.guild.id, color=color_value, channel_id=channel.id
        )

        embed = disnake.Embed(title="Настройки сервера обновлены", color=color_value)
        embed.add_field(name="Канал логов", value=channel.mention)
        embed.add_field(name="Цвет эмбедов", value=color)

        await interaction.send(embed=embed)

    @setting.autocomplete("color")
    async def color_autocomplete(
        self, inter: disnake.ApplicationCommandInteraction, user_input: str
    ):
        return [
            disnake.OptionChoice(name=color_name, value=color_name)
            for color_name in c.colors.keys()
            if user_input.lower() in color_name.lower()
        ]


def setup(bot: CustomClient):
    bot.add_cog(BotSettings(bot))
