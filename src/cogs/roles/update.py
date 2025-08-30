import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient

class UpdateRole(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_update(
        self, before: disnake.Role, after: disnake.Role
    ):
        guild_data = await self.bot.db.fetch_guild_data(after.guild.id)
        if guild_data is None:
            return
        
        log = self.bot.get_channel(guild_data.channel_id)

        async for entry in after.guild.audit_logs(
            action=disnake.AuditLogAction.role_update, limit=1
        ):
            updater = entry.user
            break
        else:
            updater = None

        changes = []

        if before.name != after.name:
            changes.append(f"Имя изменено с `{before.name}` на `{after.name}`")

        if before.color != after.color:
            changes.append(
                f"Цвет изменён с `{before.color}` на `{after.color}`"
            )

        if before.hoist != after.hoist:
            changes.append(
                f"Поднятие роли изменено на `{'Включено' if after.hoist else 'Выключено'}`"
            )

        if before.mentionable != after.mentionable:
            changes.append(
                f"Упоминание роли изменено на `{'Включено' if after.mentionable else 'Выключено'}`"
            )

        if before.permissions != after.permissions:
            changes.append("Права роли изменены.")

        if not changes:
            return

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(
            title="Обновление роли", color=guild_data.color
        )
        embed.add_field(name="Роль", value=f"{after.name} (ID: {after.id})")
        embed.add_field(
            name="Изменения", value="\n".join(changes), inline=False
        )
        embed.add_field(
            name="Обновлено пользователем",
            value=updater.mention if updater else "Неизвестен",
        )
        embed.add_field(name="Время обновления", value=current_time)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(UpdateRole(bot))
