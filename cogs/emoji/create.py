import datetime

import disnake
from disnake.ext import commands

from database.getfromdb import getchan, getcolor


class CreateEmoji(commands.Cog):
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

            embed = disnake.Embed(
                title="Создание эмодзи", color=await getcolor(guild.id)
            )
            embed.add_field(name="Эмодзи", value=f"{emoji} (ID: {emoji.id})")
            embed.add_field(
                name="Создано пользователем",
                value=creator.mention if creator else "Неизвестен",
            )
            embed.add_field(name="Время создания", value=current_time)

            await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CreateEmoji(bot))
