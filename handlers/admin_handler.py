import logging

from aiogram.fsm.context import FSMContext
from states.admin_states import Mailing
from database.db import get_session
from database.models import User
from sqlalchemy import select
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config_data.config import load_config
from filters.is_admin import IsAdmin
from keyboards.admin_keyboards import get_admin_menu
from lexicon.lexicon_ru import ADMIN_MENU, OTHER_USER_MESSAGE

logger = logging.getLogger(__name__)

config = load_config()
admin_ids = config.bot.admin_ids

admin_router = Router()

# Проверяет, является ли пользователь админом и разрешает пользоваться
# админ-панелью
@admin_router.message(Command(commands='admin_panel'), IsAdmin(admin_ids))
async def admin_panel_handler(message: Message):
    await message.answer(
        text=ADMIN_MENU['hello_admin'],
        reply_markup=get_admin_menu()
    )

# Логическое отрицание фильтра ~IsAdmin 
# Запрещает пользователю использовать админ-панель, если он не является
# администратором
@admin_router.message(Command(commands='admin_panel'), ~IsAdmin(admin_ids))
async def not_admin_panel_handler(message: Message):
    await message.answer_photo(
        photo='https://disk.yandex.ru/i/XgHlXnCuf-8LUg',
        caption=OTHER_USER_MESSAGE['not_admin_user']
    )

# ----------------Обработчик кнопок-------------------

# Статистика
@admin_router.callback_query(F.data == "admin_stats")
async def process_admin_stats(callback: CallbackQuery):
    async with get_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        total_users = len(users)

    await callback.message.answer(
        text=f"{ADMIN_MENU['stats']} {total_users}"
    )
    await callback.answer()

# Рассылка
@admin_router.callback_query(F.data == "admin_broadcast")
async def process_admin_broadcast(callback: CallbackQuery,
                                  state: FSMContext):
    await callback.message.answer(
        text=ADMIN_MENU['sending_text']
    )
    await state.set_state(Mailing.waiting_for_message)
    await callback.answer()

# Выход
@admin_router.callback_query(F.data == "admin_exit")
async def process_admin_exit(callback: CallbackQuery):
    await callback.message.answer(
        text=ADMIN_MENU['exit']
    )
    await callback.message.delete()

#------------Обработка текста рассылки и отправка-------------
@admin_router.message(Mailing.waiting_for_message)
async def process_mailing_message(message: Message,
                                  state: FSMContext):
    mailing_text = message.text

    async with get_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

    sent_count = 0
    for user in users:
        try:
            await message.bot.send_message(chat_id=user.telegram_id,
                                           text=mailing_text)
            sent_count += 1
        except Exception as e:
            logging.exception(f"Не удалось отправить пользователю {user.telegram_id}: {e}")

    await message.answer(f"✅ Сообщение отправлено {sent_count} пользователям")
    await state.clear()