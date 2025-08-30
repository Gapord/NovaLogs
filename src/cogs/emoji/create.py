import datetime

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class CreateEmoji(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(
        self,
        guild: disnake.Guild,
        before: list[disnake.Emoji],
        after: list[disnake.Emoji],
    ):
        guild_data = await self.bot.db.fetch_guild_data(guild.id)
        if guild_data is None:
            return

        log = self.bot.get_channel(guild_data.channel_id)

        new_emojis = [emoji for emoji in after if emoji not in before]

        for emoji in new_emojis:
            async for entry in guild.audit_logs(
                action=disnake.AuditLogAction.emoji_create, limit=1
            ):
                creator = entry.user
                break
            else:
                creator = None

            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")

            embed = disnake.Embed(title="Создание эмодзи", color=guild_data.color)
            embed.add_field(name="Эмодзи", value=f"{emoji} (ID: {emoji.id})")
            embed.add_field(
                name="Создано пользователем",
                value=creator.mention if creator else "Неизвестен",
            )
            embed.add_field(name="Время создания", value=current_time)

            await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CreateEmoji(bot))
