import datetime

import disnake
from disnake.ext import commands

from database.getfromdb import getchan, getcolor


class UpdateEmoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(
        self,
        guild: disnake.Guild,
        before: list[disnake.Emoji],
        after: list[disnake.Emoji],
    ):
        log = self.bot.get_channel(await getchan(guild.id))

        updated_emojis = [
            emoji
            for emoji in after
            if emoji in before and emoji.name != before[before.index(emoji)].name
        ]

        for emoji in updated_emojis:
            async for entry in guild.audit_logs(
                action=disnake.AuditLogAction.emoji_update, limit=1
            ):
                updater = entry.user
                break
            else:
                updater = None

            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")

            embed = disnake.Embed(
                title="Обновление эмодзи", color=await getcolor(guild.id)
            )
            old_emoji = before[before.index(emoji)]
            embed.add_field(name="Эмодзи", value=f"{old_emoji} (ID: {old_emoji.id})")
            embed.add_field(name="Новое имя", value=f"`{emoji.name}`")
            embed.add_field(
                name="Обновлено пользователем",
                value=updater.mention if updater else "Неизвестен",
            )
            embed.add_field(name="Время обновления", value=current_time)

            await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(UpdateEmoji(bot))
