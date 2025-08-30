import disnake
from dotenv import load_dotenv
import os

load_dotenv()


token = os.getenv("TOKEN")

game = "by Gapord"
pref = "."

dbstatus = os.getenv("DB_TYPE")

if dbstatus == "sqlite":
    db_path = "src/database/sqlite/bases/guilds.db"

if dbstatus == "mysql":
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

colors = {
    "blue": disnake.Color.blue(),
    "red": disnake.Color.red(),
    "green": disnake.Color.green(),
    "yellow": disnake.Color.yellow(),
    "orange": disnake.Color.orange(),
    "purple": disnake.Color.purple(),
    "black": disnake.Color.from_rgb(0, 0, 0),
    "white": disnake.Color.from_rgb(255, 255, 255),
}
