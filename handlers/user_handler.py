import logging
import asyncio

from database.db import get_session
from aiogram import Router, F
from database.models import User
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import (yes_no_subscribe,
                                 watch_the_video,
                                 yes_no_watch_kurs,
                                 press_button_anketa,
                                 press_policy_button,)
from sqlalchemy import select
from lexicon.lexicon_ru import RU, RU_MAIN_MENU

logger = logging.getLogger(__name__)

user_router = Router()

CHANNEL_ID = "@viktoriya_izoriya"

# Срабатывает на нажатие пользователем кнопки /start и 
# выполняет проверку, занесен ли пользователь в БД
# Если нет, то записывает его данные
@user_router.message(CommandStart())
async def process_start_command(message: Message):
    async with get_session() as session:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = result.scalar_one_or_none()

            if not user:
                new_user = User(telegram_id=message.from_user.id)
                session.add(new_user)
            await message.answer_photo(photo='https://disk.yandex.ru/i/9E5Ps69rQ7ABkQ', caption=RU["greeating_at_the_start"], 
                                 reply_markup=yes_no_subscribe())

# Этот хэндлер срабатывает на команду /help
@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer_photo(
        photo='https://disk.yandex.ru/i/mKKufoHpJ6Inmg',
        caption=RU_MAIN_MENU['/help']
    )

# Этот хэндлер срабатывает на команду /policy
@user_router.message(Command(commands='policy'))
async def process_policy_command(message: Message):
    await message.answer(
        text=RU_MAIN_MENU['policy_conf'],
        reply_markup=press_policy_button()
    )

# Нажатие на кнопку "Уже подписан"
@user_router.callback_query(F.data == "already_channel")
async def check_subscription(callback: CallbackQuery, bot):
    user_id = callback.from_user.id
    
    await callback.message.answer(
        text=RU['subscription_check']
    )

    await asyncio.sleep(3)
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

        if member.status in ("member", "administrator", "creator"):
            await callback.message.answer_photo(
                photo='https://disk.yandex.ru/i/dhYXNXjz_xiEDw',
                caption=RU['signed_to_the_channel']
            )
            await callback.answer()
        else:
            await callback.message.answer(
                text=RU['not_signed_to_the_channel'],
                reply_markup=yes_no_subscribe()
            )
            await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        await callback.message.answer(
            text="Не удалось проверить подписку. Попробуй позже"
        )
        await callback.answer()

# Хэндлер сработает на нажатие команды бесплатный урок "Форма"
@user_router.message(Command(commands='free'))
async def process_free_lesson_command(message: Message):
    await message.answer_photo(
        photo='https://disk.yandex.ru/i/u-RQZq4Avz--Hw',
        caption=RU_MAIN_MENU['/free_lesson'],
        reply_markup=watch_the_video()
    )

# Будет срабатывать на жатание команды /kurs
@user_router.message(Command(commands='kurs'))
async def process_press_kurs_command(message: Message):
    await message.answer_photo(
        photo='https://disk.yandex.ru/i/xj6r5-NvZDcIeg',
        caption=RU_MAIN_MENU['/kurs'],
        reply_markup=yes_no_watch_kurs()
    )

# Срабатывает на нажатие кнопки "Открыть анкету предзаписи"
@user_router.callback_query(F.data == 'yes_kurs')
async def check_yes_kurs_button(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo='https://disk.yandex.ru/i/vVqtWpXRh65FPA',
        caption=RU_MAIN_MENU['i_want_to_get'],
        reply_markup=press_button_anketa()
    )

# Будет срабатывать на нажатие кнопки "Так просто читаю"
@user_router.callback_query(F.data == 'no_kurs')
async def check_no_kurs_button(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://disk.yandex.ru/i/IisEmTtiaFSGPg',
        caption=RU_MAIN_MENU['i_just_think']
    )

# Хэндлер срабатывает на нажатие команды /benefit
@user_router.message(Command(commands='use'))
async def process_benefit_command(message: Message):
    await message.answer_photo(
        photo='https://disk.yandex.ru/i/XxF5wgXve2gwOg',
        caption=RU_MAIN_MENU['/benefit'],
        disable_web_page_preview=True
    )