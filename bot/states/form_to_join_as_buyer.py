from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    amount_payed = State()
    amount_max: int
    message: types.Message
    purchase_id: str

