import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class DeleteChannel(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: disnake.abc.GuildChannel):
        guild_data = await self.bot.db.fetch_guild_data(channel.guild.id)
        if guild_data is None:
            return

        log = self.bot.get_channel(guild_data.channel_id)

        async for entry in channel.guild.audit_logs(
            action=disnake.AuditLogAction.channel_delete, limit=1
        ):
            deleter = entry.user
            break
        else:
            deleter = None

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Удаление канала", color=guild_data.color)
        embed.add_field(name="Тип канала", value=channel.type.name)
        embed.add_field(name="Имя канала", value=f"{channel.name} (ID: {channel.id})")
        embed.add_field(
            name="Ответственный",
            value=deleter.mention if deleter else "Неизвестен",
        )
        embed.add_field(name="Время удаления", value=current_time)

        await log.send(embed=embed)


def setup(bot: CustomClient):
    bot.add_cog(DeleteChannel(bot))
