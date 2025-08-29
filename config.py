import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

game = "by Gapord"
pref = "."

dbstatus = 1  # 1 → sqlite, 2 → mysql
