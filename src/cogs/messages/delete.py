import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class DeleteMSG(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        async for entry in message.guild.audit_logs(
            action=disnake.AuditLogAction.message_delete, limit=1
        ):
            if entry.target.id == message.author.id:
                deleter = entry.user
                break
        else:
            deleter = message.author

        guild_data = await self.bot.db.fetch_guild_data(message.guild.id)
        if guild_data is None:
            return
        
        log = self.bot.get_channel(guild_data.channel_id)

        embed = disnake.Embed(title="Удаление сообщения", color=guild_data.color)
        embed.add_field(name="Автор", value=message.author.mention)
        embed.add_field(name="Канал", value=message.channel.mention)
        embed.add_field(name="Сообщение", value=message.content, inline=False)
        embed.set_footer(text=f"Удалил {deleter}")

        if message.attachments:
            files = [
                await attachment.to_file()
                for attachment in message.attachments
            ]
            await log.send(embed=embed, files=files)
        else:
            await log.send(embed=embed)


def setup(bot: CustomClient):
    bot.add_cog(DeleteMSG(bot))
