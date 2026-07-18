from .abs_strategy import DatabaseStrategy

from typing import Dict, Any, List
import sys

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.extensions import connection

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️  WARNING: psycopg2 не установлен. PostgreSQL будет недоступен.")
    print("   Установите: pip install psycopg2-binary")


class PostgreSQLStrategy(DatabaseStrategy):
    """Стратегия для PostgreSQL"""

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.conn: connection
        self._connect()

        print(f"✅ PostgreSQL стратегия инициализирована (база: {config['dbname']})")

    def _connect(self):
        """Подключение к PostgreSQL"""
        if not POSTGRES_AVAILABLE:
            print("❌psycopg2 не установлен. Переключитесь на SQLite в .env файле")
            sys.exit(1)

        try:
            self.conn = psycopg2.connect(**self.config)  # type: ignore
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

    def drop_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
                       DROP TABLE IF EXISTS boiler_history;
                       """)

        self.conn.commit()

        print("📊 Таблицы PostgreSQL очищены")


    def log_data(self, data: Dict[str, Any]):
        """Запись данных в PostgreSQL"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO boiler_history 
                (timestamp, input_temp_hot, input_temp_cold, valve_hot, 
                 valve_cold, valve_out, output_temp, water_level)
                VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s)
            """,
                (
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
            print(f"❌ Ошибка записи в PostgreSQL: {e}")
            self.conn.rollback()

    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получение последних записей для графиков"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """
                SELECT * FROM boiler_history 
                ORDER BY timestamp DESC 
                LIMIT %s
            """,
                (limit,),
            )

            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"❌ Ошибка чтения из PostgreSQL: {e}")
            return []

    def close(self):
        """Закрытие соединения"""
        if self.conn:
            self.conn.close()
