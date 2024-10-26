import disnake
from disnake.ext import commands
import datetime
from database.getfromdb import getchan, getcolor


class CreateRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: disnake.Role):
        guild = role.guild
        log = self.bot.get_channel(await getchan(guild.id))

        async for entry in guild.audit_logs(
            action=disnake.AuditLogAction.role_create, limit=1
        ):
            creator = entry.user
            break
        else:
            creator = None

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(
            title="Создание роли", color=await getcolor(guild.id)
        )
        embed.add_field(name="Роль", value=f"{role.name} (ID: {role.id})")
        embed.add_field(
            name="Создано пользователем",
            value=creator.mention if creator else "Неизвестен",
        )
        embed.add_field(name="Время создания", value=current_time)

        await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CreateRole(bot))
