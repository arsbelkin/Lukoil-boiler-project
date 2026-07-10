from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional
import sys

# Импортируем библиотеки (могут быть не установлены)
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️  WARNING: psycopg2 не установлен. PostgreSQL будет недоступен.")
    print("   Установите: pip install psycopg2-binary")

try:
    import sqlite3
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False
    print("❌ ERROR: sqlite3 не доступен!")
    sys.exit(1)


class DatabaseStrategy(ABC):
    """Абстрактный класс стратегии работы с БД"""
    
    @abstractmethod
    def init_tables(self):
        """Создаёт таблицы если не существуют"""
        pass
    
    @abstractmethod
    def log_data(self, data: Dict[str, Any]):
        """Записывает данные в БД"""
        pass
    
    @abstractmethod
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получает историю данных для графиков"""
        pass
    
    @abstractmethod
    def close(self):
        """Закрывает соединение"""
        pass


class SQLiteStrategy(DatabaseStrategy):
    """Стратегия для SQLite"""
    
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = None
        self._connect()
        print(f"✅ SQLite стратегия инициализирована (файл: {db_file})")
    
    def _connect(self):
        """Подключение к SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # чтобы обращаться по имени колонки
        except Exception as e:
            print(f"❌ Ошибка подключения к SQLite: {e}")
            sys.exit(1)
    
    def init_tables(self):
        """Создаёт таблицы в SQLite"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS boiler_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                input_temp_hot REAL NOT NULL,
                input_temp_cold REAL NOT NULL,
                valve_hot REAL NOT NULL,
                valve_cold REAL NOT NULL,
                valve_out REAL NOT NULL,
                output_temp REAL NOT NULL,
                water_level REAL NOT NULL
            )
        """)
        
        # Создаём индекс для ускорения запросов по времени
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON boiler_history(timestamp)
        """)
        
        self.conn.commit()
        print(" Таблицы SQLite созданы/проверены")
    
    def log_data(self, data: Dict[str, Any]):
        """Запись данных в SQLite"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO boiler_history 
                (timestamp, input_temp_hot, input_temp_cold, valve_hot, 
                 valve_cold, valve_out, output_temp, water_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data['input_temp_hot'],
                data['input_temp_cold'],
                data['valve_hot'],
                data['valve_cold'],
                data['valve_out'],
                data['output_temp'],
                data['water_level']
            ))
            self.conn.commit()
        except Exception as e:
            print(f"❌ Ошибка записи в SQLite: {e}")
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получение последних записей для графиков"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM boiler_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            # Преобразуем в список словарей
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Ошибка чтения из SQLite: {e}")
            return []
    
    def close(self):
        """Закрытие соединения"""
        if self.conn:
            self.conn.close()


class PostgreSQLStrategy(DatabaseStrategy):
    """Стратегия для PostgreSQL"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.conn = None
        self._connect()
        print(f"✅ PostgreSQL стратегия инициализирована (база: {config['dbname']})")
    
    def _connect(self):
        """Подключение к PostgreSQL"""
        if not POSTGRES_AVAILABLE:
            print("❌ psycopg2 не установлен. Переключитесь на SQLite в .env файле")
            sys.exit(1)
        
        try:
            self.conn = psycopg2.connect(**self.config)
            self.conn.autocommit = False
        except Exception as e:
            print(f"⚠️  Не удалось подключиться к PostgreSQL: {e}")
            print("   Проверьте:")
            print("   1. Запущен ли PostgreSQL сервер")
            print("   2. Правильность учётных данных в .env файле")
            print("   3. Существует ли база данных")
            print("   → Переключитесь на SQLite: DB_TYPE=sqlite")
            sys.exit(1)
    
    def init_tables(self):
        """Создаёт таблицы в PostgreSQL"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS boiler_history (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                input_temp_hot DOUBLE PRECISION NOT NULL,
                input_temp_cold DOUBLE PRECISION NOT NULL,
                valve_hot DOUBLE PRECISION NOT NULL,
                valve_cold DOUBLE PRECISION NOT NULL,
                valve_out DOUBLE PRECISION NOT NULL,
                output_temp DOUBLE PRECISION NOT NULL,
                water_level DOUBLE PRECISION NOT NULL
            )
        """)
        
        # Создаём индекс
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_boiler_history_timestamp 
            ON boiler_history(timestamp DESC)
        """)
        
        self.conn.commit()
        print("📊 Таблицы PostgreSQL созданы/проверены")
    
    def log_data(self, data: Dict[str, Any]):
        """Запись данных в PostgreSQL"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO boiler_history 
                (timestamp, input_temp_hot, input_temp_cold, valve_hot, 
                 valve_cold, valve_out, output_temp, water_level)
                VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['input_temp_hot'],
                data['input_temp_cold'],
                data['valve_hot'],
                data['valve_cold'],
                data['valve_out'],
                data['output_temp'],
                data['water_level']
            ))
            self.conn.commit()
        except Exception as e:
            print(f"❌ Ошибка записи в PostgreSQL: {e}")
            self.conn.rollback()
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получение последних записей для графиков"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM boiler_history 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"❌ Ошибка чтения из PostgreSQL: {e}")
            return []
    
    def close(self):
        """Закрытие соединения"""
        if self.conn:
            self.conn.close()


class DatabaseContext:
    """Контекст, который использует стратегию"""
    
    def __init__(self, strategy: DatabaseStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: DatabaseStrategy):
        """Смена стратегии на лету"""
        self._strategy = strategy
        print(f"🔄 Стратегия изменена на: {strategy.__class__.__name__}")
    
    def init_tables(self):
        """Инициализация таблиц"""
        self._strategy.init_tables()
    
    def log_data(self, data: Dict[str, Any]):
        """Логирование данных"""
        self._strategy.log_data(data)
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получение истории"""
        return self._strategy.get_history(limit)
    
    def close(self):
        """Закрытие соединения"""
        self._strategy.close()


def create_database_strategy(db_type: str) -> DatabaseStrategy:
    """
    Фабричный метод для создания нужной стратегии
    
    Args:
        db_type: 'postgresql' или 'sqlite'
    
    Returns:
        Экземпляр соответствующей стратегии
    """
    from db.config import Config
    
    if db_type == 'postgresql':
        return PostgreSQLStrategy(Config.POSTGRES_CONFIG)
    else:
        return SQLiteStrategy(Config.SQLITE_DB_FILE)