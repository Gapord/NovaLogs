import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class JoinMember(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild_data = await self.bot.db.fetch_guild_data(member.guild.id)
        if guild_data is None:
            return
        
        log = self.bot.get_channel(guild_data.channel_id)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(
            title="Вход на сервер", color=guild_data.color
        )
        embed.add_field(name="Пользователь", value=member.mention)
        embed.add_field(name="Точное время", value=current_time)

        await log.send(embed=embed)


def setup(bot: CustomClient):
    bot.add_cog(JoinMember(bot))
