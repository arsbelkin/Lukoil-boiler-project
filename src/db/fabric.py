from .strategies.abs_strategy import DatabaseStrategy

from .strategies.pg_stategy import PostgreSQLStrategy
from .strategies.sqlite_strategy import SQLiteStrategy

from db.config import Config


def FabricDBStategy(db_type: str) -> DatabaseStrategy:
    if db_type == "postgresql":
        return PostgreSQLStrategy(Config.POSTGRES_CONFIG)
    else:
        return SQLiteStrategy(Config.SQLITE_DB_FILE)
