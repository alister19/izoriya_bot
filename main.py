import logging
import asyncio

from config_data.logging_config import logger
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import load_config
from handlers import user_handler, admin_handler, test_handler, other_handler
from keyboards.main_menu import set_main_menu
from database import db 
from middlewares.check_subscription import SubscriptionMiddleware

logger = logging.getLogger(__name__)

async def main():
    # Загружаем конфиг
    config = load_config(".env")

    # Настраиваем логирование
    logging.basicConfig(
        level=config.log.level,
        format=config.log.format
    )

    # Инициализируем логгер
    logger.info("Бот запущен")
    logger.error("Произошла ошибка")

    # Инициализируем БД
    await db.init_db(config.db.db_url)

    # Подключение машины состояний
    storage = MemoryStorage()

    # Создаем бота и диспетчер
    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    # Подключаем миддлварь
    dp.message.middleware(SubscriptionMiddleware())

    # Главное меню бота
    await set_main_menu(bot)

    # Подключаем роутеры
    dp.include_router(user_handler.user_router)
    dp.include_router(admin_handler.admin_router)
    dp.include_router(test_handler.test_router)
    dp.include_router(other_handler.other_router)

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())