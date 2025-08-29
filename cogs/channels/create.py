import datetime

import disnake
from disnake.ext import commands

from database.getfromdb import getchan, getcolor


class CreateChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: disnake.abc.GuildChannel):
        guild = channel.guild
        log = self.bot.get_channel(await getchan(guild.id))

        async for entry in guild.audit_logs(
            action=disnake.AuditLogAction.channel_create, limit=1
        ):
            creator = entry.user
            break
        else:
            creator = None

        channel_type = (
            "Категория"
            if isinstance(channel, disnake.CategoryChannel)
            else (
                "Текстовый канал"
                if isinstance(channel, disnake.TextChannel)
                else (
                    "Голосовой канал"
                    if isinstance(channel, disnake.VoiceChannel)
                    else "Канал"
                )
            )
        )

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Создание канала", color=await getcolor(guild.id))
        embed.add_field(name="Тип канала", value=channel_type)
        embed.add_field(name="Имя канала", value=channel.name)
        embed.add_field(name="Канал", value=f"<#{channel.id}>")
        embed.add_field(
            name="Ответственный",
            value=creator.mention if creator else "Неизвестен",
        )
        embed.add_field(name="Время создания", value=current_time)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CreateChannel(bot))
