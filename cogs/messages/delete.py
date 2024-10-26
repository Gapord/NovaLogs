import disnake
from disnake.ext import commands
from database.getfromdb import getcolor, getchan


class DeleteMSG(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(
            action=disnake.AuditLogAction.message_delete, limit=1
        ):
            if entry.target.id == message.author.id:
                deleter = entry.user
                break
        else:
            deleter = message.author

        guild_id = message.guild.id
        log_channel_id = await getchan(guild_id)
        log = self.bot.get_channel(log_channel_id)

        embed = disnake.Embed(
            title="Удаление сообщения", color=await getcolor(message.guild.id)
        )
        embed.add_field(name="Автор", value=message.author.mention)
        embed.add_field(name="Канал", value=f"<#{message.channel.id}>")
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


def setup(bot):
    bot.add_cog(DeleteMSG(bot))
