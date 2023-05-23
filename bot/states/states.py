from aiogram.filters.state import StatesGroup, State


class Poll(StatesGroup):
    start_poll = State()
    finish_poll = State()
