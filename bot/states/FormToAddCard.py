from aiogram.dispatcher.filters.state import State, StatesGroup


class FormToAddCard(StatesGroup):
    card = State()
    bank = State()
    telegram_id: int
