import disnake
from disnake.ext import commands

import config as c
from src.database.base import Database


class CustomClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=c.pref,
            help_command=None,
            intents=disnake.Intents.all(),
            reload=True,
            activity=disnake.Activity(type=disnake.ActivityType.watching, name=c.view),
        )

        self.db = Database()
