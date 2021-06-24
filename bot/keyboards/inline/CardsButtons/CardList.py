
from aiogram import types


class CardList:
    def __init__(self, users: list[int]):
        users_list = [
            types.InlineKeyboardButton(text="User", callback_data="manage_cards"),
            types.InlineKeyboardButton(text="Back to cards", callback_data="back_to_cards")
        ]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*users_list)
