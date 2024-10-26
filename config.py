from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

game = "by Gapord"
pref = "."

dbstatus = 2 # 1 → sqlite, 2 → mysql
