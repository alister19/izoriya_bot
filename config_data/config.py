import logging
import os

from dataclasses import dataclass
from environs import Env

logger = logging.getLogger(__name__)

@dataclass
class BotSettings:
    token: str
    admin_ids: list[int]

@dataclass
class DatabaseSettings:
    db_url: str

@dataclass
class LoggingSettings:
    level: str
    format: str

@dataclass
class Config:
    bot: BotSettings
    db: DatabaseSettings
    log: LoggingSettings

# Функция для загрузки необходимых конфигов
def load_config(path: str | None = None) -> Config:
    env = Env()

    # Проверка на загрузку по пути файла .env
    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
        else:
            logger.info("Loading .env from '%s'", path)
    
    # Читаем BOT_TOKEN
    env.read_env(path)
    token = env("BOT_TOKEN")

    # Проверка на присутствие токена в конфигурационном файле .env
    if not token:
        raise ValueError("BOT_TOKEN must not be empty")
    
    # Читаем ADMIN_IDS
    raw_ids = env.list("ADMIN_IDS", default=[])

    # Проверям, что ADMIN_IDS имеет тип данных integer
    try:
        admin_ids = [int(x) for x in raw_ids]
    except Exception as e:
        raise ValueError(f"ADMIN_IDS must be integers, got: {raw_ids}") from e
    
    # Формируем database_url
    db_url = (
        f"postgresql+asyncpg://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}"
        f"@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"
    )

    # Настройка логгирования
    logg_settings = LoggingSettings(
        level=env("LOG_LEVEL"),
        format=env("LOG_FORMAT"),
    )

    # Выводим сообщение о успешной загрузке всех конфигов
    logger.info("Congratulation loaded successfully")

    return Config(
        bot=BotSettings(token=token, admin_ids=admin_ids),
        db=DatabaseSettings(db_url=db_url),
        log=logg_settings
    )