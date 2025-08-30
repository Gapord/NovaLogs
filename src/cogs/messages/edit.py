import io

import disnake
from disnake.ext import commands

from src.classes.custom_client import CustomClient


class EditMSG(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if not before.guild:
            return
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
        files = (
            [await att.to_file() for att in before.attachments + after.attachments]
            if (before.attachments or after.attachments)
            else []
        )

        def prepare_text_file(label, text):
            if not text:
                return None
            if len(text) > 500:
                file = io.StringIO(text)
                f = disnake.File(fp=file, filename=f"{label}_{before.id}.txt")
                files.append(f)
                return None
            return f"```{text}```"

        before_field = prepare_text_file("before", before.content)
        after_field = prepare_text_file("after", after.content)

        if before_field and before_field != "":
            embed.add_field(name="Сообщение до", value=before_field, inline=False)
        if after_field and after_field != "":
            embed.add_field(name="Сообщение после", value=after_field, inline=False)

        await log.send(embed=embed, files=files if files else None)


def setup(bot: CustomClient):
    bot.add_cog(EditMSG(bot))
