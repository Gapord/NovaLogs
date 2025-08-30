from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

import config as c


class MySQLDatabase:
    def __init__(self):
        self._ensure_database()
        self.engine = create_async_engine(
            f"mysql+aiomysql://{c.db_user}:{c.password}@{c.db_host}/{c.db_name}",
        )

    def _ensure_database(self):
        engine = create_engine(f"mysql+pymysql://{c.db_user}:{c.password}@{c.db_host}/")
        with engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS {c.db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                )
            )
