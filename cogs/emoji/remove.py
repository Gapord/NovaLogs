import disnake
from disnake.ext import commands
import datetime
from database.getfromdb import getchan, getcolor

class RemoveEmoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: disnake.Guild, before: list[disnake.Emoji], after: list[disnake.Emoji]):
        log = self.bot.get_channel(await getchan(guild.id))

        removed_emojis = [emoji for emoji in before if emoji not in after]
        
        for emoji in removed_emojis:
            async for entry in guild.audit_logs(action=disnake.AuditLogAction.emoji_delete, limit=1):
                deleter = entry.user
                break
            else:
                deleter = None

            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")

            embed = disnake.Embed(title="Удаление эмодзи", color=await getcolor(guild.id))
            embed.add_field(name="Эмодзи", value=f"{emoji} (ID: {emoji.id})")
            embed.add_field(name="Удалено пользователем", value=deleter.mention if deleter else "Неизвестен")
            embed.add_field(name="Время удаления", value=current_time)

            await log.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(RemoveEmoji(bot))
