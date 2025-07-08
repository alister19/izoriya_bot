from aiogram import Router, F
from aiogram.types import Message
from lexicon.lexicon_ru import OTHER_USER_MESSAGE

other_router = Router()

# Обработка неизвестных команд
@other_router.message(F.text.startswith('/'))
async def process_unknown_command(message: Message):
    await message.answer(
        text=OTHER_USER_MESSAGE['unknown_commands']
    )

# Обработка произвольного текста
@other_router.message(F.text)
async def process_unknown_text(message: Message):
    await message.answer(
        text=OTHER_USER_MESSAGE['unknown_text']
    )

# Обработка полученного фото
@other_router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(
        text=OTHER_USER_MESSAGE['handle_photo']
    )

# Обработка полученного документа
@other_router.message(F.document)
async def handle_document(message: Message):
    await message.answer(
        text=OTHER_USER_MESSAGE['handle_document']
    )

# Обработка полученного стикера
@other_router.message(F.sticker)
async def handle_sticker(message: Message):
    await message.answer(
        text=OTHER_USER_MESSAGE['handle_sticker']
    )