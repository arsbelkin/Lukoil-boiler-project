from .abs_strategy import DatabaseStrategy

import sys
from typing import Dict, Any, List
from datetime import datetime

try:
    import sqlite3

    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False
    print("❌ ERROR: sqlite3 не доступен!")
    sys.exit(1)


class SQLiteStrategy(DatabaseStrategy):
    """Стратегия для SQLite"""

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn: sqlite3.Connection
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
            cursor.execute(
                """
                INSERT INTO boiler_history 
                (timestamp, input_temp_hot, input_temp_cold, valve_hot, 
                 valve_cold, valve_out, output_temp, water_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    data["inputHotTemp"],
                    data["inputColdTemp"],
                    data["valveHot"],
                    data["valveCold"],
                    data["valveOut"],
                    data["outputTemp"],
                    data["waterLevel"],
                ),
            )
            self.conn.commit()
        except Exception as e:
            print(f"❌ Ошибка записи в SQLite: {e}")

    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получение последних записей для графиков"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM boiler_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (limit,),
            )

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
