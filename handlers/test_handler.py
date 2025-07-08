from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.test_states import TestStates
from aiogram.types import InlineKeyboardMarkup
from keyboards.test_keyboards import answer_keyboard, pass_the_test_button
from keyboards.test_keyboards import (keyboard_url_buttons_low,
                                      keyboard_url_buttons_high,
                                      keyboard_url_buttons_medium)
from lexicon.lexicon_test import TEST_MENU, QUESTIONS, ANSWER_OPTIONS, RESULTS

test_router = Router()

@test_router.message(Command(commands='test'))
async def process_start_test(message: Message):
    await message.answer_photo(
        photo='https://disk.yandex.ru/i/iUDklTTo3FXY9Q',
        caption=TEST_MENU['test_word'],
        reply_markup=pass_the_test_button()
    )

@test_router.callback_query(F.data == "start_test")
async def start_test_begin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(score=0, current_q=1)
    await state.set_state(TestStates.question)

    q_text = QUESTIONS[1]
    options = ANSWER_OPTIONS[1]
    msg = await callback.message.answer(
        text=q_text,
        reply_markup=answer_keyboard(1, options)
    )

    # Сохраняем id сообщения с вопросом, чтобы потом удалять
    await state.update_data(last_message_id=msg.message_id)

    await callback.answer()

@test_router.callback_query(F.data.regexp(r"^\d+:[123]$"), TestStates.question)
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_q = data["current_q"]
    score = data["score"]
    last_msg_id = data["last_message_id"]

    q_num, points = map(int, callback.data.split(":"))
    if q_num != current_q:
        await callback.answer()
        return
    
    score += points

    # удаляем сообщение с кнопками
    await callback.message.delete()

    if current_q < len(QUESTIONS):
        next_q = current_q + 1
        await state.update_data(score=score, current_q=next_q)

        q_text = QUESTIONS[next_q]
        options = ANSWER_OPTIONS[next_q]

        new_msg = await callback.message.answer(
            text=q_text,
            reply_markup=answer_keyboard(next_q, options)
        )
        await state.update_data(last_message_id=new_msg.message_id)

    else:
        result_text, result_keyboard = get_result_text(score)
        await callback.message.answer(result_text, reply_markup=result_keyboard)
        await state.clear()

    await callback.answer()

def get_result_text(score: int) -> tuple[str, InlineKeyboardMarkup, str]:
    if score <= 16:
        return RESULTS["low"], keyboard_url_buttons_low()
    elif 17 <= score <= 23:
        return RESULTS["medium"], keyboard_url_buttons_medium()
    else:
        return RESULTS["high"], keyboard_url_buttons_high()