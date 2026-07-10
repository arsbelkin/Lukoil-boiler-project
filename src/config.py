import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    """Класс конфигурации приложения"""
    
    # Тип базы данных
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite').lower()
    
    # Настройки PostgreSQL
    POSTGRES_CONFIG = {
        'dbname': os.getenv('POSTGRES_DB', 'boiler_db'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
    }
    
    # Настройки SQLite
    SQLITE_DB_FILE = os.getenv('SQLITE_DB_FILE', 'boiler.db')
    
    @classmethod
    def get_db_type(cls):
        """Возвращает тип используемой БД"""
        if cls.DB_TYPE in ['postgresql', 'postgres', 'pg']:
            return 'postgresql'
        else:
            return 'sqlite'