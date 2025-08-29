import datetime

import disnake
from disnake.ext import commands

from database.getfromdb import getchan, getcolor


class LeaveMember(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        guild = member.guild
        log = self.bot.get_channel(await getchan(guild.id))

        reason = "Самовольно"
        async for entry in guild.audit_logs(limit=1):
            if entry.target.id == member.id:
                if entry.action == disnake.AuditLogAction.kick:
                    reason = "Кик"
                    break
                if entry.action == disnake.AuditLogAction.ban:
                    reason = "Бан"
                    break

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Выход с сервера", color=await getcolor(guild.id))
        embed.add_field(name="Пользователь", value=member.mention)
        embed.add_field(name="Причина выхода", value=reason)
        embed.add_field(name="Точное время", value=current_time, inline=False)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(LeaveMember(bot))
