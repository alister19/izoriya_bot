from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import ADMIN_MENU

# Кнопки для админки
def get_admin_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=ADMIN_MENU['statistic'],
            callback_data='admin_stats'
        ),
        InlineKeyboardButton(
            text=ADMIN_MENU['sending'],
            callback_data='admin_broadcast'
        ),
        InlineKeyboardButton(
            text=ADMIN_MENU['leave_the_admin_panel'],
            callback_data='admin_exit'
        ),
        width=2
    )
    return kb.as_markup()