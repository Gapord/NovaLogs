import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient
import config as c

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
            choices=list(c.colors.keys()),
            description="Выберите цвет для сервера",
        ),
    ):
            colour = c.colors[color]

            await self.bot.db.configure_guild(guild_id=interaction.guild.id, color=colour.value, channel_id=channel.id)

            embed = disnake.Embed(
                title="Настройки сервера обновлены", color=colour
            )
            embed.add_field(name="Канал логов", value=channel.mention)
            embed.add_field(name="Цвет эмбедов", value=color)

            await interaction.send(embed=embed)


def setup(bot: CustomClient):
    bot.add_cog(BotSettings(bot))
