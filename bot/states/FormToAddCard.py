from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class FormToAddCard(StatesGroup):
    card = State()
    bank = State()
    message: types.Message
    telegram_id: int
