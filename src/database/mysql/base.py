from sqlalchemy.ext.asyncio import create_async_engine

import config as c


class MySQLDatabase:
    def __init__(self):
        self.engine = create_async_engine(
            f"mysql+aiomysql://{c.db_user}:{c.password}@{c.db_host}/{c.db_name}",
        )