import json
import disnake
from disnake.ext import commands
import config as c

bot = commands.Bot(
    command_prefix=c.pref,
    help_command=None,
    intents=disnake.Intents.all(),
    reload=True,
    activity=disnake.Game(c.game),
)


@bot.command()
async def dev1(ctx):
    channel = bot.get_channel(1168620321348255754)
    if channel is None:
        await ctx.reply("Канал не найден.")
        return

    overwrite = channel.overwrites_for(ctx.author)
    if overwrite.view_channel:

        overwrite.view_channel = False
        await channel.set_permissions(ctx.author, overwrite=overwrite)
        await ctx.reply(f"Доступ к каналу для {ctx.author.mention} удалён.")
    else:
        overwrite.view_channel = True
        await channel.set_permissions(ctx.author, overwrite=overwrite)
        await ctx.reply(f"{ctx.author.mention} получил доступ к каналу.")
    await ctx.message.delete()


@bot.event
async def on_ready():
    print(f"{bot.user.name} готов к работе")


with open("cogs_url.json", "r") as json_file:
    cogs_data = json.load(json_file)

for url in cogs_data["cogs"]:
    bot.load_extension(url)


bot.run(c.token)
