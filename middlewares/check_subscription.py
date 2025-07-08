from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from typing import Callable, Awaitable, Dict, Any
from lexicon.lexicon_ru import RU
from keyboards.keyboards import (yes_no_subscribe)

CHANNEL_ID = "@viktoriya_izoriya"

# Проверка подписки пользователя на канал, для доступа ему
# всех функций бота в случае успеха
class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]],
                              Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Разрешаем только команды /start и /help без проверки
        if event.text and event.text.startswith(("/start", "/help")):
            return await handler(event, data)
        
        try:
            member = await event.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=event.from_user.id)
            if member.status in ["left", "kicked"]:
                await event.answer(
                    text=RU['not_signed_to_the_channel'],
                    reply_markup=yes_no_subscribe()
                )
                return    # не передаем в хэндлеры
        except TelegramBadRequest:
            await event.answer(
                text=RU['bad_request']
            )
        # Если подписан - продолжаем обработку
        return await handler(event, data)