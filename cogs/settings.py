import disnake
from disnake.ext import commands
from database.sqlite.init import InitDB

colors = {
    "blue": disnake.Color.blue(),
    "red": disnake.Color.red(),
    "green": disnake.Color.green(),
    "yellow": disnake.Color.yellow(),
    "orange": disnake.Color.orange(),
    "purple": disnake.Color.purple(),
    "black": disnake.Color.from_rgb(0, 0, 0),  # Black
    "white": disnake.Color.from_rgb(255, 255, 255)  # White
}

class BotSettings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Настройка сервера")
    async def setting(
        self, 
        ctx,
        channel: disnake.abc.GuildChannel,
        color: str = commands.Param(choices=list(colors.keys()), description="Выберите цвет для сервера")
    ):
        if not ctx.author.guild_permissions.administrator:
            embed = disnake.Embed(title="Ошибка", color=disnake.Color.red())
            embed.add_field(name="", value="Для выполнения этой команды у вас должны быть права администратора.")
            await ctx.send(embed=embed, ephemeral=True)
            return
        init_db = InitDB(ctx.guild.id)
        await init_db.initdb(color, channel.id)

        embed = disnake.Embed(
            title="Настройки сервера обновлены",
            color=colors[color]
        )
        embed.add_field(name="Канал логов", value=f"<#{channel.id}>")
        embed.add_field(name="Цвет эмбедов", value=color.capitalize())
        
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(BotSettings(bot))
