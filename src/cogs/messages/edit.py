import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class EditMSG(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        guild_data = await self.bot.db.fetch_guild_data(after.guild.id)
        if guild_data is None:
            return

        log = self.bot.get_channel(guild_data.channel_id)

        embed = disnake.Embed(
            title="Редактирование сообщения",
            color=guild_data.color,
        )
        embed.add_field(name="Автор", value=after.author.mention)
        embed.add_field(name="Канал", value=after.channel.mention)
        embed.add_field(name="Сообщение до", value=before.content, inline=False)
        embed.add_field(name="Сообщение после", value=after.content)
        await log.send(embed=embed)


def setup(bot: CustomClient):
    bot.add_cog(EditMSG(bot))
