import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class LeaveMember(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        guild_data = await self.bot.db.fetch_guild_data(member.guild.id)
        if guild_data is None:
            return

        log = self.bot.get_channel(guild_data.channel_id)

        reason = "Самовольно"
        async for entry in member.guild.audit_logs(limit=1):
            if entry.target.id == member.id:
                if entry.action == disnake.AuditLogAction.kick:
                    reason = "Кик"
                    break
                elif entry.action == disnake.AuditLogAction.ban:
                    reason = "Бан"
                    break

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Выход с сервера", color=guild_data.color)
        embed.add_field(name="Пользователь", value=member.mention)
        embed.add_field(name="Причина выхода", value=reason)
        embed.add_field(name="Точное время", value=current_time, inline=False)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(LeaveMember(bot))
