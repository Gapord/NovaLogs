import io

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class DeleteMSG(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        deleter = message.author
        async for entry in message.guild.audit_logs(
            action=disnake.AuditLogAction.message_delete, limit=5
        ):
            if entry.target.id == message.author.id:
                time_diff = (message.created_at - entry.created_at).total_seconds()
                if abs(time_diff) < 5:
                    deleter = entry.user
                    break

        guild_data = await self.bot.db.fetch_guild_data(message.guild.id)
        if not guild_data:
            return

        log = self.bot.get_channel(guild_data.channel_id)

        embed = disnake.Embed(title="Удаление сообщения", color=guild_data.color)
        embed.add_field(name="Автор", value=message.author.mention)
        embed.add_field(name="Канал", value=message.channel.mention)
        embed.set_footer(text=f"Удалил {deleter}")

        files = (
            [await attachment.to_file() for attachment in message.attachments]
            if message.attachments
            else []
        )

        if len(message.content) > 500:
            txt_file = disnake.File(
                fp=io.StringIO(message.content), filename=f"message_{message.id}.txt"
            )
            files.append(txt_file)
            await log.send(embed=embed, files=files)
        else:
            if message.content != "":
                embed.add_field(
                    name="Сообщение", value=f"```{message.content}```", inline=False
                )
            await log.send(embed=embed, files=files if files else None)


def setup(bot: CustomClient):
    bot.add_cog(DeleteMSG(bot))
