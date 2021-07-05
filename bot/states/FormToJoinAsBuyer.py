from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class FormToJoinAsBuyer(StatesGroup):
    amount_payed = State()
    amount_max: float
    message: types.Message
    call: types.CallbackQuery
    purchase_id: str
