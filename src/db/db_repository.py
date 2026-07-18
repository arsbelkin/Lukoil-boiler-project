from typing import Dict, Any, List

from .config import Config
from .fabric import FabricDBStategy

from .strategies.abs_strategy import DatabaseStrategy


class DatabaseRepositoryPattern:
    def __init__(self, strategy: DatabaseStrategy | None = None):
        if strategy is None:
            strategy = self._init_strategy()

        self._strategy = strategy

        if Config.CLEAR_TABLES:
            self._strategy.drop_tables()

    def _init_strategy(self) -> DatabaseStrategy:
        db_type = Config.get_db_type()

        return FabricDBStategy(db_type)

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
