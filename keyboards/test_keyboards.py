from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_test import TEST_MENU, URL_BUTTONS_TEXT

def pass_the_test_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=TEST_MENU["pass_the_test_btn"],
            callback_data="start_test"
        ),
        width=1
    )
    return kb.as_markup()

def answer_keyboard(
        question_number: int,
        options: list[str],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=options[0], callback_data=f"{question_number}:1"
        ),
        InlineKeyboardButton(
            text=options[1], callback_data=f"{question_number}:2"
        ),
        InlineKeyboardButton(
            text=options[2], callback_data=f"{question_number}:3"
        ),
        width=1
    )
    return kb.as_markup()

def keyboard_url_buttons_low() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['forma_everyone'],
            url='https://youtu.be/cez68l66JjA'
        ),
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['article'],
            url='https://telegra.ph/5-oshibok-kotorye-sovershayut-pochti-vse-mastera-v-nachale-06-22'
        ),
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['podcast'],
            url='https://t.me/viktoriya_izoriya/14'
        ),
        width=1
    )
    return kb.as_markup()

def keyboard_url_buttons_medium() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['forma_everyone'],
            url='https://youtu.be/cez68l66JjA'
        ),
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['article'],
            url='https://telegra.ph/2-post-06-22'
        ),
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['podcast'],
            url='https://t.me/izoriachat/17'
        ),
        width=1
    )
    return kb.as_markup()

def keyboard_url_buttons_high() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['forma_everyone'],
            url='https://youtu.be/cez68l66JjA'
        ),
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['article'],
            url='https://telegra.ph/VSE-HOTYAT-KAK-VSE--I-TY-UZHE-NE-MOZHESH-06-22'
        ),
        InlineKeyboardButton(
            text=URL_BUTTONS_TEXT['podcast'],
            url='https://t.me/izoriachat/18'
        ),
        width=1
    )
    return kb.as_markup()