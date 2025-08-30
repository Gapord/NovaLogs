from sqlalchemy.ext.asyncio import create_async_engine

import config as c


class SQLiteDatabase:
    def __init__(self):
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{c.db_path}",
        )
