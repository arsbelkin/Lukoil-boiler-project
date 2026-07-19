import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс конфигурации приложения"""

    DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

    POSTGRES_CONFIG = {
        "dbname": os.getenv("POSTGRES_DB", "boiler_db"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }

    SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "boiler.db")

    CLEAR_TABLES = os.getenv("CLEAR_TABLES", "False") == "True"

    @classmethod
    def get_db_type(cls):
        """Возвращает тип используемой БД"""
        if cls.DB_TYPE in ["postgresql", "postgres", "pg"]:
            return "postgresql"
        else:
            return "sqlite"
