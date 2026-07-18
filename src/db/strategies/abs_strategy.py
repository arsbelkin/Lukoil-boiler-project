from abc import ABC, abstractmethod
from typing import Dict, Any, List


class DatabaseStrategy(ABC):
    """Абстрактный класс стратегии работы с БД"""

    @abstractmethod
    def init_tables(self):
        """Создаёт таблицы если не существуют"""
        pass

    @abstractmethod
    def drop_tables(self):
        """Очищает таблицы"""
        pass

    @abstractmethod
    def log_data(self, data: Dict[str, Any]):
        """Записывает данные в БД"""
        pass

    @abstractmethod
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Получает историю данных для графиков"""
        ...

    @abstractmethod
    def close(self):
        """Закрывает соединение"""
        pass
