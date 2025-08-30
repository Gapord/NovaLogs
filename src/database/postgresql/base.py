from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

import config as c


class PostgreSQLDatabase:
    def __init__(self):
        self._ensure_database()
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{c.db_user}:{c.password}@{c.db_host}/{c.db_name}"
        )

    def _ensure_database(self):
        engine = create_engine(
            f"postgresql+psycopg2://{c.db_user}:{c.password}@{c.db_host}/postgres"
        )
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            res = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": c.db_name},
            )
            exists = res.scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE "{c.db_name}"'))