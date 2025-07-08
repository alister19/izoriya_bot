import logging
from logging.handlers import TimedRotatingFileHandler
from config_data.config import load_config

config = load_config()

# Создаем логгер
logger = logging.getLogger()
logger.setLevel(config.log.level)

# Формат логов
formatter = logging.Formatter(config.log.format)

# Файл для логов
file_handler = TimedRotatingFileHandler(
    filename="logs/bot.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
file_handler.setLevel(config.log.level)

# Консольный логгер для ошибок
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.ERROR)

# Добавление хендлеров в логгер
logger.addHandler(file_handler)
logger.addHandler(console_handler)