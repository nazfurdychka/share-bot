from aiogram.dispatcher.filters.state import State, StatesGroup


class FormToCreatePurchase(StatesGroup):
    title = State()
    cost = State()
