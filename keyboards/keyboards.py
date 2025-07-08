from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import RU, RU_MAIN_MENU

CHANNEL_ID = "@viktoriya_izoriya"

# Кнопки после старта подтверждение подписки на канал или нет
def yes_no_subscribe() -> InlineKeyboardMarkup:
    # Объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=RU['subscribe_to_the_channel'],
            url=f"https://t.me/{CHANNEL_ID[1:]}"
        ),
        InlineKeyboardButton(
            text=RU['already_signed'],
            callback_data='already_channel'
        ),
        width=1
    )
    return kb_builder.as_markup()

# Кнопка "Смотреть видео" под сообщением бесплатного 
# урока "Форма"
def watch_the_video() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=RU_MAIN_MENU['see_the_video'],
            url="https://youtu.be/cez68l66JjA"
        )
    )
    return kb_builder.as_markup()

# Кнопки после сообщения про курс (нажатие на /kurs)
def yes_no_watch_kurs() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=RU_MAIN_MENU['yes_want_kurs'],
            callback_data='yes_kurs'
        ),
        InlineKeyboardButton(
            text=RU_MAIN_MENU['no_want_kurs'],
            callback_data='no_kurs'
        ),
        width=1
    )
    return kb_builder.as_markup()

# Кнопка для открытия анкеты для записи на курс
def press_button_anketa() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=RU_MAIN_MENU['open_anket'],
            url='https://forms.gle/2g5TAxhXm9PvrvwGA'
        ),
        width=1
    )
    return kb_builder.as_markup()

# Кнопка "Политика конфиденциальности"
def press_policy_button() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=RU_MAIN_MENU['/policy'],
            url='https://tinyurl.com/3k64btt3'
        ),
        width=1
    )
    return kb_builder.as_markup()