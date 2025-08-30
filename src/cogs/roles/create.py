import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class CreateRole(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: disnake.Role):
        guild_data = await self.bot.db.fetch_guild_data(role.guild.id)
        if guild_data is None:
            return

        log = self.bot.get_channel(guild_data.channel_id)

        async for entry in role.guild.audit_logs(
            action=disnake.AuditLogAction.role_create, limit=1
        ):
            creator = entry.user
            break
        else:
            creator = None

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Создание роли", color=guild_data.color)
        embed.add_field(name="Роль", value=f"{role.name} (ID: {role.id})")
        embed.add_field(
            name="Создано пользователем",
            value=creator.mention if creator else "Неизвестен",
        )
        embed.add_field(name="Время создания", value=current_time)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CreateRole(bot))
