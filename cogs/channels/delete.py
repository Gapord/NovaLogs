import disnake
from disnake.ext import commands
import datetime
from database.getfromdb import getchan, getcolor


class DeleteChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: disnake.abc.GuildChannel):
        guild = channel.guild
        log = self.bot.get_channel(await getchan(guild.id))

        async for entry in guild.audit_logs(
            action=disnake.AuditLogAction.channel_delete, limit=1
        ):
            deleter = entry.user
            break
        else:
            deleter = None

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

        embed = disnake.Embed(
            title="Удаление канала", color=await getcolor(guild.id)
        )
        embed.add_field(name="Тип канала", value=channel_type)
        embed.add_field(
            name="Имя канала", value=f"{channel.name} (ID: {channel.id})"
        )
        embed.add_field(
            name="Ответственный",
            value=deleter.mention if deleter else "Неизвестен",
        )
        embed.add_field(name="Время удаления", value=current_time)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DeleteChannel(bot))
