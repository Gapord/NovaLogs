import os

import aiomysql
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.db = os.getenv("DB_NAME")
        self.conn = None

    async def connect(self):
        self.conn = await aiomysql.connect(
            host=self.host, user=self.user, password=self.password, db=self.db
        )
        return self.conn
