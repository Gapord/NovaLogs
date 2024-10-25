from datetime import datetime
import datetime
import disnake
from disnake.ext import commands
import config as c
from database.getfromdb import *



class JoinMember(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.User):
        guild = member.guild
        log = self.bot.get_channel(await getchan(member.guild.id))
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(title="Вход на сервер", color = await getcolor(member.guild.id))
        embed.add_field(name="Пользователь", value=member.mention)
        embed.add_field(name="Точное время", value=current_time)

        await log.send(embed=embed)
    

def setup(bot: commands.Bot):
    bot.add_cog(JoinMember(bot))