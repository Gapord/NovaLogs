from datetime import datetime
import disnake
from disnake.ext import commands
from database.getfromdb import *

class EditMSG(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
                if before.author.id == 1128663070542155847:
                      return
                if before.channel.id == 1272523864966037546:
                      return
                log = self.bot.get_channel(await getchan(before.guild.id))
                embed = disnake.Embed(title="Редактирование сообщения", color=await getcolor(before.guild.id))
                embed.add_field(name="Автор", value=f"{after.author.mention}")
                embed.add_field(name="Канал", value=f"<#{after.channel.id}>")
                embed.add_field(name="Сообщение до", value=f"{before.content}", inline=False)
                embed.add_field(name="Сообщение после", value=f"{after.content}")
                await log.send(embed=embed)

def setup(bot):
    bot.add_cog(EditMSG(bot))
