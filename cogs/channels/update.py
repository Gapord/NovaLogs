import disnake
from disnake.ext import commands
import datetime
from database.getfromdb import getchan, getcolor

class UpdateChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: disnake.abc.GuildChannel, after: disnake.abc.GuildChannel):
        guild = after.guild
        log = self.bot.get_channel(await getchan(guild.id))
        
        async for entry in guild.audit_logs(action=disnake.AuditLogAction.channel_update, limit=1):
            updater = entry.user
            break
        else:
            updater = None

        changes = []
        
        if before.name != after.name:
            changes.append(f"Имя изменено с `{before.name}` на `{after.name}`")
        
        if before.category != after.category:
            changes.append(f"Категория изменена с `{before.category.name if before.category else 'Нет'}` на `{after.category.name if after.category else 'Нет'}`")
        
        if before.position != after.position:
            changes.append(f"Позиция изменена с `{before.position}` на `{after.position}`")
        
        if isinstance(before, disnake.TextChannel) and isinstance(after, disnake.TextChannel):
            if before.topic != after.topic:
                changes.append(f"Описание изменено с `{before.topic or 'Нет'}` на `{after.topic or 'Нет'}`")
            
            if before.slowmode_delay != after.slowmode_delay:
                changes.append(f"Slowmode изменён с `{before.slowmode_delay} секунд` на `{after.slowmode_delay} секунд`")
            
            if before.nsfw != after.nsfw:
                changes.append(f"NSFW-режим изменён на `{'Включен' if after.nsfw else 'Выключен'}`")

        if not changes:
            return

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Обновление канала", color=await getcolor(guild.id))
        embed.add_field(name="Канал", value=f"{after.name} (ID: {after.id})")
        embed.add_field(name="Изменения", value="\n".join(changes), inline=False)
        embed.add_field(name="Ответственный", value=updater.mention if updater else "Неизвестен")
        embed.add_field(name="Время обновления", value=current_time)

        await log.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(UpdateChannel(bot))
