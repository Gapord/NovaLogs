import disnake
from disnake.ext import commands

from src.database.base import Database

import config as c

class CustomClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=c.pref,
            help_command=None,
            intents=disnake.Intents.all(),
            reload=True,
            activity=disnake.Game(c.game),
        )

        self.db = Database()