from aiogram.fsm.state import State, StatesGroup

class Mailing(StatesGroup):
    waiting_for_message = State()