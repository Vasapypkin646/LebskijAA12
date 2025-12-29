"""
Логирование операций.
"""

from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """Уровни логирования."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """Класс для логирования."""
    
    def __init__(self, log_file: str = "app.log"):
        self._log_file = log_file
        self._min_level = LogLevel.INFO
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """Записать сообщение в лог."""
        if level.value >= self._min_level.value:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level.value}] {message}"
            
            print(log_entry)  # Вывод в консоль
            
            # Запись в файл
            try:
                with open(self._log_file, 'a', encoding='utf-8') as file:
                    file.write(log_entry + '\n')
            except Exception:
                pass  # Если не удалось записать в файл, просто выводим в консоль
    
    def set_level(self, level: LogLevel) -> None:
        """Установить минимальный уровень логирования."""
        self._min_level = level