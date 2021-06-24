from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    amount = State()
    message: types.Message
    purchase_id: str
