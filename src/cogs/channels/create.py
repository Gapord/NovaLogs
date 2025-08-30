import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class CreateChannel(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: disnake.abc.GuildChannel):
        guild_data = await self.bot.db.fetch_guild_data(channel.guild.id)
        if guild_data is None:
            return
        
        log = self.bot.get_channel(guild_data.channel_id)

        async for entry in channel.guild.audit_logs(
            action=disnake.AuditLogAction.channel_create, limit=1
        ):
            creator = entry.user
            break
        else:
            creator = None

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Создание канала", color=guild_data.color)
        embed.add_field(name="Тип канала", value=channel.type.name)
        embed.add_field(name="Имя канала", value=channel.name)
        embed.add_field(name="Канал", value=f"<#{channel.id}>")
        embed.add_field(
            name="Ответственный",
            value=creator.mention if creator else "Неизвестен",
        )
        embed.add_field(name="Время создания", value=current_time)

        await log.send(embed=embed)


def setup(bot: CustomClient):
    bot.add_cog(CreateChannel(bot))
