import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

GAME = "by Gapord"
PREF = "."

DBSTATUS = 1  # 1 → sqlite, 2 → mysql
