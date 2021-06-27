from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    card = State()
    bank = State()
    message: types.Message
    user_id: int
